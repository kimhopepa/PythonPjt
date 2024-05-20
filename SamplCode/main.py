import os
import configparser
import sys

# import lib
from lib import libLog2
from lib import libConfig

# DEBUG 레벨의 로그를 출력하는 Logger.logger 인스턴스 생성
Logger.logger = libLog.Logger.logger(log_level=libLog.logging.INFO)



def config_read_test1():
    config = configparser.ConfigParser()
    print(os.path.isfile('config.ini'))
    config.read('config.ini', encoding='utf-8')
    config.sections()
    print(config['system']['version'])
    # exit()


def log_test():
    # 로그 출력
    Logger.logger.debug("Debug 메시지")
    Logger.logger.info("Info 메시지")
    Logger.logger.warning("Warning 메시지")
    Logger.logger.error("Error 메시지")
    Logger.logger.critical("Critical 메시지")

def config_read_test2():
    # ConfigHandler 인스턴스 생성
    config_handler = libConfig.ConfigHandler('config.ini')

    # config 파일 읽기
    config = config_handler.read_config()
    # print(config['system']['title'])
    print(config)


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    # config_read_test1()
    log_test()
    config_read_test2()





