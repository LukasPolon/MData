from kivy.uix.textinput import TextInput


class DataSplitRateTextinput(TextInput):
    def __init__(self, **kwargs):
        self.validate = True
        self.multiline = False
        self.size_hint = (0.1, 0.05)
        self.config_data = kwargs['conf_data']
        self.base = kwargs['base']
        super(DataSplitRateTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text(self.get_actual_splitrate())
        return self

    def set_text(self, text):
        self.text = text

    def get_text(self, *args):
        return self.text

    def get_actual_splitrate(self):
        return self.config_data['split_rate']

    def on_text(self, *args):
        rate = self.get_text()
        self.validate = True
