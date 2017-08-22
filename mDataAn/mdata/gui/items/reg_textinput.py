from kivy.uix.textinput import TextInput


class RegTextinput(TextInput):
    def __init__(self, **kwargs):
        self.size_hint = (0.5, 1)
        self.readonly = True
        super(RegTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.fill_basics()
        return self

    def __iadd__(self, text):
        self.text += text
        return self

    def set_text(self, text):
        self.text = text

    def clear_text(self):
        self.text = ''

    def fill_basics(self):
        self.text += 'Company:\n'
        self.text += 'Date range:\n'
        self.text += 'Regression method:\n'
