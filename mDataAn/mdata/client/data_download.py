from pandas_datareader.data import DataReader

from mdata.drivers.config.config_management import ConfigManagement
from mdata.drivers.databases.operations import Operations


class DataDownload(object):
    def __init__(self):
        self.data = None
        self.source = 'yahoo'
        self.config = ConfigManagement()

    def download(self):
        config_data = self.config.get_data()
        company = config_data['company']
        start = config_data['date_from']
        end = config_data['date_to']
        self._prepare_params(company)
        company_data = DataReader(self.data['symbol'], self.source, start, end)
        return company_data

    def _prepare_params(self, company):
        operations = Operations()
        self.data = operations.get_one_record(table='company_info',
                                              name=company)
        if not self.data:
            raise ValueError()