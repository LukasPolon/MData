from kivy.uix.button import Button


class OptionsButton(Button):
    def __init__(self, base, **kwargs):
        self.base = base
        self.text = 'Options'
        super(OptionsButton, self).__init__(**kwargs)

    def on_press(self):
        if self.base.screen_manager.current\
                != self.base.screens['options'].name:
            self.base.screen_manager.switch_to(self.base.screens['options'])
