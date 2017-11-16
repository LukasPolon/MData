from kivy.uix.button import Button

from mdata.drivers.config.config_management import ConfigManagement


class SaveButton(Button):
    def __init__(self, base, **kwargs):
        self.base = base
        self.text = 'Save'
        self.size_hint = (0.2, 0.1)
        self.inputs = kwargs['inputs']
        self.incorrect_inputs = list()
        self.exceptions = ['company_list']
        super(SaveButton, self).__init__(**kwargs)

    def on_press(self):
        self.base.hide_save_labels()
        data = {name: value.get_text() for (name, value)
                in self.inputs.iteritems()
                if name not in self.exceptions}
        config = ConfigManagement()
        try:
            self.validate_inputs()
            config.set_data(data)
            self.base.add_widget(self.base.labels['saved'])
        except ValueError:
            wrong_labels = [self.base.labels[label].text
                            for label in self.incorrect_inputs]
            error = 'Error during saving configuration.\n' \
                    'Wrong content: {box}'\
                    .format(box='  '.join(wrong_labels))
            self.base.labels['not_saved_custom'].text = error
            self.base.add_widget(self.base.labels['not_saved_custom'])
        except Exception as e:
            print(e)
            self.base.add_widget(self.base.labels['not_saved'])

    def validate_inputs(self):
        self.incorrect_inputs = list()
        for name, content in self.inputs.iteritems():
            if not content.validate:
                self.incorrect_inputs.append(name)
        if self.incorrect_inputs:
            raise ValueError
