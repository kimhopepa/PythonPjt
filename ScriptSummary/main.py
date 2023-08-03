# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

# 2) 참조할 lib 파일 추가
# from libConvert import *
# from libConfig import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# #2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("ScriptSummary_UI.ui")
form_class = uic.loadUiType(form)[0]


# #3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()

        # 1. UI 이벤트 초기화
        self.setupUi(self)

        # 2. 버튼 이벤트 작성
        self.pushButton_path.clicked.connect(self.set_path)

    def set_path(self):
        try :
            print("set_path()")
            folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', '')
            self.textEdit_Path.setText(folder_path)
            print("folder_path", folder_path)

        except Exception as e:
            print("set_path()", e)


# 4) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
