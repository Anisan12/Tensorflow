from sklearn.externals import joblib
import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.initializers import *
import requests
import json

def normaliz(X):
    scaler = joblib.load('trainScaler.pkl')
    X = scaler.transform(X)
    return X

def predict(X):
    X = np.expand_dims(X, axis=0)
    data = json.dumps({"instances": X.tolist()})

    headers = {"content-type": "application/json"}
    json_response = requests.post('http://192.168.1.79:8501/v1/models/eurusd1:predict', data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions[0][0]