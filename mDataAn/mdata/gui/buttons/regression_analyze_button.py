from tabulate import tabulate

from kivy.uix.button import Button

from mdata.client.regression import Regression
from mdata.drivers.config.config_management import ConfigManagement


class RegressionAnalyzeButton(Button):
    def __init__(self, **kwargs):
        self.display = kwargs['display']
        self.base = self.display.reg_textbox
        self.plots = kwargs['plots']
        self.loaded_data = None
        self.regression = Regression()
        self.config = ConfigManagement()
        self.break_bar = '\n{break_ln}\n\n'.format(break_ln='*' * 60)
        super(RegressionAnalyzeButton, self).__init__(**kwargs)

    def on_press(self):
        self._get_loaded_data()
        self.regression.get_data(self.loaded_data)
        reg_describe = self.get_reg_describe()

        self.base += 'Regression type: {type}\n'\
                     .format(type=reg_describe['reg_type'])
        self.base += 'Selected data: {data}\n'\
                     .format(data=reg_describe['reg_data_type'])
        self.base += 'Train data: {rate}%\n'\
                     .format(rate=reg_describe['split_rate'])
        self.base += self.break_bar

        reg_data = self.get_reg_method()()
        self.plots.get_regression_data(reg_data)
        self.plots.generate_regression_plot()
        self.plots.generate_regression_only_test()

        self.base += 'Regression analyze finished\n'
        self.base += 'Mean square error: {mse}\n'.format(mse=reg_data['error'])

        self.base += 'Score: {sc}\n'.format(sc=reg_data['score'])
        self.display_reg_table(reg_data)
        self.base += self.break_bar

    def _get_loaded_data(self):
        if self.display.loaded_data is not None:
            self.loaded_data = self.display.loaded_data

    def get_reg_method(self):
        config_data = self.config.get_data()
        reg_method_key = config_data['regression']
        reg_method_func = self.regression.regression_methods[reg_method_key]

        return reg_method_func

    def get_reg_describe(self):
        conf_data = self.config.get_data()
        return {'reg_type': conf_data['regression'],
                'reg_data_type': conf_data['data_type'],
                'split_rate': conf_data['split_rate']}

    def display_reg_table(self, reg_data):
        self.base += 'Regression test data:\n'
        self.base += '--------------------------\n'
        pd_keys = reg_data['df_test_results'].keys()
        pd_values = reg_data['df_test_results'].values
        pd_dates = reg_data['df_test_results'].index

        pd_all_dates = reg_data['df_all_results']
        train_dates_amount = len(pd_all_dates) - len(pd_dates)

        self.base += 'Date                {k}\n'.format(k='    '.join(pd_keys))
        for d, v in zip(pd_dates, pd_values):
            first_v = str(v[0])
            second_v = str(v[1])
            self.base += '{d}     {fv}   {sv}\n'\
                         .format(d=str(d).replace('00:00:00', ''),
                                 fv=first_v, sv=second_v)
        pd_tab = tabulate(reg_data['df_test_results'],
                          headers='keys', tablefmt='psql')
        self.base += '--------------------------\n'
        self.base += 'Train/Test data border: {b}\n'\
                     .format(b=reg_data['train_test_vert_date'])
        self.base += 'Train data amount: {a}\n'.format(a=train_dates_amount)
        self.base += 'Test data amount: {t}\n'.format(t=len(pd_dates))



