import configparser
#from libLog import Logger
from lib.libLog import Logger

class ConfigHandler:
    config_dict={}
    configer = configparser.ConfigParser()
    file_path = ""

    @classmethod
    def load_config(cls, in_file_path) :
        try:
            cls.file_path = in_file_path
            cls.read_config()

            Logger.info("config File = " + in_file_path)

        except Exception as e:
            Logger.error("ConfigHandler.load_config Exception" + str(e))

    # fuction 이름 :  read_config
    # 타입 : void
    # Args : cls -> 클래스 멤버 변수 참조 객체
    # 내용 : 클래스 함수
    @classmethod
    def read_config(cls):
        try:
            cls.configer.read(cls.file_path, encoding='utf-8')
            for section in cls.configer.sections():
                cls.config_dict[section] = dict(cls.configer[section])
        except Exception as e:
            Logger.error("ConfigHandler.read_config Exception" + str(e))

    @classmethod
    def write_config(cls):
        try:
            with open(cls.file_path, 'w', encoding='utf-8') as configfile:
                cls.configer.write(configfile)

        except Exception as e:
            print("ConfigManager.WriteConfig() Exception", e)

    @staticmethod
    def changed_config(section, key, text):
        try:
            if section in ConfigHandler.configer:
                ConfigHandler.configer[section][key] = text
            else :
                ConfigHandler.configer[section] = {}
                ConfigHandler.configer[section][key] = text

            ConfigHandler.write_config()
            ConfigHandler.read_config()

        except Exception as e:
            Logger.error("ConfigHandler.load_config Exception" + str(e))
