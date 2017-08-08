from mdata import common
from configparser import ConfigParser


class ConfigManagement(object):
    def __init__(self):
        self.config_file = common.CONFIG_FILE
        self.parser = ConfigParser()

    def get_data(self):
        self.parser.read(self.config_file)
        print(dict(self.parser))
