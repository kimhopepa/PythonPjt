import os.path

import pandas as pd
from lib.libLog import Logger
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from pycparser import parse_file, c_ast
from openpyxl.utils import get_column_letter

import re

# from lib import libConfig
# from enum import Enum
# import traceback
# import openpyxl

# config_handler = libConfig.ConfigHandler('config.ini')
# Logger.logger = libLog.Logger.logger(config_level= config_handler.config_dict["system"]["log_level"])

COL_FILE_NAME = "파일 이름"
COL_FILE_PATH = "파일 경로"

COL_CR_CLASS = '분류'
COL_CR_ITEM = '코드 리뷰 항목'
COL_CR_RESULT = '코드 리뷰 결과'
COL_CR_RESULT_DETAIL = '코드 리뷰 결과 상세 내용'

ROW_CR_RESULT_OK = 'OK'
ROW_CR_RESULT_NG = 'NG'
ROW_CR_RESULT_NONE = 'N/A'
# class COL(Enum) :
#     FileName = 1
#     FilePath = 2

ROW_CR_CLASS_PERFORMANCE = '성능'
ROW_CR_CLASS_DB = 'DB'
ROW_CR_CLASS_STANDARD = '코드 표준'

ROW_CR_ITEM_ACTIVE = '서버 스크립트 Active 감시'
ROW_CR_ITEM_LOOP = 'Loop문내 처리 조건'
ROW_CR_ITEM_EVENT_CHANGE = 'Event 교환 횟수 최소화'
ROW_CR_ITEM_PROPER_DP_FCT = '적절한 DP 처리 함수'
ROW_CR_ITEM_DP_QUERY_OPT = 'DP Query 최적화 구현'
ROW_CR_ITEM_RAIMA_UP = 'RAIMA DB 증가'

ROW_CR_ITEM_DB_BIND = 'DB Query 바인딩 처리'
ROW_CR_ITEM_DB_COMMENT = 'Query 주석 작성'
ROW_CR_ITEM_DB_EXCEPTION = 'DB Query 예외 처리'

ROW_CR_ITEM_DP_EXCEPTION = 'DP 함수 예외 처리'
ROW_CR_ITEM_TRY_EXCEPTION = 'Try/Catch 예외처리'
ROW_CR_ITEM_VERSION = '스크립트 이력 관리'
ROW_CR_ITEM_CONSTRAINTS = '제약 조건 확인'
ROW_CR_ITEM_UNNECESSARY_CODE = '불필요한 코드 지양'





