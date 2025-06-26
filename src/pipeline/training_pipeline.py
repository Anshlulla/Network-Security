import os
import sys
import warnings
from src.components import data_validation
from src.components import data_ingestion
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import *
from src.entity.artifact_entity import *
warnings.filterwarnings("ignore")

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Initiating Data Ingestion")
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifcat = data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data_ingestion_artifcat
    
    def start_data_validation(self, data_ingestion_artifact) -> DataValidationArtifact:
        try:
            logging.info("Initiated Data Validation")
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data Validation Completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data_validation_artifact
    
    def start_data_transformation(self, data_validation_artifact) -> DataTransformationArtifact:
        try:
            logging.info("Initiated Data Transformation")
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                    data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation Completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data_transformation_artifact
    
    def start_model_trainer(self, data_transformation_artifact) -> ModelTrainerArtifact:
        try:
            logging.info("Initiated Model Training")
            self.model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                        model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Training Completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return model_trainer_artifact
    
    def run_pipeline(self) -> ModelTrainerArtifact:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return model_trainer_artifact