# 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

import sys
import re
import os

from lib.libConfig import ConfigHandler
from lib.libLog import Logger
from lib.libCodeReviewCheck import *


# DEBUG 레벨의 로그를 출력하는 Logger.logger 인스턴스 생성

#1. ConfigHandler 클래스 초기화
ConfigHandler.load_config('config.ini')

#2. Logger 클래스 초기화
Logger.init(config_level=(int)(ConfigHandler.config_dict["system"]["log_level"]))

#3. Python 배포 파일 생성 코드
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#4. UI 파일 연결 -> 같은 경로에 위치
Mainform = resource_path("CodeReviewUI.ui")
main_form_class = uic.loadUiType(Mainform)[0]

Detailform = resource_path("CodeReviewUI_Detail.ui")
detail_form_class = uic.loadUiType(Detailform)[0]


#5. Main Form 화면 클래스
class WindowClass(QMainWindow, main_form_class):
    
    # WindowClass 클래스 객체 초기화
    def __init__(self):
        Logger.info("WindowClass init start")
        super().__init__()
        

        # 1. UI 이벤트 초기화
        self.setupUi(self)
        self.init_UI()
        self.second_form = None

        # 2-1 UI 버튼 이벤트
        self.pushButton_Open.clicked.connect(self.UI_FileOpen)
        self.pushButton_Start.clicked.connect(self.UI_Start)


        # 2-2 UI Table Widget 더블 클릭 이벤트
        self.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)

    # 클래스 초기화
    def init_UI(self):
        try :
            #1. config 파일 조회
            self.folder_path = ConfigHandler.config_dict["Path"]["last_path"]

            if os.path.exists(self.folder_path):
                self.lineEdit_Path.setText(self.folder_path)  # 마지막 파일 선택 경로
                
            Logger.info(self.folder_path)
            Logger.info
            #2. 테이블widget에 코드 리뷰 조건 리스트 표시
            CodeReviewCheck.init_check_list()
            table_df = CodeReviewCheck.get_table_df()
            Logger.debug("WindowClass.init_UI - Column info = " + (str)(table_df.columns.tolist()))


            self.set_table_widget(table_df)

            # 창 크기 고정
            self.setFixedSize(self.width(), self.height())

        except Exception as e:
            Logger.error("WindowClass.init_UI Exception" + str(e))

    # UI - FileOpen
    def UI_FileOpen(self):
        try:
            Logger.debug("UI_OpenPath")

            #1. 파일 선택 -> selected_files 여기 저장
            file_dialog = QFileDialog()

            #2. 마지막에 사용한 폴더 경로 가져오기
            if os.path.exists(self.folder_path):
                file_dialog.setDirectory(self.folder_path)          # 마지막 파일 선택 경로
                
            #3. 선택한 파일 리스트 조회
            file_dialog.setFileMode(QFileDialog.ExistingFiles)      # 선택한 파일 리스트 조회
            file_dialog.exec_()

            #3-1. 선택한 파일들 리스트로 저장
            selected_files = file_dialog.selectedFiles()
            Logger.debug("UI_OpenPath - File List = " + (str)(selected_files))

            #4. 선택한 파일 이름 리스트 UI(listWidget_file)에 저장
            self.listWidget_file.clear()
            CodeReviewCheck.init_file_list(selected_files)

            for index, row in CodeReviewCheck.df_crc_info.iterrows():
                file_name = row[COL_FILE_NAME]
                self.listWidget_file.addItem(file_name)
                if index == 0:
                    file_path = row[COL_FILE_PATH]
                    self.folder_path = re.sub( file_name, "", file_path)

            # for index, file_name in enumerate(selected_files) :
            #     base_name = os.path.basename(file_name)
            #     self.listWidget_file.addItem(base_name)
            #     if index == 0 :
            #         last_path = file_name
            #         self.folder_path = re.sub( base_name, "", file_name)
                    
            #5. 디렉토리 경로 UI에 저장
            self.lineEdit_Path.setText(self.folder_path)

            #6. 마지막 사용 디텍토리 config 저장
            ConfigHandler.changed_config("Path", "last_path", self.folder_path)
            Logger.debug(CodeReviewCheck.df_crc_result)

        except Exception as e:
            Logger.error("WindowClass.UI_OpenPath Exception" + str(e))

    # UI - Start
    def UI_Start(self):
        try :
            Logger.debug("UI_Start")

            #1. 현재 선택한 파일 경로 조회
            # file_name =



        except Exception as e:
            Logger.error("WindowClass.UI_Start Exception" + str(e))


    # table Widget 업데이트
    def set_table_widget(self, dt_data):
        try:
            Logger.debug("WindowClass.set_table_widget : " + dt_data)
            # 1. 행, 열 크기 설정
            self.tableWidget.setRowCount(dt_data.shape[0])
            self.tableWidget.setColumnCount(dt_data.shape[1])

            # 2. 테이블 컬럼 이름 설정
            self.tableWidget.setHorizontalHeaderLabels(dt_data.columns)

            for i in range(dt_data.shape[0]):
                for j in range(dt_data.shape[1]):
                    item = QTableWidgetItem(str(dt_data.iloc[i, j]))
                    if j == 0:  # 첫 번째 열의 경우에만 가운데 정렬로 설정
                        item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

            # 3. Cell Merge
            self.set_table_merge(0)
            header = self.tableWidget.horizontalHeader()
            header.setDefaultAlignment(Qt.AlignCenter)

            # Apply style sheet to add horizontal line between header and data
            self.tableWidget.setStyleSheet("QTableView::item { border-Top: 1px solid black; }")
            self.tableWidget.setStyleSheet("QTableWidget::item:selected { background-color: #f27900; }")

            # 크기 조절 정책 설정
            column_ratios = [0.3, 0.5, 0.2]  # 각 컬럼의 비율을 입력 하세요.
            total_ratio = sum(column_ratios)
            total_width = self.tableWidget.width()

            for i, ratio in enumerate(column_ratios) :
                new_width = (int)(total_width * ratio / total_ratio)
                self.tableWidget.setColumnWidth(i, new_width)

        except Exception as e:
            Logger.error("WindowClass.set_table_widget Exception " + str(e))

    # table Widget에서 분류 컬럼을 가운데 정렬
    def set_table_merge(self, column):
        try:
            prevValue = None
            startRow = 0
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, column)
                value = item.text() if item else ""
                if value != prevValue:
                    if startRow != row:
                        self.tableWidget.setSpan(startRow, column, row - startRow, 1)
                    startRow = row
                    prevValue = value
            if startRow != self.tableWidget.rowCount() - 1:
                self.tableWidget.setSpan(startRow, column, self.tableWidget.rowCount() - startRow, 1)
        except Exception as e:
            Logger.error("WindowClass.set_table_merge Exception " + str(e))

    # table Widget 더블클릭 이벤트
    def on_cell_double_clicked(self, row, col):
        try :
            item = self.tableWidget.item(row, col)
            print(item.text())

            # Detail Form 열기
            if self.second_form is None :
                self.second_form = WindowClass_Detail()

            self.second_form.exec()
            # self.second_form.show()

            # self.new_form = NewForm()
            # self.new_form.show()
        except Exception as e:
            Logger.error("WindowClass.on_cell_double_clicked Exception " + str(e))

#6. Sub Fomr 화면 클래스 - Detail Form
class WindowClass_Detail(QDialog, detail_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        Logger.info("WindowClass_Detail init start")


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
