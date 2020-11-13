#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 01:01:33 2020

@author: justin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

regressor_models = {}
dataset = pd.read_csv(r'/home/justin/Documents/Futures/data/autotrader/2020day_1m_regression.csv')
X = dataset.iloc[:, 1:-2].values
y = dataset.iloc[:, -2].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

##multiple-linear
start_time=time.time()
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
reg_score = r2_score(y_test, y_pred)
regressor_models['multi-variable-linear'] = reg_score
print('Multiple-linear Reg_score = ', reg_score)
take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')

#polynomial
start_time=time.time()
for a in range(2, 6, 1):
    poly_reg = PolynomialFeatures(degree = 2)
    X_poly = poly_reg.fit_transform(X_train)
    lin_reg_2 = LinearRegression()
    lin_reg_2.fit(X_poly, y_train)
    y_pred = lin_reg_2.predict(poly_reg.fit_transform(X_test))
    reg_score = r2_score(y_test, y_pred)
    regressor_models['poly_degree_'+str(a)] = reg_score
    print('Poly degree ', a, ' Reg_score = ', reg_score)
take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')

#SVR
start_time=time.time()
sc_X = StandardScaler()
sc_y = StandardScaler()
y_train_reshape = y_train.reshape(len(y_train),1)
X_trans = sc_X.fit_transform(X_train)
y_trans = sc_y.fit_transform(y_train_reshape)
regressor = SVR(kernel = 'rbf')
regressor.fit(X_trans, y_trans)
y_pred = sc_y.inverse_transform(regressor.predict(sc_X.transform(X_test)))
reg_score = r2_score(y_test, y_pred)
regressor_models['SVR'] = reg_score
print('SVR Reg_score = ', reg_score)
take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')

#Decision Tree
start_time=time.time()
regressor = DecisionTreeRegressor()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
reg_score = r2_score(y_test, y_pred)
regressor_models['Decision_Tree'] = reg_score
print('Decision Tree Reg_score = ', reg_score)
take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')

#Random Forest
start_time=time.time()
for b in range(10, 110, 10):
    regressor = RandomForestRegressor(n_estimators = b)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    reg_score = r2_score(y_test, y_pred)
    regressor_models['Random_forest_estimators_'+str(b)] = reg_score
    print('Random Trees ', b, ' Reg_score = ', reg_score)
take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')