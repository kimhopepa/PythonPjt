#1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

#2) 참조할 lib 파일 추가
from libConvert import *
from libConfig import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# #2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("BindingQueryConvert.ui")
form_class = uic.loadUiType(form)[0]

# #3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()

        #1. UI 이벤트 초기화
        self.setupUi(self)

        self._converter = ConvertManager()
        self._configer = ConfigManager()

        self.pushButton_Convert.clicked.connect(self.literalConvert)

        self.loadConfig()

    def loadConfig(self):
        try :
            binding_query = self._configer.GetConfigData(self._configer.section_main, self._configer.key_binding_query)
            binding_parameter = self._configer.GetConfigData(self._configer.section_main, self._configer.key_binding_parameter)

            self.plainTextEdit_BindingQuery.setPlainText(binding_query)
            self.plainTextEdit_BindingParameter.setPlainText(binding_parameter)

        except Exception as e:
            print("loadConfig()", e)

    def literalConvert(self):
        try :
            print("literalConvert")

            text_bindingQuery = self.plainTextEdit_BindingQuery.toPlainText()
            text_bindingParameter = self.plainTextEdit_BindingParameter.toPlainText()

            #1. Literal Query 생성
            text_literal_query = self._converter.makeLiteralQuery(text_bindingQuery, text_bindingParameter)
            
            #2. UI의 lineEdit에 저장
            self.plainTextEdit_literalQuery.setPlainText(text_literal_query)
            print(text_bindingQuery, text_bindingParameter)

            self._configer.SaveConfig(self._configer.section_main, self._configer.key_binding_query, text_bindingQuery)
            self._configer.SaveConfig(self._configer.section_main, self._configer.key_binding_parameter, text_bindingParameter)

        except Exception as e:
            print("literalConvert()", e)


#4) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
