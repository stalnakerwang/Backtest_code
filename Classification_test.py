#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:56:38 2020

@author: justin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


#import dataset
dataset = pd.read_csv('DATA_NAME_FILE_HERE.csv')

#checking in all model scores
classification_models = {}

#Setting split of train test size
test_size = 0.25

#split X, Y, test, train set
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

#Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

start_time=time.time()
#Logsitic regression classifier
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
#predicting 
y_pred = classifier.predict(X_test)
#creating confusion maxtriz
cm = confusion_matrix(y_test, y_pred)
print('Logistic regression')
print(cm)
acc_score = accuracy_score(y_test, y_pred)
classification_models['logsitic_regression_classifier'] = acc_score

take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')

#KNN classifier
for a in range (5, 20, 5):
    start_time=time.time()
    classifier = KNeighborsClassifier(n_neighbors = a, metric = 'minkowski', p = 2)
    classifier.fit(X_train, y_train)
#predicting 
    y_pred = classifier.predict(X_test)
#creating confusion maxtriz
    cm = confusion_matrix(y_test, y_pred)
    print('KNN classifier_',str(a),'_n_neighbors')
    print(cm)
    acc_score = accuracy_score(y_test, y_pred)
    classification_models['KNN_classifier_'+str(a)+'_neighbors'] = acc_score

    take_time=time.time()-start_time
    print('Total Time:', round(take_time, 4), 'seconds')

#SVM classifier
kernel_style = ['linear', 'poly', 'rbf', 'sigmoid']
for b in kernel_style:
    start_time=time.time()
    classifier = SVC(kernel = b)
    classifier.fit(X_train, y_train)
#predicting 
    y_pred = classifier.predict(X_test)
#creating confusion maxtriz
    cm = confusion_matrix(y_test, y_pred)
    print('SVM classifier_',str(b),'_style')
    print(cm)
    acc_score = accuracy_score(y_test, y_pred)
    classification_models['SVM_'+b+'_style'] = acc_score

    take_time=time.time()-start_time
    print('Total Time:', round(take_time, 4), 'seconds')

start_time=time.time()
#Naive Bayes classifier
classifier = GaussianNB()
classifier.fit(X_train, y_train)
#predicting 
y_pred = classifier.predict(X_test)
#creating confusion maxtriz
cm = confusion_matrix(y_test, y_pred)
print('Naive Bayes classifier')
print(cm)
acc_score = accuracy_score(y_test, y_pred)
classification_models['Naive_Bayes_classifier'] = acc_score

take_time=time.time()-start_time
print('Total Time:', round(take_time, 4), 'seconds')


#Decision tree classifier
dtc_style = ['gini', 'entropy']
for c in dtc_style:
    start_time=time.time()
    classifier = DecisionTreeClassifier(criterion = 'entropy')
    classifier.fit(X_train, y_train)
#predicting 
    y_pred = classifier.predict(X_test)
#creating confusion maxtriz
    cm = confusion_matrix(y_test, y_pred)
    print('Decision tree classifier_',str(c),'_style')
    print(cm)
    acc_score = accuracy_score(y_test, y_pred)
    classification_models['Decision_tree_'+c+'_style'] = acc_score

    take_time=time.time()-start_time
    print('Total Time:', round(take_time, 4), 'seconds')

#Random Forest classifier
for c in dtc_style:
    for d in range (10, 110, 10):
        start_time=time.time()
        classifier = RandomForestClassifier(n_estimators = d, criterion = c)
        classifier.fit(X_train, y_train)
#predicting 
        y_pred = classifier.predict(X_test)
#creating confusion maxtriz
        cm = confusion_matrix(y_test, y_pred)
        print('Random forest classifier_',str(c),'_style_',str(d),'_estimators')
        print(cm)
        acc_score = accuracy_score(y_test, y_pred)
        classification_models['Random_forest_'+c+'_style_'+str(d)+'_trees'] = acc_score
    
        take_time=time.time()-start_time
        print('Total Time:', round(take_time, 4), 'seconds')
