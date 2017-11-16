from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from mdata.gui.buttons.load_data_button import LoadDataButton
from mdata.gui.buttons.regression_analyze_button import RegressionAnalyzeButton


class RegMenuLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        self.width = 80
        self.display_panel = kwargs['display']
        self.plots = kwargs['plots']
        self.size_hint = (None, 1)
        self._buttons = None
        super(RegMenuLayout, self).__init__(**kwargs)

    def __call__(self):
        self.generate()
        return self

    @property
    def buttons(self):
        if self._buttons is None:
            buttons = {'load_data': LoadDataButton(text='Load stock\n     data',
                                                   display=self.display_panel,
                                                   plots=self.plots),
                       'regression': RegressionAnalyzeButton(
                                        text='Regression\n   analyze',
                                        display=self.display_panel),
                       'empty': Button,
                       'old_results': Button(text='Load old\n  results')}
            self._buttons = buttons
        return self._buttons

    def generate(self):
        self.add_widget(self.buttons['load_data'])
        self.add_widget(self.buttons['regression'])
        self.add_widget(self.buttons['empty']())
        self.add_widget(self.buttons['empty']())
        self.add_widget(self.buttons['old_results'])
