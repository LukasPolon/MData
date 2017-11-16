from kivy.uix.gridlayout import GridLayout

from mdata.gui.layouts.reg_menu_layout import RegMenuLayout
from mdata.gui.layouts.reg_display_layout import RegDisplayLayout
from mdata.client.plots import PlotsGenerate


class RegressionScreenLayout(GridLayout):
    def __init__(self, **kwargs):
        self.reg_menu = None
        self.cols = 2
        self.plots = PlotsGenerate()
        self.display_layout = RegDisplayLayout(plots=self.plots)
        self.menu_layout = RegMenuLayout(display=self.display_layout,
                                         plots=self.plots)
        super(RegressionScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(self.display_layout())
        self.add_widget(self.menu_layout())
        return self
