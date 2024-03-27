import configparser

class ConfigHandler:
    def __init__(self, config_file):
        self.config_file = config_file

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config[section])
        return config_dict

    def write_config(self, config_dict):
        config = configparser.ConfigParser()
        for section, options in config_dict.items():
            config[section] = options
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)