from kivy.uix.textinput import TextInput

from mdata.drivers.databases.operations import Operations


class CompanyTextinput(TextInput):
    def __init__(self, **kwargs):
        self.validate = True
        self.multiline = False
        self.size_hint = (0.4, 0.05)
        self.config_data = kwargs['conf_data']
        self.base = kwargs['base']
        self.db_operations = Operations()
        super(CompanyTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text(self.get_actual_company())
        return self

    def on_text(self, *args):
        self.base.hide_save_labels()
        exists = self.db_operations.exists_query(table='company_info',
                                                 column='name',
                                                 value=self.text)
        self.validate = True
        if not exists:
            self.validate = False

    def set_text(self, text):
        self.text = text

    def get_text(self, *args):
        return self.text

    def get_actual_company(self):
        return self.config_data['company']


