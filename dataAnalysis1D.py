from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
import numpy as np
from predict import predict
from predict import normaliz
import requests
import json
from pytz import timezone

SEQ_LEN = 12
thresh = 0
decision = "/media/share/decision.txt"

def getClosePrice():
    json_response = requests.get(
        'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=1min&apikey=KNJDAJ4YK2G4EY82')
    response = json.loads(json_response.text)
    LastRefreshed = response['Meta Data']['4. Last Refreshed']
    ClosePrice = []
    for k, v in response['Time Series FX (1min)'].items():
        ClosePrice.append(v['4. close'])
    return LastRefreshed, ClosePrice

def main():
    df = pd.read_csv('EURUSD_12H.csv', delimiter=',', usecols=['Local time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    close = np.array(df['Close'])
    X = []
    for i in range(SEQ_LEN):
        X.append([close[i]])
    X = normaliz(X)
    prediction1 = predict(X)
    close = np.delete(close, 0)
    X = []
    for i in range(SEQ_LEN):
        X.append([close[i]])
    X = normaliz(X)
    prediction2 = predict(X)

    refresh, closePrice = getClosePrice()
    refreshEET = datetime.strptime(refresh, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone('UTC')).astimezone(
        timezone('Europe/Sofia'))
    currentTimeEET = datetime.now().astimezone(timezone('Europe/Sofia'))

    while(True):
        # Decision from threshold
        if(prediction2-prediction1 > thresh):
            f = open(decision, "w+")
            f.write("SELL")
            print("SELL")
            f.close()
        elif(prediction1-prediction2 > thresh):
            f = open(decision, "w+")
            f.write("BUY")
            print("BUY")
            f.close()
        else:
            f = open(decision, "w+")
            f.write("CLOSE")
            print("CLOSE")
            f.close()

        # No trades on weekends
        if (currentTimeEET.isoweekday() in set((0, 1))):
            monday = currentTimeEET + timedelta(days=2 - currentTimeEET.isoweekday())
            waitUntil = datetime(monday.year, monday.month, monday.day, 0, 0)
            time.sleep((waitUntil- currentTimeEET).seconds)

        # No data acquisition until next data
        else:
            nextRefresh = timedelta(days=1,hours=-refreshEET.hour,minutes=-refreshEET.minute,seconds=-refreshEET.second)
            print("Sleeping for: " + str(nextRefresh.seconds/3600) + " minutes")
            time.sleep(nextRefresh.seconds)

        # New prediction
        refreshNew, closePrice = getClosePrice()
        refreshNewEET = datetime.strptime(refresh, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone('UTC')).astimezone(timezone('Europe/Sofia'))
        while (refreshEET.day == refreshNewEET.day):
            print("No new data! Last refreshed: " + refresh + " New refresh: " + refreshNew)
            time.sleep(30)
            refreshNew, closePrice = getClosePrice()
            refreshNewEET = datetime.strptime(refresh, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone('UTC')).astimezone(timezone('Europe/Sofia'))
        refreshEET = refreshNewEET

        prediction1 = prediction2
        close = np.delete(close, 0)
        close = np.append(close, closePrice)
        X = []
        for i in range(SEQ_LEN):
            X.append([close[i]])
        X = normaliz(X)
        prediction2 = predict(X)

main()