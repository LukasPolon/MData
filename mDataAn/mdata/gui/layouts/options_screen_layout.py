from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from mdata.gui.items.temp_dir_textinput import TempDirTextinput


class OptionsScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.name = 'Options screen layout'
        self.size = (900, 650)
        self._labels = None
        self._inputs = None
        super(OptionsScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    @property
    def labels(self):
        if self._labels is None:
            labels = {'temp_dir': Label(text='Temporary files directory',
                                        pos=(-350, 300)),
                      'company': Label(text='Company',
                                       pos=(-400, 200))}
            self._labels = labels
        return self._labels

    @property
    def inputs(self):
        if self._inputs is None:
            inputs = {'temp_dir': TempDirTextinput(pos=(15, 570))}
            self._inputs = inputs
        return self._inputs

    def generate(self):
        self.add_widget(self.labels['temp_dir'])
        self.add_widget(self.inputs['temp_dir']())
        self.add_widget(self.labels['company'])


        return self

