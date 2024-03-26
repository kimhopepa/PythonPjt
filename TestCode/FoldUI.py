# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os


# 2) 참조할 lib 파일 추가
# from libConvert import *
from libConfig import *
from libFile import *

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pandas as pd

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 3) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("Folder_UI.ui")
form_class = uic.loadUiType(form)[0]

class DataFrameTableModel(QStandardItemModel):
    def __init__(self, data, parent=None):
        super(DataFrameTableModel, self).__init__(parent)
        self._data = data

        self.setHorizontalHeaderLabels(data.columns)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QStandardItem(str(data.iloc[i, j]))
                self.setItem(i, j, item)


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()

        # 1. UI 이벤트 초기화
        self.setupUi(self)

        # 라이브러리 객체 생성
        self._configer = ConfigManager()
        self._filer = FileManager()
        
        # 2. 버튼 이벤트
        self.pushButton_Path.clicked.connect(self.set_path)
        self.pushButton_FileList.clicked.connect(self.search_file_list)
        self.pushButton_Search.clicked.connect(self.search_version)

        # 3. tablwWidget 초기화
        # self.setGeometry(100, 100, 600, 400)
        # self.tableWidget_version.setGeometry(50, 50, 500, 300) # 위치 설정
        self.setWindowTitle("DataFrame in QTableView Example")


        # 3. 초기화 함수 실행
        self.loadConfig()

    def search_version(self):
        try:
            print("search_version")

            data = pd.DataFrame({
                'Name': ['Alice', 'Bob', 'Charlie'],
                'Age': [25, 30, 35],
                'Gender': ['Female', 'Male', 'Male']
            })

            # DataFrame을 테이블 위젯에 추가
            # 행, 열 수 설정
            self.tableWidget_version.setRowCount(data.shape[0])
            self.tableWidget_version.setColumnCount(data.shape[1])

            # 헤더 설정
            self.tableWidget_version.setHorizontalHeaderLabels(data.columns)
            self.tableWidget_version.setVerticalHeaderLabels(data.index.astype(str))

            # 데이터 넣기
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    item = QTableWidgetItem(str(data.iloc[i, j]))
                    self.tableWidget_version.setItem(i, j, item)

            # QTableView에도 데이터 추가
            # self.tableWidget_version = QTableView(self)
            # self.tableWidget_version.setGeometry(50, 50, 500, 300)
            #
            # model = DataFrameTableModel(data)
            # self.tableWidget_version.setModel(model)

        except Exception as e:
            print("search_version() Error", e)


    def loadConfig(self):
        try:
            # config.ini 파일에서 last 경로 가져오기
            cfg_last_path = self._configer.GetConfigData(self._configer.section_main, self._configer.key_last_path)

            # last 경로 UI 출력 -> textEdit
            self.lineEdit_Path.setText(cfg_last_path)

        except Exception as e:
            print("loadConfig()", e)

    def set_path(self):
        try:
            print("set_path()")

            # 1. UI에서 화면 열어서 경로 설정 -> Dialog
            folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', '')

            # 2. textEdit에 경로 저장
            self.lineEdit_Path.setText(folder_path)

            # 3. 마지막 경로 config 파일에 저장
            self._configer.SaveConfig(self._configer.section_main, self._configer.key_last_path, folder_path)

            print("folder_path", folder_path)

        except Exception as e:
            print("set_path()", e)

    def search_file_list(self):
        try:
            folder_path = self.lineEdit_Path.text()
            file_list = self._filer.GetPath_fileList(folder_path)
            self.plainTextEdit_FileList.setPlainText('\n'.join(file_list))

        except Exception as e:
            print("set_path()", e)




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
