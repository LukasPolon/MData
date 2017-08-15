from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

from mdata.drivers.config.config_management import ConfigManagement

from mdata.gui.items.temp_dir_textinput import TempDirTextinput
from mdata.gui.items.company_textinput import CompanyTextinput
from mdata.gui.items.date_textinput import DateTextinput
from mdata.gui.items.regression_dropdown import RegressionDropdown

from mdata.gui.buttons.save_button import SaveButton


class OptionsScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.name = 'Options screen layout'
        self.size = (900, 650)
        self._labels = None
        self._inputs = None
        self._images = None
        self._buttons = None
        self._regression = None
        self.config_obj = ConfigManagement()
        self._config_data = None
        super(OptionsScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    @property
    def regression(self):
        if self._regression is None:
            reg = ['method_1', 'method_2', 'method_3',
                   'method_4']
            self._regression = reg
        return self._regression

    @property
    def config_data(self):
        if self._config_data is None:
            self._config_data = self.config_obj.get_data()
        return self._config_data

    @property
    def labels(self):
        if self._labels is None:
            labels = {'temp_dir': Label(text='Temporary files directory',
                                        pos=(-350, 300)),
                      'company': Label(text='Company',
                                       pos=(-400, 200)),
                      'saved': Label(text='Configuration saved!',
                                     pos=(-140, -280)),
                      'not_saved': Label(text='Error during saving '
                                              'configuration.\nCheck inputs.',
                                         pos=(0, -280)),
                      'not_saved_custom': Label(pos=(0, -280),
                                                halign='left'),
                      'date_from': Label(text='Date from',
                                         pos=(-400, 100)),
                      'date_to': Label(text='Date to',
                                       pos=(-250, 100)),
                      'regression': Label(text='Regression method',
                                          pos=(-370, 0))}
            self._labels = labels
        return self._labels

    @property
    def inputs(self):
        if self._inputs is None:
            inputs = {'temp_dir': TempDirTextinput(pos=(15, 570),
                                                   conf_data=self.config_data,
                                                   base=self),
                      'company': CompanyTextinput(pos=(15, 470),
                                                  conf_data=self.config_data,
                                                  base=self),
                      'date_from': DateTextinput(pos=(15, 370),
                                                 conf_data=self.config_data,
                                                 base=self,
                                                 role='date_from'),
                      'date_to': DateTextinput(pos=(175, 370),
                                               conf_data=self.config_data,
                                               base=self,
                                               role='date_to'),
                      'regression': RegressionDropdown(pos=(15, 270),
                                                conf_data=self.config_data,
                                                reg_methods=self.regression,
                                                base=self)}
            self._inputs = inputs
        return self._inputs

    @property
    def buttons(self):
        if self._buttons is None:
            buttons = {'save': SaveButton(pos=(50, 10), inputs=self.inputs,
                                          base=self)}
            self._buttons = buttons
        return self._buttons

    def generate(self):
        self.add_widget(self.labels['temp_dir'])
        self.add_widget(self.inputs['temp_dir']())
        self.add_widget(self.labels['company'])
        self.add_widget(self.inputs['company']())
        self.add_widget(self.buttons['save'])
        self.add_widget(self.labels['date_from'])
        self.add_widget(self.inputs['date_from']())
        self.add_widget(self.labels['date_to'])
        self.add_widget(self.inputs['date_to']())
        self.add_widget(self.labels['regression'])
        self.add_widget(self.inputs['regression']())
        self.hide_save_labels()

        return self

    def hide_save_labels(self):
        labels = ['Configuration saved!', 'Error during saving configuration.']

        hide = [child for child in self.children
                if type(child) == Label
                and (child.text in labels or 'Error' in child.text)]
        [self.remove_widget(wid) for wid in hide]

