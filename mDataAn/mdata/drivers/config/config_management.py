from mdata import common
from configparser import ConfigParser
from configparser import RawConfigParser


class ConfigManagement(object):
    def __init__(self):
        self.config_file = common.CONFIG_FILE
        self.parser = ConfigParser()
        self.section = 'settings'
        self.raw_parser = RawConfigParser()
        self._params = None

    @property
    def params_template(self):
        if self._params is None:
            params = {'temp_dir': ''}
            self._params = params
        return self._params

    def get_data(self):
        self.parser.read(self.config_file)
        data = dict(self.parser._sections[self.section])
        return data

    def set_data(self, data):
        self.raw_parser.add_section(self.section)
        old_data = self.get_data()
        old_data.update(data)

        for name, value in old_data.iteritems():
            self.raw_parser.set(self.section, name, value)

        with open(self.config_file, 'w') as f:
            self.raw_parser.write(f)

if __name__ == '__main__':
    ob = ConfigManagement()
    # print(ob.get_data())
    ob.set_data({'parameter': 'valu2222e'})