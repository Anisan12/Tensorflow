from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.initializers import *
import pandas as pd

# https://finance.yahoo.com/quote/GE/history?p=GE&.tsrc=fin-srch
df = pd.read_csv('EURUSD_H1_2005.csv', delimiter=',',
                 usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

times = sorted(df.index.values)  # get the times
last_20pct = sorted(df.index.values)[-int(0.2 * len(times))]  # get the last 20% of the times
train_df = df[(df.index < last_20pct)]  # now the train_df is all the data up to the last 20%
train_df.drop(columns=["Date", 'Open', 'High', 'Low', 'Volume'], inplace=True)
train_data = train_df['Close'].as_matrix()
train_data = train_data.reshape(-1, 1)

scaler = MinMaxScaler()

# Train the Scaler with training data and smooth data
smoothing_window_size = 2500
for di in range(0, 10000, smoothing_window_size):
    scaler.fit(train_data[di:di + smoothing_window_size, :])
    train_data[di:di + smoothing_window_size, :] = scaler.transform(train_data[di:di + smoothing_window_size, :])

# You normalize the last bit of remaining data
scaler.fit(train_data[di + smoothing_window_size:, :])

scaler_filename = "trainScaler.pkl"
joblib.dump(scaler, scaler_filename)