import os
import sys
from tkinter import NE
import pandas as pd
from dotenv import load_dotenv
import pymongo
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline
from src.constants.constants import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from src.utils.estimator import NetworkModel
from src.utils.utils import load_pkl_file
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
templates = Jinja2Templates(directory="./templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.get("/predict")
async def predict(request: Request, file: UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_pkl_file("final_model/preprocessor.pkl")
        model = load_pkl_file("final_model/model.pkl")
        network_model = NetworkModel(preprocessor, model)
        y_pred = network_model.predict(df)
        df["predictions"] = y_pred
        table_html = df.to_html(classes='table table-striped')
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)