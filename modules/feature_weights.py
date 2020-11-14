import matplotlib.pyplot as plt
import datetime as datetime
import numpy as np
import pandas as pd
import talib
import seaborn as sns
from time import time
from sklearn import preprocessing
from pandas.plotting import register_matplotlib_converters
from .factorize import FactorManagement
import scipy.stats as stats
import cvxpy as cvx
import zipfile
import os
from sklearn import linear_model, decomposition, ensemble, preprocessing, isotonic, metrics
from sklearn.impute import SimpleImputer
import xgboost

register_matplotlib_converters()


class Learner:

    def __init__(self):
        pass

    @staticmethod
    def shift_mask_data(X, Y, upper_percentile, lower_percentile, n_fwd_days):
        # Shift X to match factors at t to returns at t+n_fwd_days (we want to predict future returns after all)
        shifted_X = np.roll(X, n_fwd_days + 1, axis=0)

        # Slice off rolled elements
        X = shifted_X[n_fwd_days + 1:]
        Y = Y[n_fwd_days + 1:]

        n_time, n_stocks, n_factors = X.shape

        # Look for biggest up and down movers
        upper = np.nanpercentile(Y, upper_percentile, axis=1)[:, np.newaxis]
        lower = np.nanpercentile(Y, lower_percentile, axis=1)[:, np.newaxis]

        upper_mask = (Y >= upper)
        lower_mask = (Y <= lower)

        mask = upper_mask | lower_mask  # This also drops nans
        mask = mask.flatten()

        # Only try to predict whether a stock moved up/down relative to other stocks
        Y_binary = np.zeros(n_time * n_stocks)
        Y_binary[upper_mask.flatten()] = 1
        Y_binary[lower_mask.flatten()] = -1

        # Flatten X
        X = X.reshape((n_time * n_stocks, n_factors))

        # Drop stocks that did not move much (i.e. are in the 30th to 70th percentile)
        X = X[mask]
        Y_binary = Y_binary[mask]

        return X, Y_binary

    def feature_importance_adaboost(self, n_fwd_days, close, all_factors, n_estimators, train_size,
                                    upper_percentile, lower_percentile):
        pipe = all_factors
        pipe.index = pipe.index.set_levels([pd.to_datetime(pipe.index.levels[0]), pipe.index.levels[1]])

        close = close[pipe.index.levels[1]]
        close.index = pd.to_datetime(close.index)

        chunk_start = pipe.index.levels[0][0]
        chunk_end = pipe.index.levels[0][-1]

        returns = FactorManagement().log_Returns(close, 1).loc[slice(chunk_start, chunk_end), :]
        returns_stacked = returns.stack().to_frame('Returns')

        results = pd.concat([pipe, returns_stacked], axis=1)
        results.index.set_names(['date', 'asset'], inplace=True)

        results_wo_returns = results.copy()
        returns = results_wo_returns.pop('Returns')
        Y = returns.unstack().values
        X = results_wo_returns.to_xarray().to_array()
        X = np.array(X)
        X = X.swapaxes(2, 0).swapaxes(0, 1)  # (factors, time, stocks) -> (time, stocks, factors)

        # Train-test split
        train_size_perc = train_size
        n_time, n_stocks, n_factors = X.shape
        train_size = np.int16(np.round(train_size_perc * n_time))
        X_train, Y_train = X[:train_size], Y[:train_size]
        X_test, Y_test = X[(train_size + n_fwd_days):], Y[(train_size + n_fwd_days):]

        X_train_shift, Y_train_shift = self.shift_mask_data(X_train, Y_train, n_fwd_days=n_fwd_days,
                                                            lower_percentile=lower_percentile,
                                                            upper_percentile=upper_percentile)

        X_test_shift, Y_test_shift = self.shift_mask_data(X_test, Y_test, n_fwd_days=n_fwd_days,
                                                          lower_percentile=lower_percentile,
                                                          upper_percentile=upper_percentile)

        start_timer = time()

        # Train classifier
        imputer = SimpleImputer()
        scaler = preprocessing.MinMaxScaler()
        clf = ensemble.AdaBoostClassifier(
            n_estimators=n_estimators)  # n_estimators controls how many weak classifiers are fi

        X_train_trans = imputer.fit_transform(X_train_shift)
        X_train_trans = scaler.fit_transform(X_train_trans)
        clf.fit(X_train_trans, Y_train_shift)

        end_timer = time()
        print('Time to train full ML pipline: {} secs'.format(end_timer - start_timer))

        Y_pred = clf.predict(X_train_trans)
        print('Accuracy on train set = {:.2f}%'.format(metrics.accuracy_score(Y_train_shift, Y_pred) * 100))

        # Transform test data
        X_test_trans = imputer.transform(X_test_shift)
        X_test_trans = scaler.transform(X_test_trans)

        # Predict!
        Y_pred = clf.predict(X_test_trans)
        Y_pred_prob = clf.predict_proba(X_test_trans)

        print('Predictions:', Y_pred)
        print('Probabilities of class == 1:', Y_pred_prob[:, 1] * 100)
        print('Accuracy on test set = {:.2f}%'.format(metrics.accuracy_score(Y_test_shift, Y_pred) * 100))
        print('Log-loss = {:.5f}'.format(metrics.log_loss(Y_test_shift, Y_pred_prob)))

        feature_importances = pd.Series(clf.feature_importances_, index=results_wo_returns.columns)
        feature_importances.sort_values(ascending=False)
        ax = feature_importances.plot(kind='bar')
        ax.set(ylabel='Importance (Gini Coefficient)', title='Feature importances')

        feature_importances = pd.DataFrame(data=feature_importances.values,
                                           columns=['weights'],
                                           index=feature_importances.index)
        feature_importances.index.name = 'factors'

        return feature_importances

    def feature_importance_xgb(self, n_fwd_days, close, all_factors, n_estimators, train_size,
                               upper_percentile, lower_percentile):
        pipe = all_factors
        pipe.index = pipe.index.set_levels([pd.to_datetime(pipe.index.levels[0]), pipe.index.levels[1]])

        close = close[pipe.index.levels[1]]
        close.index = pd.to_datetime(close.index)

        chunk_start = pipe.index.levels[0][0]
        chunk_end = pipe.index.levels[0][-1]

        returns = FactorManagement().log_Returns(close, 1).loc[slice(chunk_start, chunk_end), :]
        returns_stacked = returns.stack().to_frame('Returns')

        results = pd.concat([pipe, returns_stacked], axis=1)
        results.index.set_names(['date', 'asset'], inplace=True)

        results_wo_returns = results.copy()
        returns = results_wo_returns.pop('Returns')
        Y = returns.unstack().values
        X = results_wo_returns.to_xarray().to_array()
        X = np.array(X)
        X = X.swapaxes(2, 0).swapaxes(0, 1)

        # Train-test split
        train_size_perc = train_size
        n_time, n_stocks, n_factors = X.shape
        train_size = np.int16(np.round(train_size_perc * n_time))
        X_train, Y_train = X[:train_size], Y[:train_size]
        X_test, Y_test = X[(train_size + n_fwd_days):], Y[(train_size + n_fwd_days):]

        X_train_shift, Y_train_shift = self.shift_mask_data(X_train, Y_train, n_fwd_days=n_fwd_days,
                                                            lower_percentile=lower_percentile,
                                                            upper_percentile=upper_percentile)

        X_test_shift, Y_test_shift = self.shift_mask_data(X_test, Y_test, n_fwd_days=n_fwd_days,
                                                          lower_percentile=lower_percentile,
                                                          upper_percentile=upper_percentile)

        start_timer = time()

        # Train classifier
        # imputer = SimpleImputer()
        # scaler = preprocessing.MinMaxScaler()
        clf = xgboost.XGBClassifier(n_estimators=n_estimators)

        # X_train_trans = imputer.fit_transform(X_train_shift)
        # X_train_trans = scaler.fit_transform(X_train_trans)
        clf.fit(X_train_shift, Y_train_shift)

        end_timer = time()
        print('Time to train full ML pipline: {} secs'.format(end_timer - start_timer))

        Y_pred_train = clf.predict(X_train_shift)
        print('Accuracy on train set = {:.2f}%'.format(metrics.accuracy_score(Y_train_shift, Y_pred_train) * 100))

        # Transform test data
        # X_test_trans = imputer.transform(X_test_shift)
        # X_test_trans = scaler.transform(X_test_trans)

        # Predict!
        Y_pred = clf.predict(X_test_shift)
        Y_pred_prob = clf.predict_proba(X_test_shift)

        print('Predictions:', Y_pred)
        print('Probabilities of class == 1:', Y_pred_prob[:, 1] * 100)
        print('Accuracy on test set = {:.2f}%'.format(metrics.accuracy_score(Y_test_shift, Y_pred) * 100))
        print('Log-loss = {:.5f}'.format(metrics.log_loss(Y_test_shift, Y_pred_prob)))

        feature_importances = pd.Series(clf.feature_importances_, index=results_wo_returns.columns)
        feature_importances.sort_values(ascending=False)
        ax = feature_importances.plot(kind='bar')
        ax.set(ylabel='Importance (Gini Coefficient)', title='Feature importances')

        feature_importances = pd.DataFrame(data=feature_importances.values,
                                           columns=['weights'],
                                           index=feature_importances.index)
        feature_importances.index.name = 'factors'

        return feature_importances
