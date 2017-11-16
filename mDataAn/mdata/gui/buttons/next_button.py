from kivy.uix.button import Button



class NextButton(Button):
    def __init__(self, **kwargs):
        self.comp_list = kwargs['company_list']
        self.size_hint = (0.2, 0.1)
        self.text = 'Next'
        super(NextButton, self).__init__(**kwargs)

    def on_press(self):
        self._change_display()

    def _change_display(self):
        self.comp_list.next_chunk()
        self.comp_list.set_text()