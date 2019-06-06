#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:22:35 2019

@author: gabrielpundrich
"""
import pandas as pd

from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"

path_env = path_env+"/ML/LTSM_Multivariate/"


# convert series to supervised learning
# specify the number of lag hours
n_lags_used = 1
n_variables = 7

n_train_lags_used = 987



n_features = n_variables 


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# load dataset
dataset = read_csv(path_env+'pollution.csv', header=0, index_col=0)
values = dataset.values

#CATEGORICAL VARIABLE##########################################################
# integer encode direction (as it is a categorical variable in the 4th column with the direction of the wind - give a number to each category)
#encoder = LabelEncoder()
#values[:,4] = encoder.fit_transform(values[:,4])

# ensure all data is float
values = values.astype('float32')

# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)


# frame as supervised learning (using 3 hours as input) (basically creates three lags)
reframed = series_to_supervised(scaled, n_lags_used, 1)
print(reframed.shape)

# split into train and test sets
values = reframed.values

train = values[:n_train_lags_used, :]
test = values[n_train_lags_used:, :]

# split into input and outputs: n_features is pretty much number of vars
n_obs = n_lags_used * n_features


#set up X and Y
train_X, train_y = train[:, :n_obs], train[:, -n_features]


# define X variable(s): train[:, :n_obs]
# define Y variable: train[:, -n_features]

#DataFrame(train).to_csv(path_env+'1.csv')
#DataFrame(train[:, :n_obs]).to_csv(path_env+'2.csv')
#DataFrame(train[:, -n_features]).to_csv(path_env+'3.csv')



test_X, test_y = test[:, :n_obs], test[:, -n_features]
print(train_X.shape, len(train_X), train_y.shape)

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_lags_used, n_features))
test_X = test_X.reshape((test_X.shape[0], n_lags_used, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)



# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)

# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_lags_used*n_features))

# invert scaling for forecast
inv_yhat = concatenate((yhat, test_X[:, -(n_features-1):]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -(n_features-1):]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]


# calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)



inv_y
index_test = dataset.index

Data = {'Actual': inv_y, 'Predicted': inv_yhat , 'Dates': index_test[n_train_lags_used+n_lags_used:]}
df = DataFrame(Data)
df.to_csv(path_env+'output.csv')







