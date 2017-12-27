import subprocess

from kivy.uix.button import Button

from mdata.drivers.config.config_management import ConfigManagement


class OpenExplorerButton(Button):
    def __init__(self, **kwargs):
        self.config = ConfigManagement()
        self.text = 'Open Results\n  Folder'
        self.size_hint = (0.15, 0.055)
        super(OpenExplorerButton, self).__init__(**kwargs)

    def on_press(self):
        config_data = self.config.get_data()
        temp_dir = config_data['temp_dir']

        subprocess.Popen(r'explorer "{temp_dir}"'
                         .format(temp_dir=temp_dir))