# -*- coding: utf-8 -*-
"""Example of using Median Absolute Deviation (MAD) for outliers Detection.
"""
# Author: Yahya Almardeny <almardeny@gmail.com>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

import os
import sys
import numpy as np

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))
#from pyod.models.vae import VAE
from pyod.models.abod import ABOD
from pyod.models.auto_encoder import AutoEncoder
from pyod.models.mad import MAD
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize

def data(type,contamination):
    if type=='MAD':
        #contamination = 0.1  # percentage of outliers
        n_train = 200  # number of training points
        n_test = 100  # number of testing points

        # Generate sample data
        X_train, y_train, X_test, y_test = generate_data(n_train=n_train,
                                                     n_test=n_test,
                                                     n_features=1,
                                                     contamination=contamination,
                                                     random_state=42)
    elif type=='ABOD':
        contamination = 0.1  # percentage of outliers
        n_train = 200  # number of training points
        n_test = 100  # number of testing points

        # Generate sample data
        X_train, y_train, X_test, y_test = \
            generate_data(n_train=n_train,
                          n_test=n_test,
                          n_features=2,
                          contamination=contamination,
                          random_state=42)

    elif type=='AutoEncoder':
        #contamination = 0.1  # percentage of outliers
        n_train = 20000  # number of training points
        n_test = 2000  # number of testing points
        n_features = 300  # number of features

        # Generate sample data
        X_train, y_train, X_test, y_test = \
            generate_data(n_train=n_train,
                          n_test=n_test,
                          n_features=n_features,
                          contamination=contamination,
                          random_state=42)

    return X_train,y_train,X_test,y_test

def pyod_anomaly_detection(type,contamination):
    X_train, y_train, X_test, y_test=data(type=type,contamination=contamination)
    if type=='MAD':
        # train MAD detector
        clf_name = 'MAD'
        clf = MAD(threshold=3.5)
        clf.fit(X_train)

        # get the prediction labels and outlier scores of the training data
        y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
        y_train_scores = clf.decision_scores_  # raw outlier scores

        # get the prediction on the test data
        y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
        y_test_scores = clf.decision_function(X_test)  # outlier scores
        # evaluate and print the results
        print("\nOn Training Data:")
        evaluate_print(clf_name, y_train, y_train_scores)
        print("\nOn Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        # visualize the results
        # making dimensions = 2 for visualising purpose only. By repeating same data each dimension.
        visualize(clf_name, np.hstack((X_train, X_train)), y_train, np.hstack((X_test, X_test)), y_test, y_train_pred,
                  y_test_pred, show_figure=True, save_figure=False)
    elif type=='ABOD':
        # train ABOD detector
        clf_name = 'ABOD'
        clf = ABOD()
        clf.fit(X_train)

        # get the prediction labels and outlier scores of the training data
        y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
        y_train_scores = clf.decision_scores_  # raw outlier scores

        # get the prediction on the test data
        y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
        y_test_scores = clf.decision_function(X_test)  # outlier scores

        # evaluate and print the results
        print("\nOn Training Data:")
        evaluate_print(clf_name, y_train, y_train_scores)
        print("\nOn Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        # visualize the results
        visualize(clf_name, X_train, y_train, X_test, y_test, y_train_pred,
                  y_test_pred, show_figure=True, save_figure=False)
    elif type=='AutoEncoder':
        # train AutoEncoder detector
        clf_name = 'AutoEncoder'
        clf = AutoEncoder(epochs=30, contamination=contamination)
        clf.fit(X_train)

        # get the prediction labels and outlier scores of the training data
        y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
        y_train_scores = clf.decision_scores_  # raw outlier scores

        # get the prediction on the test data
        y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
        y_test_scores = clf.decision_function(X_test)  # outlier scores

        # evaluate and print the results
        print("\nOn Training Data:")
        evaluate_print(clf_name, y_train, y_train_scores)
        print("\nOn Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)
    # elif type=='VAE':
    #     # train VAE detector (Beta-VAE)
    #     clf_name = 'VAE'
    #     clf = VAE(epochs=30, contamination=contamination, gamma=0.8, capacity=0.2)
    #     clf.fit(X_train)
    #
    #     # get the prediction labels and outlier scores of the training data
    #     y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
    #     y_train_scores = clf.decision_scores_  # raw outlier scores
    #
    #     # get the prediction on the test data
    #     y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
    #     y_test_scores = clf.decision_function(X_test)  # outlier scores
    #     # evaluate and print the results
    #     print("\nOn Training Data:")
    #     evaluate_print(clf_name, y_train, y_train_scores)
    #     print("\nOn Test Data:")
    #     evaluate_print(clf_name, y_test, y_test_scores)



pyod_anomaly_detection('AutoEncoder',0.1)