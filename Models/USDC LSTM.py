import pandas as pd
import datetime

# Load Dataset
df = pd.read_csv('C:/Users/hanzhiyang/Downloads/290 New Data/USDC Price.csv')
df = df.set_index('Date')
df = df.asfreq('D')


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# Overview Plot of the Time Series Data
plt.rcParams['figure.figsize'] = (10,6)
df['USDC Price'] = df['USDC Price'].astype('float64')
plt.plot(df['USDC Price'])
plt.ylim([0.9, 1.1])
plt.xlabel('Date')
plt.ylabel('USDC Price')
plt.grid()
plt.show()



import math
import timeit
import graphviz
import pydot
import pydotplus
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.losses import MeanAbsolutePercentageError
from tensorflow.keras.utils import plot_model
from sklearn.preprocessing import MinMaxScaler

start = timeit.default_timer()

# Start Building the LSTM Model
def create_dataset(df, look_back = 1):
  dataX, dataY = [], []
  for i in range(len(df) - look_back - 1):
    a = df[i:(i+look_back), 0]
    dataX.append(a)
    dataY.append(df[i+look_back, 0])
  return np.array(dataX), np.array(dataY)

df = df.values.astype('float32')
scaler = MinMaxScaler(feature_range=(0,1))
df = scaler.fit_transform(df)
train_size = int(len(df) * 0.7)
test_size = len(df) - train_size
train, test = df[0:train_size,:], df[train_size:len(df),:]
print(len(train), len(test))

look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
trainX = np.reshape(trainX, (trainX.shape[0], look_back, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], look_back, testX.shape[1]))
print(len(trainX), len(testX))

# Add Layers to the Model
model = Sequential()
model.add(LSTM(50, input_shape=(trainX.shape[1], trainX.shape[2])))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
model.fit(trainX, trainY, epochs = 50, batch_size= 1, verbose= 2)

# Output the Architecture Graph
plot_model(model, to_file='C:/Users/hanzhiyang/Downloads/LSTMplot.png' ,show_shapes=True)

stop = timeit.default_timer()
print('Time1:', stop - start)

start = timeit.default_timer()

# Predictions
trainpred = model.predict(trainX)
testpred = model.predict(testX)
trainpred = scaler.inverse_transform(trainpred)
trainY = scaler.inverse_transform([trainY])
testpred = scaler.inverse_transform(testpred)
testY = scaler.inverse_transform([testY])

# Check MAPE Errors
mape = MeanAbsolutePercentageError()
train_score = mape(trainY[0], trainpred[:,0]).numpy()
print('Train Score: %.2f MAPE' % (train_score))
test_score = mape(testY[0], testpred[:,0]).numpy()
print('Test Score: %.2f MAPE' % (test_score))

# Plot the Graph that Shows the Comparison between True Values and Predicted Values
print(len(trainpred))
trainPredictPlot = np.empty_like(df)
trainPredictPlot[:,:] = np.nan
trainPredictPlot[look_back:len(trainpred)+look_back, :] = trainpred
testPredictPlot = np.empty_like(df)
testPredictPlot[:,:] = np.nan
print(len(trainpred)+(look_back*2)+1, len(df)-1)
testPredictPlot[len(trainpred)+(look_back*2)+1:len(df)-1, :] = testpred

stop = timeit.default_timer()
print('Time2:', stop - start)

plt.plot(scaler.inverse_transform(df), color = 'blue', alpha = 0.5)
plt.plot(testPredictPlot, color = 'red')
plt.ylim([0.9, 1.1])
plt.xlabel('Date')
plt.ylabel('USDC Price')
plt.grid()
plt.show()