from kivy.uix.button import Button

from mdata.client.regression import Regression

class RegressionAnalyzeButton(Button):
    def __init__(self, **kwargs):
        self.display = kwargs['display']
        self.loaded_data = None
        self.regression = Regression()
        super(RegressionAnalyzeButton, self).__init__(**kwargs)

    def on_press(self):
        self._get_loaded_data()
        self.regression.get_data(self.loaded_data)
        self.regression.linear_regression_price()
        # self.regression.linear_regression()

    def _get_loaded_data(self):
        if self.display.loaded_data is not None:
            self.loaded_data = self.display.loaded_data


