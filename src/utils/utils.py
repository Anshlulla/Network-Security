import re
import yaml
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import os
import sys
import numpy as np
import pickle
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from src.entity.artifact_entity import ClassificationMetricArtifact

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file_path)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            return yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_np_array(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
        logging.info("Saved numpy array as .npy file")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_np_array(file_path) -> np.array:
    if not os.path.exists(file_path):
        raise FileNotFoundError
    try:
        with open(file_path, "rb") as file:
            contents = np.load(file)
            return contents
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_pkl_file(file_path: str, obj: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj=obj, file=file)
        logging.info("Saved pickle object as .pkl file")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_pkl_file(file_path: str) -> object:
    if not os.path.exists(file_path):
        raise FileNotFoundError
    try:
        with open(file_path, "rb") as file:
            contents = pickle.load(file)
            return contents
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)
        model_accuracy = accuracy_score(y_true, y_pred)

        classification_score = ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision,
            recall_score=model_recall,
            accuracy_score=model_accuracy
        )

        return classification_score
    except Exception as e:
        raise NetworkSecurityException(e, sys)