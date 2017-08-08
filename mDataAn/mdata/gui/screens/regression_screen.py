from kivy.uix.screenmanager import Screen

from mdata.gui.layouts.regression_screen_layout import RegressionScreenLayout


class RegressionScreen(Screen):
    def __init__(self, **kwargs):
        self.name = 'RegressionScreen'
        self.info_layout = RegressionScreenLayout()
        super(RegressionScreen, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(self.info_layout())
        return self
