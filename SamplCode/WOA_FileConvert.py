# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

# import lib
from lib import libLog2
from lib import libConfig
from lib.libFile import *

# DEBUG 레벨의 로그를 출력하는 Logger.logger 인스턴스 생성

#1. config 파일 조회
config_handler = libConfig.ConfigHandler('config.ini')
#2. config 데이터 변수 저장
# config_handler.read_config()
#3. 로그 등급 확인하여 로거 객체 생성
Logger.logger = libLog.Logger.logger(config_level= config_handler.config_dict["system"]["log_level"])


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 3) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("WOA_FileConvert.ui")
form_class = uic.loadUiType(form)[0]


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QWidget, form_class):
    def __init__(self):
        Logger.logger.info("WindowClass init start")
        super().__init__()
        self.setupUi(self)

        self.pushButton_FileOpen.clicked.connect(self.UI_Progs)

    def UI_Progs(self):
        try :
            Logger.logger.info("UI_Progs Start")


            #1. 현재 경로 가져오기
            self.folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', config_handler.config_dict["Path"]["last_path"])
            self.lineEdit_Path.setText(self.folder_path)
            config_handler.changed_config("Path", "last_path", self.folder_path)

            #2. 파일 읽기




        except Exception as e :
            Logger.logger.error("UI_Open Exception" + str(e))



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
