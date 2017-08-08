from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class ExitPopupLayout(GridLayout):
    def __init__(self, **kwargs):
        self.name = 'Exit popup layout'
        self.rows = 2
        super(ExitPopupLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        popup_label = Label(text='Are you sure you want to \n'
                                 '   exit the application?')
        exit_button = Button(text='Yes',
                             size_hint=(0.5, 0.3))
        exit_button.bind(on_press=App.get_running_app().stop)

        self.add_widget(popup_label)
        self.add_widget(exit_button)
        return self
