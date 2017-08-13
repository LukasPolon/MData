from kivy.uix.textinput import TextInput

from datetime import datetime

from mdata.drivers.databases.operations import Operations


class DateTextinput(TextInput):
    def __init__(self, **kwargs):
        self.validate = True
        self.multiline = False
        self.size_hint = (0.1, 0.05)
        self.config_data = kwargs['conf_data']
        self.base = kwargs['base']
        self.role = kwargs['role']
        self.db_operations = Operations()
        super(DateTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text(self.get_actual_date())
        return self

    def on_text(self, *args):
        try:
            self.parse_date()
            self.validate = True
        except:
            self.validate = False

    def set_text(self, text):
        self.text = text

    def get_text(self, *args):
        return self.text

    def get_actual_date(self):
        return self.config_data[self.role]

    def parse_date(self):
        date = self.text.split('-')
        date = [int(el) for el in date]
        date = datetime(*date)
        return date
