import os

from kivy.uix.button import Button

from mdata.drivers.config.config_management import ConfigManagement


class RegressionSaveButton(Button):
    def __init__(self, **kwargs):
        self.display = kwargs['display']
        self.base = self.display.reg_textbox
        self.plots = kwargs['plots']
        self.config = ConfigManagement()
        super(RegressionSaveButton, self).__init__(**kwargs)

    def on_press(self):
        folder_name = self.create_folder()
        self.save_diagrams(folder_name)
        self.save_text(folder_name)

    def get_config_data(self):
        return self.config.get_data()

    def create_folder(self):
        format_date = self.plots.get_format_date()
        folder_name = os.path.join(self.get_config_data()['temp_dir'],
                                   format_date)
        os.mkdir(folder_name)

        if not os.path.exists(folder_name):
            raise ValueError('Wrong folder/ Folder does not exists.')

        return folder_name

    def save_diagrams(self, folder_name):
        if self.plots.unp_plot_fig:
            self.plots.unp_plot_fig.savefig('{dir}\{file}'
                                  .format(dir=folder_name,
                                    file=self.plots.diagram_names['prices_oc']))
        if self.plots.volume_plot_fig:
            self.plots.volume_plot_fig.savefig('{dir}\{file}'
                                     .format(dir=folder_name,
                                    file=self.plots.diagram_names['volume']))
        if self.plots.high_low_fig:
            self.plots.high_low_fig.savefig('{dir}\{file}'
                                  .format(dir=folder_name,
                                          file=self.plots.diagram_names['prices_hl']))
        if self.plots.regression_fig:
            self.plots.regression_fig.savefig('{dir}\{file}'
                                  .format(dir=folder_name,
                                          file=self.plots.diagram_names['linear_reg']))

    def save_text(self, folder_name):
        conf_data = self.get_config_data()
        company = conf_data['company']
        file_name = '{comp}_results_{date}.txt'\
                    .format(date=self.plots.get_format_date(),
                            comp=company)
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'w') as reg_f:
            reg_f.write(self.base.text)
            reg_f.flush()



