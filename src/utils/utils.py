import yaml
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import os
import sys
import numpy as np
import pickle
import dill

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