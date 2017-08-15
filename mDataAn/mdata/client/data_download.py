import os
from pandas_datareader.data import DataReader

from mdata.drivers.config.config_management import ConfigManagement
from mdata.drivers.databases.operations import Operations

import mdata.common as common


class DataDownload(object):
    def __init__(self):
        self.data = None
        self.source = 'google'
        self.config = ConfigManagement()

    def download(self):
        config_data = self.config.get_data()
        company = config_data['company']
        start = config_data['date_from']
        end = config_data['date_to']
        self.prepare_params(company)
        company_data = DataReader(self.data['symbol'], self.source, start, end)
        return company_data

    def prepare_params(self, company):
        operations = Operations()
        self.data = operations.get_one_record(table='company_info',
                                              name=company)
        if not self.data:
            raise ValueError


if __name__ == '__main__':
    ob = DataDownload()
    e = ob.download()
    e.plot()
    # d = e.to_dict()
    # date_ = [date.to_pydatetime()
    #          for i, date in enumerate(d['High'].keys())
    #          if i % 2 is 0]
    # date2 = [d for i,d in enumerate(date_) if i % 2 is 0]
    # high = [hi for hi in d['High'].values()]
    # high = [(da.to_pydatetime(), h)
    #         for da, h in d['High'].iteritems()]
    # print(high[0][0])
    # print(type(high[0][0]))
    # high = [(str(date).split(' ')[0], h)
    #         for date, h in d['High'].iteritems()]
    # import pygal

    # xy_chart = pygal.XY()
    # xy_chart.title = 'XY Cosinus'
    # xy_chart.add('high', high)
    # xy_chart.render_to_file('diag.svg')

    # dateline = pygal.DateLine(x_label_rotation=25, stroke=False)
    # dateline.x_labels = date_
    # dateline.add('High', high, show_only_major_dots=True)
    # dateline.render_to_file(os.path.join(common.IMAGES_DIR, 'chart.svg'))