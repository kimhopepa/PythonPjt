# 1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import re
import os

# import lib

from lib.libLog import Logger

from lib import libConfig
from lib.libCodeReviewCheck import CodeReviewCheck


# DEBUG 레벨의 로그를 출력하는 Logger.logger 인스턴스 생성

#1. config 파일 조회
config_handler = libConfig.ConfigHandler('config.ini')
#2. config 데이터 변수 저장
# config_handler.read_config()
#3. 로그 등급 확인하여 로거 객체 생성

# Logger.logger = libLog.Logger.logger(config_level= config_handler.config_dict["system"]["log_level"])
Logger.init(config_level=(int)(config_handler.config_dict["system"]["log_level"]))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 3) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("CodeReviewUI.ui")
form_class = uic.loadUiType(form)[0]


# 4) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        # Logger.init(config_level=config_handler.config_dict["system"]["log_level"])
        Logger.info("WindowClass init start")
        super().__init__()
        self.checker = CodeReviewCheck()

        # 1. UI 이벤트 초기화
        self.setupUi(self)
        self.init_UI()

        # self.set_table_widget()

        self.pushButton_Open.clicked.connect(self.UI_OpenPath)

    def init_UI(self):
        try :

            #1. config 파일 조회
            self.folder_path = config_handler.config_dict["Path"]["last_path"]
            if os.path.exists(self.folder_path):
                self.lineEdit_Path.setText(self.folder_path)  # 마지막 파일 선택 경로
                
            Logger.logger.info(self.folder_path)

            #2. 테이블widget에 코드 리뷰 조건 리스트 표시
            self.set_table_widget(self.checker.df_crc_result)

        except Exception as e:
            Logger.logger.error("init_UI Exception" + str(e))

    def UI_OpenPath(self):
        try:
            Logger.logger.debug("UI_OpenPath")

            #1. 파일 선택 -> selected_files 여기 저장
            file_dialog = QFileDialog()

            if os.path.exists(self.folder_path):
                file_dialog.setDirectory(self.folder_path)          # 마지막 파일 선택 경로

            file_dialog.setFileMode(QFileDialog.ExistingFiles)  # 선택한 파일 리스트 조회
            file_dialog.exec_()

            # file_path = file_dialog.getExistingDirectory()
            selected_files = file_dialog.selectedFiles()

            # Logger.logger.debug("UI_OpenPath - File Path = " + file_path)
            Logger.logger.debug("UI_OpenPath - File List = " + (str)(selected_files))

            #2. 선택한 파일 이름 리스트 UI(listWidget_file)에 저장
            for index, file_name in enumerate(selected_files) :
                base_name = os.path.basename(file_name)
                self.listWidget_file.addItem(base_name)
                if index == 0 :
                    last_path = file_name
                    self.folder_path = re.sub( base_name, "", file_name)
                    
            #3. 디렉토리 경로 UI에 저장
            self.lineEdit_Path.setText(self.folder_path)

            #4. 마지막 사용 디텍토리 config 저장
            config_handler.changed_config("Path", "last_path", self.folder_path)

        except Exception as e:
            Logger.logger.error("init_UI Exception" + str(e))

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

            # 크기 조절 정책 설정
            column_ratios = [0.7, 0.3]  # 각 컬럼의 비율을 입력 하세요.
            total_ratio = sum(column_ratios)
            total_width = self.tableWidget.width()
            print(total_ratio, total_width)
            for i, ratio in enumerate(column_ratios) :
                new_width = (int)(total_width * ratio / total_ratio)
                self.tableWidget.setColumnWidth(i, new_width)



            # self.tableWidget.resizeColumnsToContents()
            # self.tableWidget.setColumnWidth(10)
            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # header = self.tableWidget.horizontalHeader()
            # header.setSectionResizeMode(QHeaderView.ResizeToContents)
            # last_col = self.tableWidget.columnCount() - 1
            # print("last_col" + (str)(last_col))
            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # self.tableWidget.resizeColumnsToContents()
            # self.tableWidget.resizeRowsToContents()
            # self.tableWidget.horizontalHeader().setStretchLastSection(True)
            # for col in range(dt_data.shape[1]):
            #     self.tableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
            #
            # last_col = self.tableWidget.columnCount() - 1
            # self.tableWidget.horizontalHeader().setSectionResizeMode(last_col, QHeaderView.Stretch)

            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        except Exception as e:
            Logger.logger.error("set_table_widget Exception " + str(e))


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
