from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label
from mdata.gui.items.reg_textinput import RegTextinput


class RegDisplayLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.size = (820, 650)
        self.reg_textbox = RegTextinput(pos=(0, 0))
        super(RegDisplayLayout, self).__init__(**kwargs)

    def __call__(self):
        self.generate()
        return self

    def generate(self):
        self.add_widget(self.reg_textbox())
