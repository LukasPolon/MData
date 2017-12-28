from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class DataTypeDropdown(Button):
    def __init__(self, **kwargs):
        self.data_types = kwargs['data_types']
        self.base = kwargs['base']
        self.conf_data = kwargs['conf_data']
        self.drop_list = DropDown()
        self.size_hint = (0.1, 0.05)
        self.validate = True
        super(DataTypeDropdown, self).__init__(**kwargs)

    def __call__(self):
        self.set_text(self.get_actual_method())
        self.build()
        return self

    def set_text(self, text):
        self.text = text

    def get_text(self, *args):
        return self.text

    def build(self):
        for d_type in self.data_types:
            btn = Button(text=d_type, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self,
                                                                  'text', x))

    def get_actual_method(self):
        return self.conf_data['data_type']