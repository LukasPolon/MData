from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label


class InfoScreenLayout(AnchorLayout):
    def __init__(self, **kwargs):
        self.anchor_x = 'center'
        self.anchor_y = 'top'
        super(InfoScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(Label(text='Info Label'))
        return self
