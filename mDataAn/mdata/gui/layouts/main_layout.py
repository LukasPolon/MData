from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SwapTransition


from mdata.gui.screens.info_screen import InfoScreen
from mdata.gui.screens.options_screen import OptionsScreen
from mdata.gui.screens.regression_screen import RegressionScreen

from mdata.gui.layouts.menu_layout import MenuLayout


class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        self._info_screen = None
        self._menu_screen = None
        self._screens = None
        self.screen_manager = ScreenManager(transition=SwapTransition())
        self.menu_layout = MenuLayout(self.screen_manager, self.screens)
        self.cols = 2
        super(MainLayout, self).__init__(**kwargs)

    def __call__(self):
        self.add_widget(self.menu_layout())
        self.add_widget(self.screen_manager)
        self.screen_manager.switch_to(self.screens['info'])
        return self

    @property
    def screens(self):
        if self._screens is None:
            screens = {'info': InfoScreen()(),
                       'options': OptionsScreen()(),
                       'regression': RegressionScreen()()}
            self._screens = screens
        return self._screens



