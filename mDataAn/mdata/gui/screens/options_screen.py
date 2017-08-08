from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from mdata.gui.layouts.options_screen_layout import OptionsScreenLayout


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        self.name = 'OptionsScreen'
        self.options_layout = OptionsScreenLayout()
        super(OptionsScreen, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(self.options_layout())
        return self
