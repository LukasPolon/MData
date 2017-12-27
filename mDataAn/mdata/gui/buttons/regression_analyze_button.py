from kivy.uix.button import Button

from mdata.client.regression import Regression
from mdata.drivers.config.config_management import ConfigManagement


class RegressionAnalyzeButton(Button):
    def __init__(self, **kwargs):
        self.display = kwargs['display']
        self.loaded_data = None
        self.regression = Regression()
        self.config = ConfigManagement()
        super(RegressionAnalyzeButton, self).__init__(**kwargs)

    def on_press(self):
        self._get_loaded_data()
        self.regression.get_data(self.loaded_data)
        self.get_reg_method()()

    def _get_loaded_data(self):
        if self.display.loaded_data is not None:
            self.loaded_data = self.display.loaded_data

    def get_reg_method(self):
        config_data = self.config.get_data()
        reg_method_key = config_data['regression']
        reg_method_func = self.regression.regression_methods[reg_method_key]

        return reg_method_func


