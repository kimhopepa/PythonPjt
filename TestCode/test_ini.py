import configparser
import json


def save_list_to_ini(file_path, section, option, lst):
    config = configparser.ConfigParser()
    config.read(file_path)

    if not config.has_section(section):
        config.add_section(section)

    # 리스트를 JSON 문자열로 변환하여 저장
    config.set(section, option, json.dumps(lst))

    with open(file_path, 'w') as configfile:
        config.write(configfile)


# 사용 예제
file_path = 'config.ini'
section = 'Settings'
option = 'my_list'
lst = [1, 2, 3, 4, 5]

save_list_to_ini(file_path, section, option, lst)


def load_list_from_ini(file_path, section, option):
    config = configparser.ConfigParser()
    config.read(file_path)

    if config.has_section(section) and config.has_option(section, option):
        value = config.get(section, option)
        return json.loads(value)
    return []


# 사용 예제
loaded_list = load_list_from_ini(file_path, section, option)
print(loaded_list)  # 출력 결과: [1, 2, 3, 4, 5]