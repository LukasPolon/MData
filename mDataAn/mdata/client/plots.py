from datetime import datetime as dt
from mdata.drivers.config.config_management import ConfigManagement


class PlotsGenerate(object):

    def __init__(self):
        self.data = None
        self.config_mng = ConfigManagement()
        self.unprocessed_plot = None
        self.unp_plot_fig = None
        self.last_company = None

    def generate_data_plot(self):
        """ Generate plot from all data except Volume column"""
        company = self._get_company()
        self.last_company = company
        plot_title = 'Unprocessed stock data '\
                     '({comp})'.format(comp=company)
        try:
            self.data = self.data.drop(['Volume', 'High', 'Low', 'Adj Close'], 1)
        except ValueError:
            pass

        self.unprocessed_plot = self.data.plot(title=plot_title,
                                               grid=True)
        self.unprocessed_plot.set_ylabel('Value')
        self.unp_plot_fig = self.unprocessed_plot.get_figure()
        # self._generate_plot_name()
        # data_fig.savefig('{dir}\plot2.png'.format(dir=self._get_tempdir()))

    def upload_data(self, data):
        self.data = data

    def _get_tempdir(self):
        config_data = self.config_mng.get_data()
        temp_dir = config_data['temp_dir']
        return temp_dir

    def _get_company(self):
        config_data = self.config_mng.get_data()
        company = config_data['company']
        return company

    def _generate_plot_name(self):
        current_date = dt.today()
        filename = ''
