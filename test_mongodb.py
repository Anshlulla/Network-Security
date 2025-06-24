from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_CONNECTION_STRING")

client = MongoClient(uri)
print("Connected Successfully: ", client)