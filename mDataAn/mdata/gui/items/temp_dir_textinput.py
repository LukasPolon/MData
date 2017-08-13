import os
from kivy.uix.textinput import TextInput


class TempDirTextinput(TextInput):
    def __init__(self, **kwargs):
        self.validate = True
        self.multiline = False
        self.size_hint = (0.4, 0.05)
        self.config_data = kwargs['conf_data']
        self.base = kwargs['base']
        super(TempDirTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text(self.get_actual_directory())
        return self

    def on_text(self, *args):
        self.base.hide_save_labels()
        self.validate = True
        if not os.path.isdir(self.text):
            self.validate = False

    def set_text(self, text):
        self.text = text

    def get_text(self, *args):
        return self.text

    def get_actual_directory(self):
        return self.config_data['temp_dir']
