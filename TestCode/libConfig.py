import configparser
from time import strftime
import os

#ConfigParser 클래스
# from attr import _config


class ConfigManger:

    section_main = "main"
    key_pw = "pw"
    key_id = "id"
    key_site = "site"
    key_move_url = "move_url"

    def __init__(self):
        self._fileName = "config.ini"

        self._config = configparser.ConfigParser()


    def GetFilePath(self):
        try:
            # config_path = os.getcwd() + self._fileName
            if os.path.isfile(self._fileName) == True :
                self._config.read(self._fileName, encoding='utf-8')
            else :
                print("파일이 없습니다.", self._fileName)

        except Exception as e:
            print("GetFilePath()", e)


    def SaveConfig(self, section, key, text):
        try :
            # 1. section 있는지 확인
            if section in self._config:
                self._config[section][key] = text

            else:
                self._config[section] = {}
                self._config[section][key] = text

            # 2. section 저장 후 config 파일 write
            self.WriteConfig()

        except Exception as e:
            print("SaverConfig() : ", e)
    def WriteConfig(self):
        try :
            with open(self._fileName, 'w', encoding='utf-8') as configfile:
                self._config.write(configfile)

        except Exception as e:
            print("SaverConfig()", e)

    def GetConfigData(self, section, key):
        try:
            result_text = ""
            self._config = configparser.ConfigParser()
            self._config.read('config.ini', encoding='utf-8')
            if section in self._config and key in self._config[section]:
                result_text = self._config[section][key]
                print("GetConfigData() - check ok", section, key)
            else:
                result_text = ""
                print("GetConfigData - NG", section, key)
        except Exception as e:
            print("GetConfigData()", e)

        return result_text

class ConfigManager:
    section_main = "main"
    key_last_path = "last_path"

    def __init__(self):

        self._fileName = "config.ini"
        # 1. config 객체 생성
        self._config = configparser.ConfigParser()

        # 2. ini파일 경로 가져오기
        self._is_exist = self.GetFilePath()

    def GetFilePath(self):
        try:
            self._file_path = os.getcwd() + "\config.ini"
            if os.path.isfile(self._fileName) == True:
                print("file check - ok.", self._file_path)
                self._config.read('config.ini', encoding='utf-8')
            else:
                print("file check - ng.", self._file_path)
        except Exception as e:
            print("GetFilePath()", e)

    def SaveConfig(self, section, key, text):
        try:
            # 1. section 있는지 확인
            if section in self._config:
                self._config[section][key] = text

            else:
                self._config[section] = {}
                self._config[section][key] = text

            self.WriteConfig()

        except Exception as e:
            print("ConfigManager.SaveConfig() Exception", e)

    def WriteConfig(self):
        try:
            with open(self._fileName, 'w', encoding='utf-8') as configfile:
                self._config.write(configfile)

        except Exception as e:
            print("ConfigManager.WriteConfig() Exception", e)

    def GetConfigData(self, section, key):
        try:
            result_text = ""
            self._config = configparser.ConfigParser()
            self._config.read('config.ini', encoding='utf-8')
            if section in self._config and key in self._config[section]:

                result_text = self._config[section][key]
                print("ConfigManager.GetConfigData() ini check ok", section, key)
            else:
                result_text = ""
                print("ConfigManager.GetConfigData() ini check ng", section, key)
        except Exception as e:
            print("GetConfigData()", e)

        return result_text