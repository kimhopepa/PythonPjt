# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
import platform
from library_log import *
import cpuinfo
import psutil


# 2) 참조할 lib 파일 추가
# from libConvert import *
# from libConfig import *
# from libFile import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 3) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("HardwareInfo.ui")
form_class = uic.loadUiType(form)[0]


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()

        # 1. UI 이벤트 초기화
        self.setupUi(self)

        # 2. 버튼 이벤트
        self.pushButton_HardwareInfo.clicked.connect(self.get_hardwareInfo)

    # 버튼 이벤트
    def get_hardwareInfo(self):
        try:
            data = cpuinfo.get_cpu_info()
            cpu_info = data['brand_raw']
            logical_process_count = data['count']   # 논리 프로세스 수량
            cpu_info_cores = data['family']         # 코어 수량

            v_memory = psutil.virtual_memory()      # 메모리


            virtual_memory = psutil.virtual_memory()
            str_cpu_info ="cpu info =" + data['brand_raw'] + ", Core = " +  str(cpu_info_cores) + ", Logical Count = " + str(logical_process_count)
            str_memory_info = "memory = " + str(v_memory.total)

            logger.info(str_cpu_info)
            logger.info(str_memory_info)


            self.plainTextEdit.setPlainText(str_cpu_info)
            self.plainTextEdit.appendPlainText(str_memory_info)


        except Exception as e:
            print("get_hardwareInfo()", e)


# 5) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
