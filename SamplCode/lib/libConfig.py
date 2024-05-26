import configparser

class ConfigHandler:
    def __init__(self, config_file):
        self.config_dict =  {}
        self._config = configparser.ConfigParser()
        self.config_file = config_file
        self.read_config()

    def read_config(self):
        self._config.read(self.config_file, encoding='utf-8')
        for section in self._config.sections():
            self.config_dict[section] = dict(self._config[section])


    # def write_config(self):
    #     config = configparser.ConfigParser()
    #     for section, options in self.config_dict.items():
    #         config[section] = options
    #     with open(self.config_file, 'w') as configfile:
    #         config.write(configfile)

    def changed_config(self, section, key, text):
        # 1. section 있는지 확인
        if section in self._config:
            self._config[section][key] = text

        else:
            self._config[section] = {}
            self._config[section][key] = text

        self.WriteConfig()
        self.read_config()

    def WriteConfig(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                self._config.write(configfile)

        except Exception as e:
            print("ConfigManager.WriteConfig() Exception", e)