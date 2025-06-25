import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from src.logging.logger import logging
from src.exception.exception import NetworkSecurityException
from src.constants.constants import *
from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.utils.utils import save_np_array, save_pkl_file

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_tranformer_object(cls) -> Pipeline:
        logging.info("Initializing KNN Imputer")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocesser: Pipeline = Pipeline([("imputer", imputer)])
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return preprocesser

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating Data Transformation")
            self.data_validation_artifact.valid_train_file_path
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            X_train, y_train = train_df.drop(TARGET_COLUMN, axis=1), train_df[TARGET_COLUMN]
            X_test, y_test = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]

            y_train = y_train.replace(to_replace=-1, value=0)
            y_test = y_test.replace(to_replace=-1, value=0)

            preprocessor = self.get_data_tranformer_object()
            X_train_transformer = preprocessor.fit_transform(X_train)
            X_test_transformer = preprocessor.transform(X_test)

            train_arr = np.c_[X_train_transformer, np.array(y_train)]
            test_arr = np.c_[X_test_transformer, np.array(y_test)]

            save_np_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_np_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_pkl_file(self.data_transformation_config.transformed_object_file_path, preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data_transformation_artifact