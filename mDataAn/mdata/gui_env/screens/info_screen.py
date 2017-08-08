from kivy.uix.screenmanager import Screen

from mdata.gui_env.layouts.info_screen_layout import InfoScreenLayout


class InfoScreen(Screen):
    def __init__(self, **kwargs):
        self.name = 'InfoScreen'
        self.info_layout = InfoScreenLayout()
        super(InfoScreen, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(self.info_layout())
        return self
