from kivy.uix.button import Button


class InfoButton(Button):
    def __init__(self, base, **kwargs):
        self.base = base
        self.text = 'Info'
        super(InfoButton, self).__init__(**kwargs)

    def on_press(self):
        if self.base.screen_manager.current\
                != self.base.screens['info'].name:
            self.base.screen_manager.switch_to(self.base.screens['info'])
