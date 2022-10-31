import configparser
from time import strftime

config_path = "config.ini"

#ConfigParser 객체 선언
config = configparser.ConfigParser()
path = "adfa"

def inifile_save(section_name, key_name, text) :
    config.read(path)
    #1. section 있는지 확인
    if section_name in config:
        config[section_name][key_name] = text
    else :
        config[section_name] = {}
        config[section_name][key_name] = text

    with open(path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)



def inifile_load(section_name, key_name) :
    result_text = ""
    config.read(path)
    if section_name in config and key_name in config[section_name] :
        result_text = config[section_name][key_name]
    else :
        result_text = ""

    return result_text
