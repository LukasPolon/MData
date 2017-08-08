from kivy.uix.boxlayout import BoxLayout
from mdata.gui_env.buttons.info_button import InfoButton
from mdata.gui_env.buttons.options_button import OptionsButton

from kivy.uix.button import Button


class MenuLayout(BoxLayout):
    def __init__(self, screen_manager, screens, **kwargs):
        self.screen_manager = screen_manager
        self.screens = screens
        self._buttons = None
        self.orientation = 'vertical'
        self.width = 100
        self.size_hint = (None, 1)
        super(MenuLayout, self).__init__(**kwargs)

    def __call__(self):
        self.generate()
        return self

    @property
    def buttons(self):
        if self._buttons is None:
            buttons = {'info': InfoButton(self),
                       'options': OptionsButton(self)}
            self._buttons = buttons
        return self._buttons

    def generate(self):
        self.add_widget(self.buttons['info'])
        self.add_widget(self.buttons['options'])
        self.add_widget(Button(text='B3'))
        self.add_widget(Button(text='B4'))
        self.add_widget(Button(text='B5'))

