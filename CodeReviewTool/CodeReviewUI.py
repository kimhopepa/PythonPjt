# 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from datetime import datetime

import sys
import os

from lib.libConfig import ConfigHandler
from lib.libLog import Logger
from lib.libCodeReviewCheck import *

# DEBUG 레벨의 로그를 출력하는 Logger.logger 인스턴스 생성

# 1. ConfigHandler 클래스 초기화
ConfigHandler.load_config('config.ini')

# 2. Logger 클래스 초기화
Logger.init(config_level=(int)(ConfigHandler.config_dict["system"]["log_level"]))


# 3. Python 배포 파일 생성 코드
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 4. UI 파일 연결 -> 같은 경로에 위치
Mainform = resource_path("CodeReviewUI.ui")
main_form_class = uic.loadUiType(Mainform)[0]

Detailform = resource_path("CodeReviewUI_Detail.ui")
detail_form_class = uic.loadUiType(Detailform)[0]


# 5. Main Form 화면 클래스
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
        self.pushButton_Export.clicked.connect(self.UI_Export)

        # 2-2 UI Table Widget 더블 클릭 이벤트
        self.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)

    # 클래스 UI 초기화
    def init_UI(self):
        try:
            # 1. config 파일 조회
            self.folder_path = ConfigHandler.config_dict["Path"]["last_path"]

            # 1-1. 마지막 파일 경로 UI에 표시
            if os.path.exists(self.folder_path):
                self.lineEdit_Path.setText(self.folder_path)  # 마지막 파일 선택 경로
            Logger.info(self.folder_path)

            # 1-2. 마지막 파일 리스트 UI 리스트 추가
            last_file_list = ConfigHandler.get_config_list("Path", "last_file_list")
            CodeReviewCheck.CodeData.init_file_list(last_file_list)
            df_file = CodeReviewCheck.df_crc_info[[COL_FILE_NAME]]

            #2-1. Table Widget 삭제
            self.tableWidget_File.clearContents()

            #2-2. 테이블widget에 코드 리뷰 항목 DataTable 초기화
            CodeReviewCheck.CodeData.init_check_list()

            # COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT 컬럼 정보만 저장 -> table_df
            table_df = CodeReviewCheck.CodeData.get_tablewidget_df()
            Logger.debug("WindowClass.init_UI - Column info = " + (str)(table_df.columns.tolist()))

            # 3. UI 업데이트
            self.set_table_widget(table_df)         # tablewidget -> 코드 리뷰 항목
            self.set_table_widget_file(df_file)     # tableWidget_File -> 선택한 파일 리스트



            # 창 크기 고정
            self.setFixedSize(self.width(), self.height())

        except Exception as e:
            Logger.error("WindowClass.init_UI Exception" + str(e))

    '''def init_UI(self):
        try:
            # 1. config 파일 조회
            self.folder_path = ConfigHandler.config_dict["Path"]["last_path"]

            # 1-1. 마지막 파일 경로 UI에 표시
            if os.path.exists(self.folder_path):
                self.lineEdit_Path.setText(self.folder_path)  # 마지막 파일 선택 경로

            # 1-2. 마지막 파일 리스트 UI 리스트 추가
            last_file_list = ConfigHandler.get_config_list("Path", "last_file_list")
            self.listWidget_file.clear()
            CodeReviewCheck.CodeData.init_file_list(last_file_list)
            print("last_file_list", last_file_list)

            for index, row in CodeReviewCheck.df_crc_info.iterrows():
                file_name = row[COL_FILE_NAME]
                self.listWidget_file.addItem(file_name)

            Logger.info(self.folder_path)

            # 2. 테이블widget에 코드 리뷰 조건 리스트 표시
            CodeReviewCheck.CodeData.init_check_list()
            table_df = CodeReviewCheck.CodeData.get_table_df()
            Logger.debug("WindowClass.init_UI - Column info = " + (str)(table_df.columns.tolist()))

            # 3. UI 업데이트
            self.set_table_widget(table_df)

            # 창 크기 고정
            self.setFixedSize(self.width(), self.height())

        except Exception as e:
            Logger.error("WindowClass.init_UI Exception" + str(e))'''

    # UI - FileOpen
    def UI_FileOpen(self):
        try:
            Logger.debug("UI_OpenPath")

            # 1. 파일 선택 -> selected_files 여기 저장
            file_dialog = QFileDialog()

            # 2. 마지막에 사용한 폴더 경로 가져오기
            if os.path.exists(self.folder_path):
                file_dialog.setDirectory(self.folder_path)  # 마지막 파일 선택 경로

            # 3. 선택한 파일 리스트 조회
            file_dialog.setFileMode(QFileDialog.ExistingFiles)  # 선택한 파일 리스트 조회
            file_dialog.exec_()

            # 3-1. 선택한 파일들 리스트로 저장
            selected_files = file_dialog.selectedFiles()
            # ini 파일에 저장
            ConfigHandler.changed_config_list("Path", "last_file_list", selected_files)
            Logger.debug("UI_OpenPath - File List = " + (str)(selected_files))

            # 4-1. 선택한 파일 리스트 CodeReviewCheck -> DataFrame(df_crc_info)에 저장
            CodeReviewCheck.CodeData.init_file_list(selected_files)
            df_file = CodeReviewCheck.df_crc_info[[COL_FILE_NAME]]
            self.tableWidget_File.clearContents()
            self.set_table_widget_file(df_file)  # tableWidget_File -> 선택한 파일 리스트

            # 5. 디렉토리 경로 UI에 저장
            self.lineEdit_Path.setText(self.folder_path)

            # 6. 마지막 사용 디텍토리 config 저장
            ConfigHandler.changed_config("Path", "last_path", self.folder_path)
            Logger.debug(CodeReviewCheck.df_crc_result)

        except Exception as e:
            Logger.error("WindowClass.UI_OpenPath Exception" + str(e))

    # UI - Start
    def UI_Start(self):
        try:
            Logger.info("UI_Start")
            #1. TableWidget에서 선택한 레코드 가져오기
            selected_row = self.tableWidget_File.currentRow()
            if selected_row == -1 :
                QMessageBox.information(self, "Warning", "파일을 선택 해주세요. (리뷰 파일을 선택하지 않았습니다.)")
            else :
                selected_file_name = self.tableWidget_File.item(selected_row, 0).text()

            #2. 선택한 파일 이름의 Full 경로 가져오기
            selectced_file_path = CodeReviewCheck.CodeData.get_file_path(selected_file_name)
            Logger.debug("UI_Start - selected file name = " + selected_file_name + ", path = " + selectced_file_path)

            #3. code 문자열로 저장
            text_code = CodeReviewCheck.CodeCheck.get_file_to_text(selectced_file_path)

            #Code(text_code) + Check(SVR, CLI) 정보를 전달하여 코드 리뷰 점검 시작!!!!

            #4. Code Check 실행
            # SVR | CLI 확인하여 코드 리뷰 항목 리스트 가져 오기


            #5. Code 검증 결과 TableWidget 업데이트

            print(text_code)
        except Exception as e:
            Logger.error("WindowClass.UI_Start Exception" + str(e))

    # UI - Export
    def UI_Export(self):
        try:
            Logger.debug("UI_Export")
            # 1. 선택한 파일 가져 오기 (QListWidget)
            select_item = self.listWidget_file.currentItem()

            if select_item is not None:
                # 2. Export 파일 이름 생성
                # 2.1 선택한 파일 이름 조회
                select_file_name = select_item.text()
                # 파일 확장자에서 확장자 제거 -> get_remove_extension
                select_file_name = CodeReviewCheck.CodeData.get_remove_extension(select_file_name)
                format_time = datetime.now().strftime("%Y%m%d%H%M%S")
                select_file_name = select_file_name + "_" + "CodeReivewResult_" + format_time

                options = QFileDialog.Options()
                # options |= QFileDialog.DontUseNativeDialog  # 네이티브 대화 상자 사용 안 함

                # 3. 저장 파일 경로 가져오기 - file_path
                file_path, _ = QFileDialog.getSaveFileName(self, "코드 리뷰 결과 저장", select_file_name,
                                                           "Excel Files (*.xlsx)",
                                                           options=options)

                # 4. TableWidget 데이터 Dataframe 변환
                export_df = CodeReviewCheck.CodeUI.get_df_to_tablewidget(self.tableWidget)

                # 5. 엑셀 파일로 저장
                CodeReviewCheck.CodeUI.excel_save(file_path, export_df)

                print(file_path)
            else:
                QMessageBox.information(self, "Warning", "코드 리뷰 파일을 선택하지 않았습니다.")
        except Exception as e:
            Logger.error("WindowClass.UI_Export Exception" + str(e))

    # table Widget 업데이트
    def set_table_widget(self, dt_data):
        try:
            Logger.debug("WindowClass.set_table_widget : " + dt_data)

            # 1. 행, 열 크기 설정
            self.tableWidget.setRowCount(dt_data.shape[0])
            self.tableWidget.setColumnCount(dt_data.shape[1])

            # 2. 테이블 컬럼 이름 설정 : 분류 | 코드 리뷰 항목 | 코드 리뷰 결과
            self.tableWidget.setHorizontalHeaderLabels(dt_data.columns)

            for i in range(dt_data.shape[0]):
                for j in range(dt_data.shape[1]):
                    item = QTableWidgetItem(str(dt_data.iloc[i, j]))
                    if j == 0 or j == 2:  # 첫 번째 열의 경우에만 가운데 정렬로 설정
                        item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

            # 3. Cell Merge
            self.set_table_merge(0)
            header = self.tableWidget.horizontalHeader()
            header.setDefaultAlignment(Qt.AlignCenter)

            # Apply style sheet to add horizontal line between header and data
            # self.tableWidget.setStyleSheet("QTableWidget::item:selected { background-color: #f27900; }")
            # self.tableWidget.setStyleSheet("QTableView::item { border-Top: 1px solid black; }")
            self.tableWidget.setStyleSheet("""
                    QTableWidget::item:selected { background-color: #f27900; }
                    QTableView::item { border-top: 1px solid black; }
                """)

            # 크기 조절 정책 설정
            column_ratios = [0.3, 0.5, 0.2]  # 각 컬럼의 비율을 입력 하세요.
            total_ratio = sum(column_ratios)
            total_width = self.tableWidget.width()

            for i, ratio in enumerate(column_ratios):
                new_width = (int)(total_width * ratio / total_ratio)
                self.tableWidget.setColumnWidth(i, new_width)

        except Exception as e:
            Logger.error("WindowClass.set_table_widget Exception " + str(e))

    def set_table_widget_file(self, df):
        try:
            Logger.debug("WindowClass.set_table_widget_file : " + df)
            # DataFrame의 행과 열 개수 가져오기
            num_rows, num_cols = df.shape

            # TableWidget의 행과 열 개수 설정
            self.tableWidget_File.setRowCount(num_rows)
            self.tableWidget_File.setColumnCount(num_cols)

            # 컬럼 헤더 설정
            self.tableWidget_File.setHorizontalHeaderLabels(df.columns)

            # DataFrame의 데이터를 TableWidget에 추가
            for i in range(num_rows):
                for j in range(num_cols):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    self.tableWidget_File.setItem(i, j, item)

            header = self.tableWidget_File.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except Exception as e:
            Logger.error("WindowClass.set_table_widget_file Exception " + str(e))

    # table widget에 Dictionary 데이터 넣기
    def set_table_from_dict(self, table_widget, data):
        try:
            Logger.debug("WindowClass.set_table_from_dict : " + data)
            #1. 데이터의 키 목록을 가져와서 열 개수 설정
            column_count = len(data.keys())
            table_widget.setColumnCount(column_count)

            #2.데이터의 키 목록을 열 헤더로 설정
            table_widget.setHorizontalHeaderLabels(data.keys())

            #3.데이터의 값을 테이블에 추가
            row_count = len(next(iter(data.values())))  # 데이터의 첫 번째 값의 길이를 행 개수로 사용
            table_widget.setRowCount(row_count)

            #4. table_widget 업데이트
            for col, key in enumerate(data.keys()):
                values = data[key]
                for row, value in enumerate(values):
                    item = QTableWidgetItem(str(value))  # 데이터를 문자열로 변환하여 QTableWidgetItem 생성
                    table_widget.setItem(row, col, item)
        except Exception as e:
            Logger.error("WindowClass.set_table_from_dict Exception " + str(e))

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

    # table Widget 더블 클릭 이벤트
    def on_cell_double_clicked(self, row, col):
        try:
            col_item_index = 1
            cell_data = self.tableWidget.item(row, col_item_index).text()

            # Detail Form 열기
            if self.second_form is None:
                self.second_form = WindowClass_Detail()


            self.second_form.exec(cell_data)
            # self.second_form.exec()
        except Exception as e:
            Logger.error("WindowClass.on_cell_double_clicked Exception " + str(e))


