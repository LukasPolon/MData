from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable',0)

from kivy.core.window import Window
Window.size = (1000, 650)

from mdata.gui.layouts.main_layout import MainLayout


class MDataApp(App):
    def build(self):
        main_layout = MainLayout()
        return main_layout()

if __name__ == '__main__':
    ob = MDataApp()
    ob.run()

