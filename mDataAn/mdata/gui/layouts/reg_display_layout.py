from kivy.uix.floatlayout import FloatLayout

from mdata.gui.items.reg_textinput import RegTextinput
from mdata.gui.buttons.data_diagram_button import DataDiagramButton
from mdata.gui.buttons.data_volume_diagram_button import DataVolumeDiagramButton


class RegDisplayLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.size = (820, 650)
        self.reg_textbox = RegTextinput(pos=(0, 0))
        self.data_diagram_button = DataDiagramButton(pos=(450, 550),
                                                     plots=kwargs['plots'])
        self.volume_diagram_button = DataVolumeDiagramButton(pos=(580, 550),
                                                             plots=kwargs['plots'])
        self.loaded_data = None
        super(RegDisplayLayout, self).__init__(**kwargs)

    def __call__(self):
        self.generate()
        return self

    def generate(self):
        self.add_widget(self.reg_textbox())
        self.add_widget(self.data_diagram_button)
        self.add_widget(self.volume_diagram_button)
