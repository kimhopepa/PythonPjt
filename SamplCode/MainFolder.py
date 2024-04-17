# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

# import lib
from lib import libLog
from lib import libConfig
from lib.libFile import *

# DEBUG 레벨의 로그를 출력하는 Logger 인스턴스 생성

#1. config 파일 조회
config_handler = libConfig.ConfigHandler('config.ini')
#2. config 데이터 변수 저장
# config_handler.read_config()
#3. 로그 등급 확인하여 로거 객체 생성
logger = libLog.Logger(config_level= config_handler.config_dict["system"]["log_level"])


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 3) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("FolderUI.ui")
form_class = uic.loadUiType(form)[0]


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QWidget, form_class):
    def __init__(self):
        logger.info("WindowClass init start")
        super().__init__()

# 5) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':

    app = QApplication(sys.argv)
    # QApplication : 프로그램을 실행시켜주는 클래스

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
