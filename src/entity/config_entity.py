from datetime import datetime
import os
from src.constants.data_ingestion_constants import *

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline = PIPELINE_NAME
        self.artifacts_name = ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name, timestamp)
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

