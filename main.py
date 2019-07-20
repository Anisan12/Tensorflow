from sklearn.externals import joblib
import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.initializers import *
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json

SEQ_LEN = 3

df = pd.read_csv('data.csv',delimiter=',',usecols=['real','predict'])
predict = np.array(df['predict'])
test_data = np.array(df['real'])

profit1 = []
profit1Sum = []
profit2 = []
profit2Sum = []
profit3 = []
profit3Sum= []
step = np.linspace(0, 0.005, num=5000, endpoint=False)

for i in range(len(step)):
    temp1 = []
    temp2 = []
    temp3 = []
    for j in range(len(predict)):
        temp1.append(0)
        temp2.append(0)
        temp3.append(0)
    profit1.append(temp1)
    profit2.append(temp2)
    profit3.append(temp3)

for x in range(len(step)):
    for i in range(SEQ_LEN + 1, len(predict)):
        if (abs(predict[i] - predict[i-1]) > step[x]):
            if (predict[i] > predict[i-1]):
                profit1[x][i] = test_data[i] - test_data[i-1]
            else:
                profit1[x][i] = test_data[i-1] - test_data[i]

    for i in range(SEQ_LEN + 2, len(predict)):
        if (profit1[x][i] == 0):
            continue
        else:
            if (profit1[x][i] > 0 and profit1[x][i-1] > 0):
                profit2[x][i] = profit1[x][i]
            elif (profit1[x][i] < 0 and profit1[x][i-1] < 0):
                profit2[x][i] = profit1[x][i]

    for i in range(SEQ_LEN + 3, len(predict)):
        if (profit2[x][i] == 0):
            continue
        else:
            if (profit2[x][i] > 0 and profit2[x][i-1] > 0):
                profit3[x][i] = profit2[x][i]
            elif (profit2[x][i] < 0 and profit2[x][i-1] < 0):
                profit3[x][i] = profit2[x][i]

    profit1Sum.append(sum(profit1[x]))
    profit2Sum.append(sum(profit2[x]))
    profit3Sum.append(sum(profit3[x]))

plt.figure(figsize=(18, 9))
plt.plot(profit1Sum, color='black', label='profit1')
plt.plot(profit2Sum, color='green', label='profit2')
plt.plot(profit3Sum, color='red', label='profit3')
plt.title('Profit chart', fontsize=30)
# plt.xticks(range(0,df.shape[0],50),df['Date'].loc[::50],rotation=45)
plt.xlabel('Step')
plt.ylabel('Profit')
plt.legend(fontsize=18)
plt.show()

#X = [[1.23844],[1.23646],[1.23517],[1.23565],[1.23522],[1.23715],[1.23777],[1.23885],[1.23825],[1.23823],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002],[1.002]]
#
#df = pd.read_csv('EURUSD_H1_2005.csv',delimiter=',',usecols=['Date','Open','High','Low','Close', 'Volume'])
#
#times = sorted(df.index.values)  # get the times
#last_10pct = sorted(df.index.values)[-int(0.1 * len(times))]  # get the last 10% of the times
#test_df = df[(df.index >= last_10pct)]
#test_df.drop(columns=["Date", 'Open', 'High', 'Low', 'Volume'],
#             inplace=True)  # don't need this anymore.
#
#test_df_np = test_df['Close'].to_numpy()
#test_df_np = test_df_np.reshape(-1, 1)
#test_df['normid'] = normaliz(test_df_np)
#
#predictColumn = []
#for i in range(24):
#    predictColumn.append(0)
#
#for k in range(24, len(test_df)):
#    CurrentIndex = []
#    for i in range((k-24), k):
#        TempM = []
#        TempM.append(test_df.iloc[i][1])
#        CurrentIndex.append(TempM)
#    predictColumn.append(predict(CurrentIndex)[0])
#
#test_df.insert(2, "predict", predictColumn)
#test_df.to_csv(r'test_data.csv')

#x = [1,2,3,4,5,6]
#y = [1,3,5,8,3,1]
#plt.plot(x,y)
#plt.show()
