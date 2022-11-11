import os
import configparser



print(os.getcwd())

path = os.getcwd() + "\config.ini"

print(path)



#1 설정파일 만들기
config = configparser.ConfigParser()
config['system'] = {}
config['system']['title'] = 'Neural Networks'
config['system']['version'] = '1.2.42'

#1.1 설정 파일만들기
with open('config.ini', 'w', encoding='utf-8') as configfile:
    config.write(configfile)
