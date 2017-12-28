import time
from kivy.uix.button import Button

from mdata.drivers.config.config_management import ConfigManagement
from mdata.client.data_download import DataDownload
from mdata.client.plots import PlotsGenerate


class LoadDataButton(Button):
    def __init__(self, **kwargs):
        self.display = kwargs['display']
        self.base = kwargs['display'].reg_textbox
        self.plots = kwargs['plots']
        self.break_bar = '\n{break_ln}\n\n'.format(break_ln='*'*60)
        self.stock_data = None
        super(LoadDataButton, self).__init__(**kwargs)

    def __call__(self):
        pass

    def on_press(self):
        time.sleep(0.3)
        config = ConfigManagement()
        config_data = config.get_data()

        self.update_output(config_data)
        data_download = DataDownload()
        self.base += 'Downloading data...\n'
        self.stock_data = data_download.download()
        self.base += 'Downloading finished.\n'
        self.base += self.break_bar
        self.display.loaded_data = self.stock_data
        self.plots.upload_data(self.stock_data)
        self.plots.generate_price_plot()
        self.plots.generate_volume_plot()
        self.plots.generate_high_low_plot()
        # self.plots.save_diagrams()

    def update_output(self, conf_data):
        self.base.clear_text()
        time.sleep(1)
        self.base += 'Company: {company}\n'.format(**conf_data)
        self.base += 'Date range: {date_from} - ' \
                     '{date_to}\n'.format(**conf_data)
        self.base += 'Regression method: : {regression}\n'.format(**conf_data)
        self.base += self.break_bar

    # def _generate_plot(self):
    #     plots = PlotsGenerate(self.stock_data)
    #     plots.generate_data_plot()