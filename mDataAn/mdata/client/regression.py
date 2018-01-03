import re
import numpy as np
import pandas as pd

from copy import deepcopy

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

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
            reg_methods = {'linear': self.linear,
                           'svr': self.svr,
                           'kernel_ridge': self.kernel_ridge,
                           'gaussian': self.gaussian_process}
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

    def linear(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_values = np.concatenate(sort.values)
        sort_dates = sort.index.values

        original_dates, dates_delta = self.change_dates(sort_dates)
        dates_delta = np.reshape(dates_delta, (len(dates_delta), 1))

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        sort_dates = sc_y.fit_transform(dates_delta)
        sort_values = sc_x.fit_transform(sort_values)

        sort_dates_train, sort_dates_test = self.split_data(sort_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        linear_reg = LinearRegression()
        linear_reg.fit(sort_dates_train, sort_values_train)
        sort_pred = linear_reg.predict(sort_dates)

        sc_p = StandardScaler()
        sc_p.fit(sort_pred)
        sort_pred = sc_x.inverse_transform(sort_pred)
        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)

        orig_dates_train = original_dates[
                           :len(np.concatenate(sort_dates_train))]
        orig_dates_test = original_dates[
                          len(np.concatenate(sort_dates_train)):]

        all_dates = np.concatenate((orig_dates_train, orig_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        sort_values_test = sc_x.inverse_transform(sort_values_test)
        all_values = sc_x.inverse_transform(all_values)

        score = linear_reg.score(sort_dates, all_values)

        train_test_vert_date = orig_dates_train[-1]

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=orig_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        best_params = ''

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type,
                'best_params': best_params}

    def svr(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_values = np.concatenate(sort.values)
        sort_dates = sort.index.values

        original_dates, dates_delta = self.change_dates(sort_dates)
        dates_delta = np.reshape(dates_delta, (len(dates_delta), 1))

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        sort_dates = sc_y.fit_transform(dates_delta)
        sort_values = sc_x.fit_transform(sort_values)

        sort_dates_train, sort_dates_test = self.split_data(sort_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        svr_rbf = GridSearchCV(SVR(kernel='rbf'),
                               param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                                           "gamma": np.logspace(-2, 2, 5)})
        svr_rbf.fit(sort_dates_train, sort_values_train)
        sort_pred = svr_rbf.predict(sort_dates)

        sc_p = StandardScaler()
        sc_p.fit(sort_pred)
        sort_pred = sc_x.inverse_transform(sort_pred)
        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)

        orig_dates_train = original_dates[
                           :len(np.concatenate(sort_dates_train))]
        orig_dates_test = original_dates[
                          len(np.concatenate(sort_dates_train)):]

        all_dates = np.concatenate((orig_dates_train, orig_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        sort_values_test = sc_x.inverse_transform(sort_values_test)
        all_values = sc_x.inverse_transform(all_values)

        score = svr_rbf.score(sort_dates, all_values)

        train_test_vert_date = orig_dates_train[-1]

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=orig_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        best_params = svr_rbf.best_params_

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type,
                'best_params': best_params}

    def kernel_ridge(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_values = np.concatenate(sort.values)
        sort_dates = sort.index.values

        original_dates, dates_delta = self.change_dates(sort_dates)
        dates_delta = np.reshape(dates_delta, (len(dates_delta), 1))

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        sort_dates = sc_y.fit_transform(dates_delta)
        sort_values = sc_x.fit_transform(sort_values)

        sort_dates_train, sort_dates_test = self.split_data(sort_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        krr = GridSearchCV(KernelRidge(kernel='rbf'),
                               param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3],
                                           "gamma": np.logspace(-2, 2, 5)})

        krr.fit(sort_dates_train, sort_values_train)
        sort_pred = krr.predict(sort_dates)

        sc_p = StandardScaler()
        sc_p.fit(sort_pred)
        sort_pred = sc_x.inverse_transform(sort_pred)
        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)

        orig_dates_train = original_dates[:len(np.concatenate(sort_dates_train))]
        orig_dates_test = original_dates[len(np.concatenate(sort_dates_train)):]

        all_dates = np.concatenate((orig_dates_train, orig_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        sort_values_test = sc_x.inverse_transform(sort_values_test)
        all_values = sc_x.inverse_transform(all_values)

        score = krr.score(sort_dates, all_values)

        train_test_vert_date = orig_dates_train[-1]

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=orig_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        best_params = krr.best_params_

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type,
                'best_params': best_params}

    def gaussian_process(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_values = np.concatenate(sort.values)
        sort_dates = sort.index.values

        original_dates, dates_delta = self.change_dates(sort_dates)
        dates_delta = np.reshape(dates_delta, (len(dates_delta), 1))

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        sort_dates = sc_y.fit_transform(dates_delta)
        sort_values = sc_x.fit_transform(sort_values)

        sort_dates_train, sort_dates_test = self.split_data(sort_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        gpr = GridSearchCV(GaussianProcessRegressor(),
                           param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3,
                                                 1e-6, 1e-10]})
        gpr.fit(sort_dates_train, sort_values_train)
        sort_pred = gpr.predict(sort_dates)

        sc_p = StandardScaler()
        sc_p.fit(sort_pred)
        sort_pred = sc_x.inverse_transform(sort_pred)
        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)

        orig_dates_train = original_dates[
                           :len(np.concatenate(sort_dates_train))]
        orig_dates_test = original_dates[
                          len(np.concatenate(sort_dates_train)):]

        all_dates = np.concatenate((orig_dates_train, orig_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        sort_values_test = sc_x.inverse_transform(sort_values_test)
        all_values = sc_x.inverse_transform(all_values)

        score = gpr.score(sort_dates, all_values)

        train_test_vert_date = orig_dates_train[-1]

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=orig_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        best_params = gpr.best_params_

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type,
                'best_params': best_params}

    def split_data(self, data, training_percentage):
        data_len = len(data)
        training_divide = float(training_percentage) / 100
        training_len = int(data_len*training_divide)
        training = data[:training_len]
        test = data[training_len:]
        return training, test

    def change_dates(self, dates):
        original_dates = pd.to_datetime(dates)
        dates_delta = (original_dates - original_dates.min())\
                       / np.timedelta64(1, 'D')
        dates_delta = np.asarray(dates_delta)
        return original_dates, dates_delta

