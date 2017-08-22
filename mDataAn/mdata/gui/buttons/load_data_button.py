from kivy.uix.button import Button

from mdata.drivers.config.config_management import ConfigManagement


class LoadDataButton(Button):
    def __init__(self, **kwargs):
        self.base = kwargs['display'].reg_textbox
        super(LoadDataButton, self).__init__(**kwargs)

    def __call__(self):
        pass
md
    def on_press(self):
        config = ConfigManagement()
        config_data = config.get_data()
        self.update_output(config_data)

    def update_output(self, conf_data):
        self.base.clear_text()
        self.base += 'Company: {company}\n'.format(**conf_data)
        self.base += 'Date range: {date_from} - ' \
                     '{date_to}\n'.format(**conf_data)
        self.base += 'Regression method: : {regression}\n'.format(**conf_data)
        self.base += '\n{break_ln}\n\n'.format(break_ln='*'*60)

