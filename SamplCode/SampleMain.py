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
form = resource_path("SampleUI.ui")
form_class = uic.loadUiType(form)[0]


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        logger.info("WindowClass init start")
        super().__init__()


        # 1. UI 이벤트 초기화
        self.setupUi(self)
        self.pushButton_Open.clicked.connect(self.UI_Open)
        self.pushButton_Search.clicked.connect(self.UI_Search)
        self.pushButton_Version.clicked.connect(self.UI_Version_Check)

        self.init_UI()

    def init_UI(self):
        try :
            self.folder_path = config_handler.config_dict["Path"]["last_path"]
            self.lineEdit_Path.setText(self.folder_path)
            logger.info(self.folder_path)
        except Exception as e:
            logger.error("init_UI Exception" + str(e))

    def UI_Open(self):
        try:
            logger.debug("UI_Open Start")
            # 폴더 선택
            #self.folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', config_handler.config_dict["Path"]["last_path"])

            file_dialog = QFileDialog();
            file_dialog.setFileMode(QFileDialog.ExistingFiles)

            file_dialog.exec_()
            selected_files = file_dialog.selectedFiles()

            for file_name in selected_files :
                print("file name = " + os.path.basename(file_name))

            self.lineEdit_Path.setText(self.folder_path)
            config_handler.chagned_config("Path", "last_path", self.folder_path)

            logger.debug("UI_Open path = " + self.folder_path)

        except Exception as e:
            print("UI_Open Exception", e)
            logger.error("UI_Open Exception" + str(e))

    def UI_Search(self):
        try:
            logger.debug("UI_Open UI_Search")
            file_df = get_folder_file_list_dataframe(self.folder_path)
            print(file_df)

            # 1. 행, 열 크기 설정
            self.tableWidget.setRowCount(file_df.shape[0])
            self.tableWidget.setColumnCount(file_df.shape[1])

            # 2. 테이블 컬럼 이름 설정
            self.tableWidget.setHorizontalHeaderLabels(file_df.columns)

            for i in range(file_df.shape[0]):
                for j in range(file_df.shape[1]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(file_df.iat[i, j])))

            #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Exception as e:
            logger.error("UI_Search Exception " + str(e))

    def UI_Version_Check(self):
        try:
            pass
            logger.debug("UI_Version_Check")
            winccoa_path = "C:\Siemens\Automation\WinCC_OA"
            file_df = get_Winccoa_version(winccoa_path)
            self.set_table_widget(file_df)

        except Exception as e:
            logger.error("UI_Search Exception " + str(e))

    def set_table_widget(self, dt_data):
        try:
            # 1. 행, 열 크기 설정
            self.tableWidget.setRowCount(dt_data.shape[0])
            self.tableWidget.setColumnCount(dt_data.shape[1])

            # 2. 테이블 컬럼 이름 설정
            self.tableWidget.setHorizontalHeaderLabels(dt_data.columns)

            for i in range(dt_data.shape[0]):
                for j in range(dt_data.shape[1]):
                    print(i,j,dt_data.iat[i, j])
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(dt_data.iat[i, j])))

            # for col in range(dt_data.shape[1]):
            #     self.tableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
            #
            # last_col = self.tableWidget.columnCount() - 1
            # self.tableWidget.horizontalHeader().setSectionResizeMode(last_col, QHeaderView.Stretch)

            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
        except Exception as e:
            logger.error("set_table_widget Exception " + str(e))


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
