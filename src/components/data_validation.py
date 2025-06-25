from src.entity.artifact_entity import *
from src.entity.config_entity import DataValidationConfig
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.utils.utils import read_yaml_file, write_yaml_file
from src.constants.constants import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        try:
            numOfColumns = len(self._schema_config)
            logging.info(f"Required number of columns: {numOfColumns}")
            logging.info(f"Current number of columns: {len(df.columns)}")
            return numOfColumns == len(df.columns)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_dataset_drift(self, baseDf, curDf, thresh=.005) -> bool:
        try:
            status = True
            report = {}
            for col in list(baseDf.columns):
                d1 = baseDf[col]
                d2 = curDf[col]
                is_sample_dist_same = ks_2samp(d1, d2)
                if is_sample_dist_same.pvalue >= thresh:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    col: {
                        "p_value": is_sample_dist_same.pvalue,
                        "drift_status": is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataIngestionArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            status = self.validate_columns(train_df)
            if not status:
                error = "Train dataframe does not have a valid schema"

            status = self.validate_columns(test_df)
            if not status:
                error = "Test dataframe does not have a valid schema"
            
            status = self.detect_dataset_drift(train_df, test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)

            dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
            os.makedirs(dir_path, exist_ok=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data_validation_artifact