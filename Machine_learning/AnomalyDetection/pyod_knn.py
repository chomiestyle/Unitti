# -*- coding: utf-8 -*-
"""Example of using kNN for outlier detection
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

import os
import sys

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from pyod.models.knn import KNN
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize
import pandas as pd
from sklearn.model_selection import train_test_split



from datetime import datetime
#
# timestamp = 1545730073
# dt_object = datetime.fromtimestamp(timestamp)
# print(dt_object)
def get_data(filename, cols=None):
    data=pd.read_csv(filename)
    #print(data['Time'])
    #data['Time']=data['Time'].apply(lambda x: datetime.fromtimestamp(x/1000))

    if cols!=None:
        new_data=data[['Time']+cols]
    else:
        new_data=data[data.columns[1:]]

    print(len(new_data.columns))
    for i in new_data.columns:
        print(i)
    new_data.set_index("Time", inplace=True)
    new_data=new_data.loc[(new_data!=0).any(axis=1)]
    #new_data= new_data[(new_data.T != 0).any()]
    new_data=new_data.dropna()
    #new_data
    print(new_data)
    new_data.to_csv('C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/prueba_metricas3.csv', index=True)

    # selected_data=data[col].dropna(inplace=False)
    # train, test = train_test_split(selected_data, test_size=0.2, shuffle=False)
    # #print(train)
    #
    # return train.values,test.values




def knn(X_train,y_train=None,X_test=None, y_test=None):
    # train kNN detector
    clf_name = 'KNN'
    clf = KNN()
    clf.fit(X_train)

    # get the prediction labels and outlier scores of the training data
    y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
    y_train_scores = clf.decision_scores_  # raw outlier scores
    # # get the prediction on the test data
    y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
    y_test_scores = clf.decision_function(X_test)  # outlier scores


    #
    # # evaluate and print the results
    # print("\nOn Training Data:")
    # evaluate_print(clf_name, y_train, y_train_scores)
    # print("\nOn Test Data:")
    # evaluate_print(clf_name, y_test, y_test_scores)
    #
    # visualize the results
    visualize(clf_name, X_train, X_test, y_train_pred,y_test_pred, show_figure=True, save_figure=False)

    return y_train_pred, y_train_scores



filename='C:/Users/56979/PycharmProjects/Unitti/Monitoring/Datadog/data/Datadog_20_25.csv'
postgresql_columns={'conn':['postgresql.connections','postgresql.percent_usage_connections'],
                    'row':['postgresql.rows_updated','postgresql.rows_returned','postgresql.rows_inserted','postgresql.rows_fetched','postgresql.rows_deleted'],
                    'temp_files':['postgresql.temp_bytes','postgresql.temp_files'],
                    'commit':['postgresql.commits']}

trace_columns={'resource_service':['trace.django.request.duration.by.resource_service.100p','trace.django.request.duration.by.resource_service.99p','trace.django.request.duration.by.resource_service.75p'],
               'service':['trace.django.template.render.duration.by.service.99p','trace.django.template.render.duration.by.service.75p']}


system_columns={'cpu':['system.cpu.idle','system.cpu.guest','system.cpu.context_switches','system.cpu.iowait','system.cpu.num_cores'],
                'disk':['system.disk.free','system.disk.in_use','system.disk.write_time_pct']}


def main():
    get_data(filename,postgresql_columns['temp_files'])
    X_train,X_test=get_data(filename=filename,cols=postgresql_columns['temp_files']+postgresql_columns['conn']+postgresql_columns['row']+postgresql_columns['commit'])
    pred,score=knn(X_train=X_train,X_test=X_test)
    print(len(pred))
    print(len(score))

get_data(filename=filename,cols=postgresql_columns['temp_files']+postgresql_columns['conn']+postgresql_columns['row']+postgresql_columns['commit'])