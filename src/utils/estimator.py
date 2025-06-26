from platform import processor
from src.logging.logger import logging
from src.exception.exception import NetworkSecurityException
from src.constants.constants import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
import sys

class NetworkModel:
    def __init__(self, processor, model):
        self.processor = processor
        self.model = model

    def predict(self, x):
        x_transform = self.processor.transform(x)
        y_pred = self.model.predict(x_transform)
        return y_pred