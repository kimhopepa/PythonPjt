import os
import configparser



def config_read_test():
    config = configparser.ConfigParser()
    print(os.path.isfile('config.ini'))
    config.read('config.ini', encoding ='utf-8')
    config.sections()
    print(config['system']['version'])
    exit()


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    config_read_test()






# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
