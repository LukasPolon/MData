from kivy.uix.button import Button


class RegressionButton(Button):
    def __init__(self, base, **kwargs):
        self.base = base
        self.text = 'Regression\n  Analysis'
        super(RegressionButton, self).__init__(**kwargs)

    def on_press(self):
        if self.base.screen_manager.current\
                != self.base.screens['regression'].name:
            self.base.screen_manager.switch_to(self.base.screens['regression'])
