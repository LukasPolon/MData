from datetime import datetime as dt
from copy import deepcopy
from mdata.drivers.config.config_management import ConfigManagement


class PlotsGenerate(object):

    def __init__(self):
        self.data = None
        self.price_data = None
        self.volume_data = None
        self.high_low_data = None
        self.config_mng = ConfigManagement()
        self.unprocessed_plot = None
        self.volume_plot = None
        self.high_low_plot = None
        self.unp_plot_fig = None
        self.volume_plot_fig = None
        self.high_low_fig = None
        self.last_company = None
        self._diagram_names = None

    @property
    def diagram_names(self):
        if self._diagram_names is None:
            current_date = dt.today()
            format_date = '{year}_{month}_{day}_{hour}_{min}_{sec}'\
                          .format(year=current_date.year,
                                  month=current_date.month,
                                  day=current_date.day,
                                  hour=current_date.hour,
                                  min=current_date.minute,
                                  sec=current_date.second)

            names = {'prices_hl': '{company}_hl_prices_{date}.png'
                               .format(company=self.last_company,
                                       date=format_date),
                     'prices_oc': '{company}_oc_prices_{date}.png'
                                    .format(company=self.last_company,
                                            date=format_date),
                     'volume': '{company}_volume_{date}.png'
                               .format(company=self.last_company,
                                       date=format_date)}
            self._diagram_names = names
        return self._diagram_names

    def generate_price_plot(self, *elements):
        """ Generate plot from all data except Volume column"""
        company = self._get_company()
        self.last_company = company
        plot_title = 'Stock prices for '\
                     '{comp}'.format(comp=company)
        try:
            self.price_data = deepcopy(self.data)
            self.price_data = self.data.drop(['Volume', 'High', 'Low',
                                              'Adj Close'], 1)
        except ValueError:
            print('Plot_prices error')

        self.unprocessed_plot = self.price_data.plot(title=plot_title,
                                                     grid=True)
        self.unprocessed_plot.set_ylabel('Value')
        self.unp_plot_fig = self.unprocessed_plot.get_figure()

    def generate_volume_plot(self):
        company = self._get_company()
        self.last_company = company
        plot_title = 'Stock volume for ' \
                     '{comp}'.format(comp=company)
        try:
            self.volume_data = deepcopy(self.data)
            self.volume_data = self.data.drop(['High', 'Low', 'Open', 'Close',
                                               'Adj Close'], 1)
        except ValueError:
            print('Plot_volume error')

        self.volume_plot = self.volume_data.plot(title=plot_title, grid=True)
        self.volume_plot.set_ylabel('Value')
        self.volume_plot_fig = self.volume_plot.get_figure()

    def generate_high_low_plot(self):
        company = self._get_company()
        self.last_company = company
        plot_title = 'Stock volume for ' \
                     '{comp}'.format(comp=company)
        try:
            self.high_low_data = deepcopy(self.data)
            self.high_low_data = self.data.drop(['Volume', 'Open', 'Close',
                                                 'Adj Close'], 1)
        except ValueError:
            print('Plot_volume error')

        self.high_low_plot = self.high_low_data.plot(title=plot_title, grid=True)
        self.high_low_plot.set_ylabel('Value')
        self.high_low_fig = self.high_low_plot.get_figure()

    def get_regression_data(self):
        pass

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

    def save_diagrams(self):
        self.unp_plot_fig.savefig('{dir}\{file}'
                                  .format(dir=self._get_tempdir(),
                                          file=self.diagram_names['prices_oc']))
        self.volume_plot_fig.savefig('{dir}\{file}'
                                     .format(dir=self._get_tempdir(),
                                             file=self.diagram_names['volume']))

        self.high_low_fig.savefig('{dir}\{file}'
                                  .format(dir=self._get_tempdir(),
                                          file=self.diagram_names['prices_hl']))

