from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import sys

def evaluate_models(X_train, y_train, X_test, y_test, models, params) -> dict:
    try:
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param_grid = params[list(models.keys())[i]]
            print(model, param_grid)

            gs = GridSearchCV(model, param_grid, cv=2)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            report[list(models.keys())[i]] = r2_score(y_test, y_pred)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    return report