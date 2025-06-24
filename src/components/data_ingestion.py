import pymongo.mongo_client
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_CONNECTION_STRING")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.client = pymongo.MongoClient(MONGODB_URL)
    
    def export_collection_as_df(self):
        try:
            db = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            collection = self.client[db][collection_name]
            data = pd.DataFrame(list(collection.find({})))
            if "_id" in data.columns.to_list():
                data.drop("_id", inplace=True, axis=1)
            data.replace({"na", np.nan}, inplace=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data
    
    def export_data_into_feature_store(self, data: pd.DataFrame):
        try:
            featue_store_file_path = self.data_ingestion_config.feature_store_dir
            dir_path = os.path.dirname(featue_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            data.to_csv(featue_store_file_path, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return data
    
    def split_data(self, data: pd.DataFrame):
        try:
            train, test = train_test_split(data, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train-test split")
            
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)

            dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dir_path, exist_ok=True)
            test.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logging.info("Split into train-test sets")            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def initiate_data_ingestion(self):
        try:
            data = self.export_collection_as_df()
            data = self.export_data_into_feature_store(data)
            self.split_data(data)
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, test_file_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        