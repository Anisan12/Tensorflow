from datetime import datetime
from datetime import timedelta
import requests
import json
import time

def getClosePrice():
    json_response = requests.get(
        'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=60min&apikey=KNJDAJ4YK2G4EY82')
    response = json.loads(json_response.text)
    LastRefreshed = response['Meta Data']['4. Last Refreshed']
    ClosePrice = []
    for k, v in response['Time Series FX (60min)'].items():
        ClosePrice.append(v['4. close'])
    return LastRefreshed, ClosePrice

currentTime = datetime.now()
refresh, close = getClosePrice()
refreshTime = datetime.strptime(refresh, '%Y-%m-%d %H:%M:%S')
print(timedelta(hours=(refreshTime.hour+1)-refreshTime.hour,minutes=refreshTime.minute - currentTime.minute,seconds=refreshTime.second-currentTime.second))