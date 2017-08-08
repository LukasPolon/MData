from kivy.uix.button import Button
from kivy.uix.popup import Popup

from mdata.gui.layouts.exit_popup_layout import ExitPopupLayout


class ExitButton(Button):
    def __init__(self, base, **kwargs):
        self.base = base
        self.text = 'Exit'
        super(ExitButton, self).__init__(**kwargs)

    def on_press(self):
        self.generate_popup()

    def generate_popup(self):
        exit_popup_layout = ExitPopupLayout()
        popup = Popup(title='Exit',
                      content=exit_popup_layout(),
                      size=(350, 350),
                      size_hint=(None, None))
        popup.open()
