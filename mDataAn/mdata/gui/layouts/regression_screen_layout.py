from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label


class RegressionScreenLayout(AnchorLayout):
    def __init__(self, **kwargs):
        self.anchor_x = 'center'
        self.anchor_y = 'top'
        super(RegressionScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(Label(text='Regression Screen Label'))
        return self