class CodeReviewCheck :
    df_crc_info = pd.DataFrame(columns=[COL_FILE_NAME, COL_FILE_PATH])
    df_crc_result = pd.DataFrame(columns=[COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT, COL_CR_RESULT_DETAIL])

    @staticmethod
    def init_check_list():
        try:
            Logger.debug("CodeReviewCheck.init_check_list Start")
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_ACTIVE, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_LOOP, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_EVENT_CHANGE, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_PROPER_DP_FCT, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_DP_QUERY_OPT, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_PERFORMANCE , COL_CR_ITEM: ROW_CR_ITEM_RAIMA_UP, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_DB, COL_CR_ITEM: ROW_CR_ITEM_DB_BIND, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_DB, COL_CR_ITEM: ROW_CR_ITEM_DB_COMMENT, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_DB, COL_CR_ITEM: ROW_CR_ITEM_DB_EXCEPTION, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_STANDARD, COL_CR_ITEM: ROW_CR_ITEM_DP_EXCEPTION, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_STANDARD, COL_CR_ITEM: ROW_CR_ITEM_TRY_EXCEPTION, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_STANDARD, COL_CR_ITEM: ROW_CR_ITEM_VERSION, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_STANDARD, COL_CR_ITEM: ROW_CR_ITEM_CONSTRAINTS, COL_CR_RESULT: ROW_CR_RESULT_NONE})
            CodeReviewCheck.df_crc_result = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_result, {COL_CR_CLASS:ROW_CR_CLASS_STANDARD, COL_CR_ITEM: ROW_CR_ITEM_UNNECESSARY_CODE, COL_CR_RESULT: ROW_CR_RESULT_NONE})
        except Exception as e:
            Logger.error("CodeReviewCheck.init_check_list - init_UI2 Exception" + str(e))

    @staticmethod
    def get_table_df():
        try:
            Logger.debug("CodeReviewCheck.init_check_list Start")
            return CodeReviewCheck.df_crc_result[[COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT]]
        except Exception as e:
            Logger.error("CodeReviewCheck.get_table_df - Exception" + str(e))

    '''
    function : init_file_list
    args : file_list(UI에서 선택한 파일 리스트)
    detail : UI에서 선택한 파일 정보 클래스 변수에 저장
    return : 없음
    '''
    @staticmethod
    def init_file_list(selected_files):
        try:
            Logger.debug("CodeReviewCheck.init_file_list Start")
            CodeReviewCheck.df_crc_info = CodeReviewCheck.df_crc_info.drop(CodeReviewCheck.df_crc_info.index)
            for index, file_name in enumerate(selected_files) :
                base_name = os.path.basename(file_name)
                CodeReviewCheck.df_crc_info = CodeReviewCheck.df_concat(CodeReviewCheck.df_crc_info,
                                                                          {COL_FILE_NAME: base_name,
                                                                           COL_FILE_PATH: file_name})

        except Exception as e:
            Logger.error("CodeReviewCheck.init_file_list - Exception" + str(e))

    '''
    function : df_concat
    args : cls(클래스 인스턴스), update_df(변경될 DataFrame), new_dict(DataFrame에 추가될 Dictionary)
    detail : Dicionary 데이터를 DataFrame 변수에 저장하여 반환 
    return : 변경된 DataFrame을 반환
    '''
    # DataFrame에서 Dictionary를 추가하여 반환
    @classmethod
    def df_concat(cls, update_df, new_dict):
        try:
            Logger.debug("CodeReviewCheck - df_concat start")
            new_record_df = pd.DataFrame([new_dict])
            update_df = pd.concat([update_df, new_record_df], ignore_index=True)

        except Exception as e:
            Logger.error("CodeReviewCheck.df_concat - Exception" + str(e))
        return update_df

    # 파일 이름에서 확장자를 제거하여 반환
    @staticmethod
    def get_remove_extension(filename):
        try:
            Logger.debug("CodeReviewCheck - get_remove_extension start")
            name, ext = os.path.splitext(filename)
            return name

        except Exception as e:
            Logger.error("CodeReviewCheck.get_remove_extension - Exception" + str(e))


    '''
    function : df_concat
    args : cls(클래스 인스턴스), update_df(변경될 DataFrame), new_dict(DataFrame에 추가될 Dictionary)
    detail : Dicionary 데이터를 DataFrame 변수에 저장하여 반환 
    return : 변경된 DataFrame을 반환
    '''
    # 테이블 Widget 데이터 -> DafaFrame으로 변환
    @staticmethod
    def get_df_to_tablewidget(tb_widget):
        try :
            Logger.debug("CodeReviewCheck.file_export Start")
            #1. Table_Widget -> DataFrame으로 변환
            # 열 헤더 가져오기
            headers = [tb_widget.horizontalHeaderItem(i).text() for i in range(tb_widget.columnCount())]

            # 데이터 가져오기
            data = []
            for row in range(tb_widget.rowCount()):
                row_data = []
                for column in range(tb_widget.columnCount()):
                    item = tb_widget.item(row, column)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # DataFrame으로 변환
            df = pd.DataFrame(data, columns=headers)
            return df

        except Exception as e:
            Logger.error("CodeReviewCheck.file_export - Exception" + str(e))

    # 엑셀 파일저장
    @staticmethod
    def excel_save(save_path, df_table):
        try:
            Logger.debug("CodeReviewCheck - excel_save start")
            #1. 엑셀 워크북 생성
            wb = Workbook()
            ws = wb.active

            #2. DataFrame 데이터 워크북 저장
            for r in dataframe_to_rows(df_table, index=False, header=True):
                ws.append(r)

            #3. 모든 셀 가운데 정렬 및 맞춤
            for row in ws.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(horizontal='center', vertical='center')

            CodeReviewCheck.excel_merge_cell(ws, 'A2', 'A7')
            CodeReviewCheck.excel_merge_cell(ws, 'A8', 'A10')
            CodeReviewCheck.excel_merge_cell(ws, 'A11', 'A15')

            CodeReviewCheck.set_column_width(ws, 1, 20)
            CodeReviewCheck.set_column_width(ws, 2, 40)
            CodeReviewCheck.set_column_width(ws, 3, 30)

            #3-1 Cell 병합
            # 병합할 셀 영역
            # merge_range = 'A2:A7'
            #
            # # 병합된 셀의 값을 첫 번째 셀의 값으로 설정
            # first_cell = ws['A2']
            # value_to_merge = first_cell.value
            # ws.merge_cells(merge_range)
            #
            # # 병합된 셀에 값 설정
            # merged_cell = ws['A2']
            # merged_cell.value = value_to_merge

            #4. 엑셀 파일 저장
            wb.save(save_path)
        except Exception as e:
            Logger.error("CodeReviewCheck.excel_save - Exception" + str(e))
            # print(traceback.format_exc())

    # 엑셀 시트 Cell 병합
    @classmethod
    def excel_merge_cell(cls, ws, start_cell, end_cell):
        try:
            Logger.debug("CodeReviewCheck - excel_merge_cell start")
            # 병합할 셀 영역
            merge_range = f'{start_cell}:{end_cell}'

            # 병합된 셀의 값을 첫 번째 셀의 값으로 설정
            first_cell = ws[start_cell]
            value_to_merge = first_cell.value
            ws.merge_cells(merge_range)

            # 병합된 셀에 값 설정
            merged_cell = ws[start_cell]
            merged_cell.value = value_to_merge
        except Exception as e:
            Logger.error("CodeReviewCheck.excel_merge_cell - Exception" + str(e))
            # print(traceback.format_exc())

    # 엑셀 시트 열 사이즈 설정
    @classmethod
    def set_column_width(cls, sheet, column, width):
        try:
            Logger.debug("CodeReviewCheck - set_column_width start")
            col_letter = get_column_letter(column)
            sheet.column_dimensions[col_letter].width = width
        except Exception as e:
            Logger.error("CodeReviewCheck.set_column_width - Exception" + str(e))

    @staticmethod
    def test_check_code(file_name):
        try:
            pass
        except Exception as e:
            Logger.error("CodeReviewCheck.test_check_code - Exception" + str(e))

    @staticmethod
    def check_code(file_name):
        try :
            #1. 파일 이름으로 Full Path 가져오기
            file_path = CodeReviewCheck.get_file_path(file_name)
            file_path = os.path.normpath(file_path)
            print("test- df_crc_info", CodeReviewCheck.df_crc_info)
            print("test-file_path", file_path)
            ast = parse_file(file_path, use_cpp=True)

            # C 코드 파싱
            # ast = parse_file(filename=file_path,
            #                  use_cpp=True,
            #                  cpp_args=['-E', '-Iutils/fake_libc_include'])
            ast.show()
            print(ast)
            # AST 노드 순회
            # visitor = FuncCallVisitor()
            # visitor.visit(ast)
            # ast_CallVistor()
        except Exception as e:
            Logger.error("CodeReviewCheck.check_version - Exception" + str(e))

    @classmethod
    def get_file_path(cls, file_name):
        file_path = None
        try:
            Logger.debug("CodeReviewCheck - get_file_path start")
            # print("test - get_file_path", cls.df_crc_info[cls.df_crc_info[COL_FILE_NAME] == file_name, COL_FILE_PATH])
            file_path = cls.df_crc_info.loc[cls.df_crc_info[COL_FILE_NAME] == file_name, COL_FILE_PATH].iloc[0]
            return file_path

        except Exception as e:
            Logger.error("CodeReviewCheck.get_file_path - Exception" + str(e))


    # @classmethod
    # def convert_to_python_path(cls, path):
    #     try:
    #         return os.path.normpath(path)
    #     except Exception as e:
    #         Logger.error("CodeReviewCheck.check_version - Exception" + str(e))

    @classmethod
    def ast_CallVistor(cls, node):
        try:
            print(f'Function call: {node.name.name}')
        except Exception as e:
            Logger.error("CodeReviewCheck.check_version - Exception" + str(e))

    '''
    function : add_crc_info
    args : new_dict()
    detail : 전달받은 DataFrame에 Dicionary를 추가하여 반환 
    return : 변경된 DataFrame을 반환
    '''
    @staticmethod
    def add_crc_info(new_dict):
        try :
            pass
            #1. UI에서 선택한 파일


        except Exception as e:
            Logger.error("CodeReviewCheck.add_crc_info -  Exception" + str(e))

class FuncCallVisitor(c_ast.NodeVisitor):
    def visit_FuncCall(self, node):
        print(f'Function call: {node.name.name}')