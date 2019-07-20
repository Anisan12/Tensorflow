from datetime import datetime
from datetime import timedelta
import time
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.initializers import *
from predict import predict
from predict import normaliz
import requests
import json
import sys

# Profit2
SEQ_LEN = 3
thresh = 0.000367

def getClosePrice():
    json_response = requests.get(
        'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=60min&apikey=KNJDAJ4YK2G4EY82')
    response = json.loads(json_response.text)
    LastRefreshed = response['Meta Data']['4. Last Refreshed']
    ClosePrice = []
    for k, v in response['Time Series FX (60min)'].items():
        ClosePrice.append(v['4. close'])
    return LastRefreshed, ClosePrice

def main():
    predictions = []

    # Before Last prediction
    refresh, close = getClosePrice()
    X = []
    for i in range(SEQ_LEN):
        X.append([close[i]])
    X = normaliz(X)
    predictions.append(predict(X))
    X = []
    for i in range(1,SEQ_LEN+1):
        X.append([close[i]])
    X = normaliz(X)
    predictions.append(predict(X))
    X = []
    for i in range(2,SEQ_LEN+2):
        X.append([close[i]])
    X = normaliz(X)
    predictions.append(predict(X))

    while(True):
        # Decision from threshold
        if(predictions[0]-predictions[1] > thresh and predictions[1]-predictions[2] > thresh):
            f = open("decision.txt", "w+")
            f.write("BUY")
            f.close()
        elif(predictions[1]-predictions[0] > thresh and predictions[2]-predictions[1] > thresh):
            f = open("decision.txt", "w+")
            f.write("SELL")
            f.close()
        else:
            f = open("decision.txt", "w+")
            f.write("CLOSE")
            f.close()

        refresh, close = getClosePrice()
        refreshTime = datetime.strptime(refresh, '%Y-%m-%d %H:%M:%S')
        currentTime = datetime.now()

        # No trades on weekends
        if (currentTime.weekday() in set((4, 5)) and currentTime.hour >= 17):
            sunday = currentTime + timedelta(days=6 - currentTime.weekday())
            waitUntil = datetime(sunday.year, sunday.month, sunday.day, 16, 59)
            time.sleep((waitUntil- currentTime).seconds)

        # No data acquisition until next data
        nextRefresh = timedelta(hours=(refreshTime.hour+1)-refreshTime.hour,minutes=refreshTime.minute - currentTime.minute,seconds=refreshTime.second-currentTime.second)
        time.sleep(nextRefresh.seconds)

        # New prediction
        predictions[2] = predictions[1]
        predictions[1] = predictions[0]
        refresh, close = getClosePrice()
        X = []
        for i in range(SEQ_LEN):
            X.append([close[i]])
        X = normaliz(X)
        predictions[0] = predict(X)

main()
#main(sys.argv[1])