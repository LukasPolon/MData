from sklearn import linear_model
from numpy import array
from copy import deepcopy
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn

from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from mdata.drivers.config.config_management import ConfigManagement


class Regression(object):
    def __init__(self):
        self.data = None
        self.conf = ConfigManagement()
        self._reg_methods = None
        self._reg_data_types = None

    @property
    def regression_methods(self):
        if self._reg_methods is None:
            reg_methods = {'linear': self.linear}
            self._reg_methods = reg_methods
        return self._reg_methods

    @property
    def regression_data_types(self):
        if self._reg_data_types is None:
            data_types = ['Open', 'Close', 'High', 'Low',
                          'Adj Close', 'Volume']
            self._reg_data_types = data_types
        return self._reg_data_types

    def get_data(self, data):
        self.data = data

    def get_split_rate(self):
        data = self.conf.get_data()
        return data['split_rate']

    def get_data_type(self):
        data = self.conf.get_data()
        return data['data_type']

    def linear_regression(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        volume = data.drop(['Open', 'High', 'Low', 'Close', 'Adj Close'],
                           axis=1)

        data = deepcopy(self.data)
        close = data.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'],
                           axis=1)

        volume_training, volume_test = self.split_data(volume, split_rate)
        close_training, close_test = self.split_data(close, split_rate)

        linear_reg = LinearRegression()
        linear_reg.fit(volume_training, close_training)

        close_pred = linear_reg.predict(volume_test)

        error = mean_squared_error(close_test, close_pred)
        coefficients = linear_reg.coef_
        score = r2_score(close_test, close_pred)

        print(error, coefficients, score)

    def linear_regression_price(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        close = data.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'],
                           axis=1)
        close_dates = close.index.values
        close_values = close.values

        close_dates = np.reshape(close_dates, (len(close_dates), 1))
        close_dates = [[int(d[0])] for d in close_dates]
        close_values = np.reshape(close_values, (len(close_values), 1))

        close_dates_train, close_dates_test = self.split_data(close_dates,
                                                              split_rate)
        close_values_train, close_values_test = self.split_data(close_values,
                                                                split_rate)

        linear_reg = LinearRegression()
        linear_reg.fit(close_dates_train, close_values_train)

        close_pred = linear_reg.predict(close_dates_test)

        error = mean_squared_error(close_values_test, close_pred)
        coefficients = linear_reg.coef_
        score = r2_score(close_values_test, close_pred)

        df_results = pd.DataFrame(index=np.concatenate(tuple(close_dates_test)),
                                  data={'Close': np.concatenate(tuple(close_values_test)),
                                        'Regression': np.concatenate(tuple(close_pred))})

        return {'close_pred': close_pred,
                'error': error,
                'coefficients': coefficients,
                'score': score,
                'df_results': df_results}

    def linear(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)

        sort_dates = sort.index.values
        sort_values = sort.values

        sort_dates = np.reshape(sort_dates, (len(sort_dates), 1))
        sort_dates = [[int(d[0])] for d in sort_dates]
        sort_values = np.reshape(sort_values, (len(sort_values), 1))

        sort_dates_train, sort_dates_test = self.split_data(sort_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        linear_reg = LinearRegression()
        linear_reg.fit(sort_dates_train, sort_values_train)

        sort_pred = linear_reg.predict(sort_dates_test)

        error = mean_squared_error(sort_values_test, sort_pred)
        coefficients = linear_reg.coef_
        score = r2_score(sort_values_test, sort_pred)

        df_results = pd.DataFrame(
            index=np.concatenate(tuple(sort_dates_test)),
            data={'Close': np.concatenate(tuple(sort_values_test)),
                  'Regression': np.concatenate(tuple(sort_pred))})

        return {'close_pred': sort_pred,
                'error': error,
                'coefficients': coefficients,
                'score': score,
                'df_results': df_results,
                'chosen_data': chosen_data_type}

    def split_data(self, data, training_percentage):
        data_len = len(data)
        training_divide = float(training_percentage) / 100
        training_len = int(data_len*training_divide)
        training = data[:training_len]
        test = data[training_len:]
        return training, test


if __name__ == '__main__':
    ob = Regression()
    ob.linear_regression()
