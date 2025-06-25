import yaml
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import os
import sys
import numpy as np
import pickle

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

def save_pkl_file(file_path: str, obj: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj=obj, file=file)
        logging.info("Saved pickle object as .pkl file")
    except Exception as e:
        raise NetworkSecurityException(e, sys)