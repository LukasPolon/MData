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
        # self.plots.save_reg_diagram()

        self.base += 'Regression analyze finished\n'
        self.base += 'Mean square error: {mse}\n'.format(mse=reg_data['error'])
        self.base += 'Coefficients: {coef}\n'\
                     .format(coef=reg_data['coefficients'])
        self.base += 'Score: {sc}\n'.format(sc=reg_data['score'])
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


