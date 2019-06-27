#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 16:45:59 2019

@author: gabrielpundrich
"""
#Code adapted from https://www.analyticsvidhya.com/blog/2018/10/predicting-stock-price-machine-learningnd-deep-learning-techniques-python/


def add_datepart(df, fldname, drop=True, time=False, errors="raise"):	
    """add_datepart converts a column of df from a datetime64 to many columns containing
    the information from the date. This applies changes inplace.
    Parameters:
    -----------
    df: A pandas data frame. df gain several new columns.
    fldname: A string that is the name of the date column you wish to expand.
        If it is not a datetime64 series, it will be converted to one with pd.to_datetime.
    drop: If true then the original date column will be removed.
    time: If true time features: Hour, Minute, Second will be added.
    Examples:
    ---------
    >>> df = pd.DataFrame({ 'A' : pd.to_datetime(['3/11/2000', '3/12/2000', '3/13/2000'], infer_datetime_format=False) })
    >>> df
        A
    0   2000-03-11
    1   2000-03-12
    2   2000-03-13
    >>> add_datepart(df, 'A')
    >>> df
        AYear AMonth AWeek ADay ADayofweek ADayofyear AIs_month_end AIs_month_start AIs_quarter_end AIs_quarter_start AIs_year_end AIs_year_start AElapsed
    0   2000  3      10    11   5          71         False         False           False           False             False        False          952732800
    1   2000  3      10    12   6          72         False         False           False           False             False        False          952819200
    2   2000  3      11    13   0          73         False         False           False           False             False        False          952905600
    """
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64

    if not np.issubdtype(fld_dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True, errors=errors)
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)




path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
base_dir = path_env + "/ML/LTSM/"


#import packages
import re
import pandas as pd
import numpy as np
import sys
#to plot within notebook
import matplotlib.pyplot as plt
%matplotlib inline

#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

#for normalizing data
from sklearn.preprocessing import MinMaxScaler

#importing required libraries
from sklearn.preprocessing import MinMaxScaler
#install("tensorflow")
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM



#read the input file
df = pd.read_csv(base_dir+'NSE-TATAGLOBAL.csv')

#print the head
df.head()

#setting index as date
df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df.index = df['Date']

#plot
plt.figure(figsize=(16,8))
plt.plot(df['Close'], label='Close Price history')




#Long Short Term Memory (LSTM)



#creating dataframe
data = df.sort_index(ascending=True, axis=0)

#create dataframe only using only close and date 
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]

#setting index
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)

#creating train and test sets (keep just price values)
dataset = new_data.values

#train data only 987 days
train = dataset[0:987,:]

#test data using the remaining 248 days
valid = dataset[987:,:]


#set up the scale as range 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

#compare
scaled_data
dataset


x_train, y_train = [], []

#predict the data using the lagged 60 days price
for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])

#transform into an array type to have access to all functions of an array
x_train, y_train = np.array(x_train), np.array(y_train)

#numpy.reshape(a, newshape, order)
#It will reshape the data from a 2-D to a 3-D with 1 feature to fit into the LTSM parameter
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# create and fit the LSTM network
model = Sequential()



"""
units=50: number of neurons or nodes that we want in the layer
return_sequences=True, which is set to true since we will add more layers to the model
input_shape=60: number of time steps while the last parameter is the number of indicators.
"""
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))

#add a new layer with more 50 neurons
model.add(LSTM(units=50))

#last layer added to the model equal to 1 (as we want a single output)
model.add(Dense(1))

"""
Model Compilation
Here we compile our LSTM before we can train it on the training data. 

We use the mean squared error as loss function and to reduce the loss or 
to optimize the algorithm, we use the adam optimizer.
"""
model.compile(loss='mean_squared_error', optimizer='adam')

"""

Model training

One Epoch is when an ENTIRE dataset is passed forward and backward through the 
neural network only ONCE.
Since one epoch is too big to feed to the computer at once we divide it in several smaller batches.

By setting verbose 0, 1 or 2 you just say how do you want to 'see' the training progress for each epoch.

verbose=0 will show you nothing (silent)

verbose=1 will show you an animated progress bar like:

progres_bar

verbose=2 will just mention the number of epoch like this:
"""
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=1)


#predicting 246 values, using past 60 from the train data
inputs = new_data[len(new_data) - len(valid) - 60:].values
inputs = inputs.reshape(-1,1)

#transform the inputs into the same scale
inputs  = scaler.transform(inputs)

X_test = []
#i from 60 till 308 (248+60)
#Input has one column and 308 rows. We create X_test with 248 ROWS and 60 columns
for i in range(60,inputs.shape[0]):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)

#reshape 3d to fit LTSM
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)


"""
The RMSE is the square root of the variance of the residuals. 
It indicates the absolute fit of the model to the data–how close the observed
data points are to the model’s predicted values. Whereas
"""
rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
rms




#for plotting
train = new_data[:987]
valid = new_data[987:]
valid['Predictions'] = closing_price
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])


valid.to_csv(base_dir + 'valid.csv')




