from kivy.uix.textinput import TextInput


class TempDirTextinput(TextInput):
    def __init__(self, **kwargs):
        self.multiline = False
        self.size_hint = (0.4, 0.05)
        super(TempDirTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text('Directory')
        return self

    def set_text(self, text):
        self.text = text

    def get_actual_directory(self):
        pass
