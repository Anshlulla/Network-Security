from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import sys
import warnings
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import (DataIngestionConfig, 
                                      TrainingPipelineConfig, 
                                      DataValidationConfig, 
                                      DataTransformationConfig,
                                      ModelTrainerConfig)
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                         data_validation_config=data_validation_config)
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                 data_transformation_config=data_transformation_config)
        logging.info("Initiate Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                     model_trainer_config=model_trainer_config)
        logging.info("Initiated Model Training")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training Completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    