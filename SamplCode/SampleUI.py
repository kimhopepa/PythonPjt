#1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
from lib.libConfig import *
from lib.libLog import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import pandas as pd



def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(   os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# #2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("SampleUI.ui")
form_class = uic.loadUiType(form)[0]

# #3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        # 라이브러리 객체 생성
        self._configer = ConfigManager()
        self._loger = LogManager()

        self.init()
        #1. UI 이벤트 초기화
        self.setupUi(self)

        # 2. UI 객체 연결하기 : 객체 이름 -> pushButton
        self.pushButton_OpenPath.clicked.connect(self.OpenPathEvent)


        # 3. TableWidget 초기화
        print("TableWidget1 test")
        self.setDataFrame()

    def setDataFrame(self):
        try:
            # Create a Pandas DataFrame
            data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
                    'Age': [25, 30, 35, 40],
                    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}
            df = pd.DataFrame(data)

            self.tableWidget.setRowCount(df.shape[0])
            self.tableWidget.setColumnCount(df.shape[1])

            # Set column headers
            self.tableWidget.setHorizontalHeaderLabels(df.columns)

            # Insert data into the table
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    self.tableWidget.setItem(i, j, item)

            # Resize the TableWidget based on content
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

            # Set TableWidget as central widget of the window
            # self.setCentralWidget(self.tableWidget)

        except Exception as e:
            print("setDataFrame", e)


    def init(self):
        self.orgin_path = self._configer.GetConfigData(self._configer.section_main, self._configer.key_last_path)
        print('test', self.orgin_path)

    def OpenPathEvent(self):
        try:
            print("pushButton Event")

            # 1. UI에서 화면 열어서 경로 설정 -> Dialog
            print('pushButton Event2', self.orgin_path)
            folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', self.orgin_path)


            # 2. textEdit에 경로 저장
            self.lineEdit_path.setText(folder_path)

            # 3. ini 파일에 최근 경로 저장
            self._configer.SaveConfig(self._configer.section_main, self._configer.key_last_path, folder_path)


        except Exception as e:
            print("pushButton Event", e)

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
