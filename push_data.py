import os
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from src.logging.logger import logging
from src.exception.exception import NetworkSecurityException
import certifi
import pymongo
load_dotenv()

FILE_PATH = r"network-data/phishingData.csv"
DB = "networksecurity"
COLLECTION = "NetworkData"
MONGODB_URL = os.getenv("MONGODB_CONNECTION_STRING")
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self, db, collection, mongodb_url):
        self.db = db
        self.collection = collection
        self.client = pymongo.MongoClient(mongodb_url)

        self.db = self.client[self.db]
        self.collection = self.db[self.collection]
    
    def csv_to_json(self, file_path) -> list:
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            json_data = data.to_json(orient="records") # same for to_dict()
            records = json.loads(json_data)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return records
    
    def insert_data_to_mongodb(self, records):
        try:
            self.collection.insert_many(records)        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        return self.collection.count_documents({})
    

if __name__ == "__main__":
    obj = NetworkDataExtract(db=DB,
                             collection=COLLECTION, 
                             mongodb_url=MONGODB_URL)
    records = obj.csv_to_json(file_path=FILE_PATH)
    lenOfRecords = obj.insert_data_to_mongodb(records=records)
    print(lenOfRecords)