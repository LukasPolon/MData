from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class OptionsScreen(object):
    def __init__(self):
        pass

    def __call__(self):
        return self.generate()

    def generate(self):
        options_screen = Screen(name='OptionsScreen')
        options_screen_layout = GridLayout(rows=2)
        options_screen_layout.add_widget(Button(text='MB1'))
        options_screen_layout.add_widget(Button(text='MB2'))
        options_screen.add_widget(options_screen_layout)

        return options_screen