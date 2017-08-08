from kivy.app import App

from mdata.gui_env.layouts.main_layout import MainLayout


class MDataApp(App):
    def build(self):
        main_layout = MainLayout()
        return main_layout()

if __name__ == '__main__':
    ob = MDataApp()
    ob.run()

