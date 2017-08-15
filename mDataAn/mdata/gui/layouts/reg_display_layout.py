from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label


class RegDisplayLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.size = (820, 650)
        self._labels = None
        super(RegDisplayLayout, self).__init__(**kwargs)

    @property
    def labels(self):
        if self._labels is None:
            labels = {'company': Label(text='Company:',
                                       pos=(-370, 300)),
                      'dates': Label(text='Date range:',
                                     pos=(-366, 260)),
                      'regression': Label(text='Regression model:',
                                          pos=(-342, 220))}
            self._labels = labels
        return self._labels

    def __call__(self):
        self.generate()
        return self

    def generate(self):
        self.add_widget(self.labels['company'])
        self.add_widget(self.labels['dates'])
        self.add_widget(self.labels['regression'])