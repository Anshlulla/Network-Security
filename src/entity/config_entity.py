from datetime import datetime
import os
from src.constants.constants import *

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline = PIPELINE_NAME
        self.artifacts_name = ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name, timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
        )
        self.feature_store_dir = os.path.join(
            training_pipeline_config.artifacts_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
        )
        self.train_file_path = os.path.join(
            training_pipeline_config.artifacts_dir, TRAIN_FILE_NAME, FILE_NAME
        )
        self.test_file_path = os.path.join(
            training_pipeline_config.artifacts_dir, TEST_FILE_NAME, FILE_NAME
        )
        self.train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATO
        self.collection_name = DATA_INGESTION_COLLECTION_NAME
        self.database_name = DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join( training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )


class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifacts_dir,DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            PREPROCESSING_OBJECT_FILE_NAME,)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifacts_dir, MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, 
            MODEL_FILE_NAME
        )
        self.expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
