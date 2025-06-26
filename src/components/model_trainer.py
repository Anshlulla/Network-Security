import os
from tkinter import NE
from matplotlib.pyplot import get
import numpy as np
import sys
import pandas as pd
import mlflow
import mlflow.sklearn
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.constants.constants import *
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.utils import *
from src.utils.estimator import NetworkModel
from src.utils.evaluate_models import evaluate_models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
import dagshub
dagshub.init(repo_owner='anshlulla26', repo_name='Network-Security', mlflow=True)

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "RandomForest": RandomForestClassifier(),
                "DecisionTree": DecisionTreeClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "GradientBoosting": GradientBoostingClassifier(),
                "LogisticRegression": LogisticRegression()
            }

            params = {
                "DecisionTree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "RandomForest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "GradientBoosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LogisticRegression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]
            y_pred_train = best_model.predict(X_train)
            y_pred_test = best_model.predict(X_test)
            train_classification_metrics = get_classification_score(y_train, y_pred_train)
            test_classification_metrics = get_classification_score(y_test, y_pred_test)

            self.track_mlflow(best_model, train_classification_metrics, "train")
            self.track_mlflow(best_model, test_classification_metrics, "test")

            preprocessor = load_pkl_file(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor, best_model)
            save_pkl_file(self.model_trainer_config.trained_model_file_path, network_model)
            
            save_pkl_file("final_model/model.pkl", best_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_classification_metrics,
                test_metric_artifact=test_classification_metrics
            )

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self, best_model, classification_metrics, set):
        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            recall_score = classification_metrics.recall_score
            precision_score = classification_metrics.precision_score
            accuracy_score = classification_metrics.accuracy_score

            mlflow.log_metric(f"{set}_f1_score", f1_score)
            mlflow.log_metric(f"{set}_precision_score", precision_score)
            mlflow.log_metric(f"{set}_recall_score", recall_score)
            mlflow.log_metric(f"{set}_accuracy_score", accuracy_score)
            mlflow.sklearn.log_model(best_model, "model")

    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_np_array(train_file_path)
            test_arr = load_np_array(test_file_path)

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)