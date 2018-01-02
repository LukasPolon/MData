import re
import numpy as np
import pandas as pd
from datetime import date

from copy import deepcopy

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor

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

        linear_reg2 = LinearRegression()
        linear_reg2.fit(sort_dates_train, sort_values_train)
        sort_pred2 = linear_reg.predict(sort_dates)

        error = mean_squared_error(sort_values_test, sort_pred)
        coefficients = linear_reg.coef_
        score = r2_score(sort_values_test, sort_pred)

        df_test_results = pd.DataFrame(
            index=np.concatenate(tuple(sort_dates_test)),
            data={'Close': np.concatenate(tuple(sort_values_test)),
                  'Regression': np.concatenate(tuple(sort_pred))})

        df_all_results = pd.DataFrame(
            index=np.concatenate(tuple(sort_dates)),
            data={'Close': np.concatenate(tuple(sort_values)),
                  'Regression': np.concatenate(tuple(sort_pred2))})

        parsed_train_dates, parsed_test_dates = self.split_data(sort.index.values, split_rate)
        parsed_all_dates = np.concatenate((parsed_train_dates, parsed_test_dates))

        parsed_all_dates = self.dt_parse(parsed_all_dates)
        parsed_train_dates = self.dt_parse(parsed_train_dates)
        parsed_test_dates = self.dt_parse(parsed_test_dates)

        train_test_date = parsed_train_dates[-1]
        train_test_vert_date = sort_dates_train[-1]

        return {'close_pred': sort_pred,
                'error': error,
                'coefficients': coefficients,
                'score': score,
                'df_test_results': df_test_results,
                'df_all_results': df_all_results,
                'chosen_data': chosen_data_type,
                'parsed_all_dates': parsed_all_dates,
                'parsed_train_dates': parsed_train_dates,
                'parsed_test_dates': parsed_test_dates,
                'train_test_date': train_test_date,
                'train_test_vert_date': train_test_vert_date}

    def svr(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_dates = [d.astype('M8[D]').astype('O') for d in sort.index.values]
        sort_values = np.concatenate(sort.values)

        new_dates = list()
        for d in sort_dates:
            d_year = str(d.year)
            d_month = '0{m}'.format(m=d.month) if len(str(d.month)) is 1 else str(d.month)
            d_day = '0{d}'.format(d=d.day) if len(str(d.day)) is 1 else str(d.day)
            new_dates.append(int(''.join([d_year, d_month, d_day])))
        new_dates = np.reshape(np.asarray(new_dates), (len(new_dates), 1))

        sort_dates_train, sort_dates_test = self.split_data(new_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr_rbf.fit(sort_dates_train, sort_values_train)
        sort_pred = svr_rbf.predict(new_dates)
        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)
        # score = r2_score(sort_values_test, pred_no_train)
        sort_dates_test = [self.parse_date(x)
                           for x in np.concatenate(sort_dates_test)]
        sort_dates_train = [self.parse_date(x)
                            for x in np.concatenate(sort_dates_train)]
        all_dates = np.concatenate((sort_dates_train, sort_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        score = svr_rbf.score(new_dates, all_values)

        train_test_vert_date = pd.to_datetime(
                                str(sort_dates_train[-1])).strftime('%Y-%m-%d')

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=sort_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type}

    def kernel_ridge(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_dates = [d.astype('M8[D]').astype('O') for d in sort.index.values]
        sort_values = np.concatenate(sort.values)

        new_dates = list()
        for d in sort_dates:
            d_year = str(d.year)
            d_month = '0{m}'.format(m=d.month) if len(
                str(d.month)) is 1 else str(d.month)
            d_day = '0{d}'.format(d=d.day) if len(str(d.day)) is 1 else str(
                d.day)
            new_dates.append(int(''.join([d_year, d_month, d_day])))
        new_dates = np.reshape(np.asarray(new_dates), (len(new_dates), 1))

        sort_dates_train, sort_dates_test = self.split_data(new_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        svr_rbf = KernelRidge(kernel='rbf')#, alpha=1e3, gamma=0.1)
        svr_rbf.fit(sort_dates_train, sort_values_train)
        print(svr_rbf.get_params())
        sort_pred = svr_rbf.predict(new_dates)

        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)
        # score = r2_score(sort_values_test, pred_no_train)
        sort_dates_test = [self.parse_date(x)
                           for x in np.concatenate(sort_dates_test)]
        sort_dates_train = [self.parse_date(x)
                            for x in np.concatenate(sort_dates_train)]
        all_dates = np.concatenate((sort_dates_train, sort_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        score = svr_rbf.score(new_dates, all_values)

        train_test_vert_date = pd.to_datetime(
            str(sort_dates_train[-1])).strftime('%Y-%m-%d')

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=sort_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type}

    def gaussian_process(self):
        data = deepcopy(self.data)
        split_rate = self.get_split_rate()
        chosen_data_type = self.get_data_type()
        all_data_types = self.regression_data_types
        data_to_drop = [data_t for data_t in all_data_types
                        if data_t != chosen_data_type]

        sort = data.drop(data_to_drop, axis=1)
        sort_dates = [d.astype('M8[D]').astype('O') for d in sort.index.values]
        sort_values = np.concatenate(sort.values)

        new_dates = list()
        for d in sort_dates:
            d_year = str(d.year)
            d_month = '0{m}'.format(m=d.month) if len(str(d.month)) is 1 else str(d.month)
            d_day = '0{d}'.format(d=d.day) if len(str(d.day)) is 1 else str(d.day)
            new_dates.append(int(''.join([d_year, d_month, d_day])))
        new_dates = np.reshape(np.asarray(new_dates), (len(new_dates), 1))

        sort_dates_train, sort_dates_test = self.split_data(new_dates,
                                                            split_rate)
        sort_values_train, sort_values_test = self.split_data(sort_values,
                                                              split_rate)

        svr_rbf = GaussianProcessRegressor()
        svr_rbf.fit(sort_dates_train, sort_values_train)
        sort_pred = svr_rbf.predict(new_dates)

        pred_no_train = sort_pred[len(sort_dates_train):]

        error = mean_squared_error(sort_values_test, pred_no_train)
        # score = r2_score(sort_values_test, pred_no_train)
        sort_dates_test = [self.parse_date(x)
                           for x in np.concatenate(sort_dates_test)]
        sort_dates_train = [self.parse_date(x)
                            for x in np.concatenate(sort_dates_train)]
        all_dates = np.concatenate((sort_dates_train, sort_dates_test))
        all_values = np.concatenate((sort_values_train, sort_values_test))
        score = svr_rbf.score(new_dates, all_values)

        train_test_vert_date = pd.to_datetime(
                                str(sort_dates_train[-1])).strftime('%Y-%m-%d')

        df_all_results = pd.DataFrame(
            index=all_dates,
            data={chosen_data_type: all_values,
                  'Regression': sort_pred}
        )
        df_test_results = pd.DataFrame(
            index=sort_dates_test,
            data={chosen_data_type: sort_values_test,
                  'Regression': pred_no_train}
        )

        return {'close_pred': sort_pred,
                'error': error,
                'score': score,
                'df_all_results': df_all_results,
                'train_test_vert_date': train_test_vert_date,
                'df_test_results': df_test_results,
                'chosen_data': chosen_data_type}

    def split_data(self, data, training_percentage):
        data_len = len(data)
        training_divide = float(training_percentage) / 100
        training_len = int(data_len*training_divide)
        training = data[:training_len]
        test = data[training_len:]
        return training, test

    def parse_date(self, int_date):
        n_date = '{y}-{m}-{d}'.format(y=str(int_date)[:4],
                                      m=str(int_date)[4:6],
                                      d=str(int_date)[6:])
        return np.datetime64(n_date)

    def dt_parse(self, dt):
        e = '2017-11-17T00:00:00.000000000'
        date_reg = r'([0-9\-]+)T'
        new_dt = list()
        for d in dt:
            new_dt.append(re.match(date_reg, str(d)).group(1))
        new_dt = np.asarray(new_dt)
        return new_dt