# 6. Sub Fomr 화면 클래스 - Detail Form
class WindowClass_Detail(QDialog, detail_form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #1. Detail 이벤트 초기화
        self.init_UI()

        Logger.info("WindowClass_Detail init start")

    def exec(self, name):
        try:
            Logger.info("WindowClass_Detail exec() " + name)

            #1. 코드 리뷰 항목 타이블 변경
            self.cr_item = name
            self.setWindowTitle(self.cr_item + "-상세 내용")


            #2. 코드 리뷰 항목에 대한 결과 내용 테이블에 업데이트
            self.tableWidget_detail.clearContents()
            dt_data = CodeReviewCheck.CodeData.get_tablewidget_detail_df(self.cr_item)

            self.set_table_wdgiet_detail(dt_data)

            super().exec()

        except Exception as e:
            Logger.error("WindowClass.exec Exception" + str(e))

    def set_table_wdgiet_detail(self, dt_data):
        try:
            Logger.info("WindowClass_Detail set_table_wdgiet_detail()")
            print(dt_data.shape[0], dt_data.shape[1])
            # 1. 행, 열 크기 설정
            self.tableWidget_detail.setRowCount(dt_data.shape[0])
            self.tableWidget_detail.setColumnCount(dt_data.shape[1])


            # 2. 테이블 컬럼 이름 설정 : '코드 리뷰 항목' | '코드 리뷰 결과' | 'Line' | '상세 내용'
            self.tableWidget_detail.setHorizontalHeaderLabels(dt_data.columns)
            for i in range(dt_data.shape[0]):
                for j in range(dt_data.shape[1]):
                    item = QTableWidgetItem(str(dt_data.iloc[i, j]))
                    if j < 2:  # 첫 번째 열의 경우에만 가운데 정렬로 설정
                        item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_detail.setItem(i, j, item)

            self.tableWidget_detail.setStyleSheet("""
                    QTableWidget::item:selected { background-color: #f27900; }
                    QTableView::item { border-top: 1px solid black; }
                """)

           # 크기 조절 정책 설정
            column_ratios = [0.3, 0.1, 0.2, 0.4]  # 각 컬럼의 비율을 입력 하세요.
            total_ratio = sum(column_ratios)
            total_width = self.tableWidget_detail.width()

            for i, ratio in enumerate(column_ratios):
                new_width = (int)(total_width * ratio / total_ratio)
                self.tableWidget_detail.setColumnWidth(i, new_width)
        except Exception as e:
            Logger.error("WindowClass.exec Exception" + str(e))

    # 클래스 Detail UI 초기화
    def init_UI(self):
        try:
            None

        except Exception as e:
            Logger.error("WindowClass.init_UI Exception" + str(e))

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
