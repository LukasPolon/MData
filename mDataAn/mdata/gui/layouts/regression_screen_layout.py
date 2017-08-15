from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from mdata.gui.layouts.reg_menu_layout import RegMenuLayout
from mdata.gui.layouts.reg_display_layout import RegDisplayLayout


class RegressionScreenLayout(GridLayout):
    def __init__(self, **kwargs):
        self.reg_menu = None
        self.cols = 2
        super(RegressionScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(RegDisplayLayout()())
        self.add_widget(RegMenuLayout()())
        return self
