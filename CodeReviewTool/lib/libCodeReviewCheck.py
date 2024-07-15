import os.path
import json

import pandas as pd
from lib.libLog import Logger
# from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

import re
import chardet

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
COL_CR_LINE = 'Line'
COL_CR_RESULT_DETAIL = '상세 내용'
COL_CR_YN = 'Y/N'

ROW_CR_RESULT_OK = 'OK'
ROW_CR_RESULT_NG = 'NG'
ROW_CR_RESULT_NONE = 'N/A'

ROW_CR_CHECK_ALL = 'ALL'
ROW_CR_CHECK_SVR = 'SVR'
ROW_CR_CHECK_CLI = 'CLI'
ROW_CR_CHECK_NONE = 'NONE'

# class COL(Enum) :
#     FileName = 1
#     FilePath = 2asdf

ROW_CR_CLASS_PERFORMANCE = '성능'
ROW_CR_CLASS_DB = 'DB'
ROW_CR_CLASS_STANDARD = '코드 표준'

# [성능]
# COL_CR_CLASS(분류) | COL_CR_ITEM(코드 리뷰 항목) | COL_CR_RESULT(결과) | COL_CR_LINE(Line) | COL_CR_RESULT_DETAIL(상세 내용) | SVR/CLI
CR_ITEM_IDX = 1
ROW_CR_ITEM_ACTIVE = [ROW_CR_CLASS_PERFORMANCE, '서버 스크립트 Active 감시', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_SVR]
ROW_CR_ITEM_LOOP = [ROW_CR_CLASS_PERFORMANCE, 'Loop문내 처리 조건',  '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_EVENT_CHANGE = [ROW_CR_CLASS_PERFORMANCE, 'Event 교환 횟수 최소화', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_PROPER_DP_FCT = [ROW_CR_CLASS_PERFORMANCE, '적절한 DP 처리 함수','', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_NONE]
ROW_CR_ITEM_DP_QUERY_OPT = [ROW_CR_CLASS_PERFORMANCE, 'DP Query 최적화 구현', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_NONE]
ROW_CR_ITEM_RAIMA_UP = [ROW_CR_CLASS_PERFORMANCE, 'RAIMA DB 증가','', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]

# [DB]
ROW_CR_ITEM_DB_BIND = [ROW_CR_CLASS_DB, 'DB Query 바인딩 처리', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_DB_COMMENT = [ROW_CR_CLASS_DB, 'Query 주석 작성', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_DB_EXCEPTION = [ROW_CR_CLASS_DB, 'DB Query 예외 처리', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]

# [코드 표준]
ROW_CR_ITEM_DP_EXCEPTION = [ROW_CR_CLASS_STANDARD, 'DP 함수 예외 처리', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_SVR]
ROW_CR_ITEM_TRY_EXCEPTION = [ROW_CR_CLASS_STANDARD, 'Try/Catch 예외처리', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_VERSION = [ROW_CR_CLASS_STANDARD, '스크립트 이력 관리', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_SVR]
ROW_CR_ITEM_CONSTRAINTS = [ROW_CR_CLASS_STANDARD, '제약 조건 확인', R'', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_NONE]
ROW_CR_ITEM_HARD_CODE = [ROW_CR_CLASS_STANDARD, '하드코딩 지양', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]
ROW_CR_ITEM_UNNECESSARY_CODE = [ROW_CR_CLASS_STANDARD, '불필요한 코드 지양', '', '', ROW_CR_RESULT_NONE, ROW_CR_CHECK_ALL]

'''
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
'''


class CodeReviewCheck:
    # df_crc_info 컬럼 명 : 파일 이름 | 파일 Full Path
    df_crc_info = pd.DataFrame(columns=[COL_FILE_NAME, COL_FILE_PATH])

    # df_crc_result 컬럼 명 : 구분 | 코드 리뷰 항목 | 코드 리뷰 결과 | Line | 상세 내용 | YN
    df_crc_result = pd.DataFrame(
        columns=[COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT_DETAIL , COL_CR_LINE, COL_CR_RESULT, COL_CR_YN])

    # Data Table 처리 동작
    class CodeData:
        # Data Table 초기화 -> df_crc_result
        @staticmethod
        def init_check_list():
            try:
                Logger.debug("CodeReviewCheck.init_check_list Call")

                #1. Data 모두 삭제
                CodeReviewCheck.df_crc_result.drop(CodeReviewCheck.df_crc_result.index, inplace=True)

                #2. Data 기본 데이터로 저장
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_ACTIVE)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_LOOP)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_EVENT_CHANGE)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_PROPER_DP_FCT)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_DP_QUERY_OPT)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_RAIMA_UP)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_DB_BIND)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_DB_COMMENT)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_DP_EXCEPTION)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_TRY_EXCEPTION)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_VERSION)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_CONSTRAINTS)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_HARD_CODE)
                CodeReviewCheck.df_crc_result = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_result, ROW_CR_ITEM_UNNECESSARY_CODE)

            except Exception as e:
                Logger.error("CodeReviewCheck.init_check_list - Exception : " + str(e))

        # 선택한 파일 리스트를 df 저장 -> df_crc_info ("파일 이름", "파일 전체 경로")
        @staticmethod
        def init_file_list(selected_files):
            try:
                Logger.debug("CodeReviewCheck.init_file_list Start")
                CodeReviewCheck.df_crc_info.drop(CodeReviewCheck.df_crc_info.index, inplace=True)

                for index, file_name in enumerate(selected_files):
                    base_name = os.path.basename(file_name)
                    CodeReviewCheck.df_crc_info = CodeReviewCheck.CodeData.df_concat(CodeReviewCheck.df_crc_info, {COL_FILE_NAME: base_name, COL_FILE_PATH: file_name})


            except Exception as e:
                Logger.error("CodeReviewCheck.init_file_list - Exception : " + str(e))

        # Data Table에서 특정 컬럼 데이터만 가져오기 -> df_crc_result ("분류", "코드 리뷰 항목", 코드 리뷰 결과")
        @staticmethod
        def get_tablewidget_df():
            try:
                Logger.debug("CodeReviewCheck.get_tablewidget_df Start")
                return CodeReviewCheck.df_crc_result[[COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT]]
            except Exception as e:
                Logger.error("CodeReviewCheck.get_tablewidget_df - Exception : " + str(e))

        # Data Table에서 특정 컬럼 데이터만 가져오기 + 조건("코드 리뷰 항목" == cr_item_name) -> df_crc_result ("코드 리뷰 항목","상세 내용", "코드 리뷰 결과", "위치")
        @staticmethod
        def get_tablewidget_detail_df(cr_item_name):
            try:
                Logger.debug("CodeReviewCheck.get_tablewidget_detail_df Start")
                return CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item_name,
                                                         [COL_CR_ITEM, COL_CR_RESULT_DETAIL, COL_CR_LINE, COL_CR_RESULT]]
            except Exception as e:
                Logger.error("CodeReviewCheck.get_tablewidget_detail_df - Exception : " + str(e))

        @staticmethod
        def get_dict_from_list(input_list, key="selectedList"):
            try:
                Logger.debug("CodeReviewCheck.get_dict_from_list Start")
                result_dict = {}

                for item in input_list:
                    result_dict[key] = item

                return result_dict
            except Exception as e:
                Logger.error("CodeReviewCheck.get_dict_from_list - Exception : " + str(e))

        # DataFrame에서 Dictionary를 추가 하여 반환
        @classmethod
        def df_concat(cls, update_df, new_list):
            try:
                Logger.debug("CodeReviewCheck - df_concat Call" + str(new_list))
                # new_record_df = pd.DataFrame([new_dict])
                # update_df = pd.concat([update_df, new_record_df], ignore_index=True)
                update_df.loc[len(update_df)] = new_list

            except Exception as e:
                Logger.error("CodeReviewCheck.df_concat - Exception : " + str(e))
            return update_df

        # 파일 이름에서 확장자를 제거하여 반환
        @staticmethod
        def get_remove_extension(filename):
            try:
                Logger.debug("CodeReviewCheck - get_remove_extension start")
                name, ext = os.path.splitext(filename)
                return name

            except Exception as e:
                Logger.error("CodeReviewCheck.get_remove_extension - Exception : " + str(e))

        @classmethod
        def get_file_path(cls, file_name):
            file_path = None
            try:
                Logger.debug("CodeReviewCheck - get_file_path start")
                file_path = CodeReviewCheck.df_crc_info[CodeReviewCheck.df_crc_info[COL_FILE_NAME] == file_name][COL_FILE_PATH].iloc[0]
                return file_path

            except Exception as e:
                Logger.error("CodeReviewCheck.get_file_path - Exception : " + str(e))


    # UI 관련 동작 구현
    class CodeUI:
        '''
        function : df_concat
        args : cls(클래스 인스턴스), update_df(변경될 DataFrame), new_dict(DataFrame에 추가`````````````````````````````````````````될 Dictionary)
        detail : Dicionary 데이터를 DataFrame 변수에 저장하여 반환
        return : 변경된 DataFrame을 반환
        '''

        # 테이블 Widget 데이터 -> DafaFrame으로 변환
        @staticmethod
        def get_df_to_tablewidget(tb_widget):
            try:
                Logger.debug("CodeReviewCheck.file_export Start")
                # 1. Table_Widget -> DataFrame으로 변환
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
                Logger.error("CodeReviewCheck.file_export - Exception : " + str(e))

        # 엑셀 파일저장
        @staticmethod
        def excel_save(save_path, df_table):
            try:
                Logger.debug("CodeReviewCheck - excel_save start")
                # 1. 엑셀 워크북 생성
                wb = Workbook()
                ws = wb.active

                # 2. DataFrame 데이터 워크북 저장
                for r in dataframe_to_rows(df_table, index=False, header=True):
                    ws.append(r)

                # 3. 모든 셀 가운데 정렬 및 맞춤
                for row in ws.iter_rows():
                    for cell in row:
                        cell.alignment = Alignment(horizontal='center', vertical='center')

                CodeReviewCheck.CodeUI.excel_merge_cell(ws, 'A2', 'A7')
                CodeReviewCheck.CodeUI.excel_merge_cell(ws, 'A8', 'A9')
                CodeReviewCheck.CodeUI.excel_merge_cell(ws, 'A10', 'A15')

                CodeReviewCheck.CodeUI.set_column_width(ws, 1, 20)
                CodeReviewCheck.CodeUI.set_column_width(ws, 2, 40)
                CodeReviewCheck.CodeUI.set_column_width(ws, 3, 30)

                # 3-1 Cell 병합
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

                # 4. 엑셀 파일 저장
                wb.save(save_path)
            except Exception as e:
                Logger.error("CodeReviewCheck.excel_save - Exception : " + str(e))
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
                Logger.error("CodeReviewCheck.excel_merge_cell - Exception : " + str(e))
                # print(traceback.format_exc())

        # 엑셀 시트 열 사이즈 설정
        @classmethod
        def set_column_width(cls, sheet, column, width):
            try:
                Logger.debug("CodeReviewCheck - set_column_width start")
                col_letter = get_column_letter(column)
                sheet.column_dimensions[col_letter].width = width
            except Exception as e:
                Logger.error("CodeReviewCheck.set_column_width - Exception : " + str(e))

        @classmethod
        def get_export_df(cls):
            try :
                Logger.debug("CodeReviewCheck.get_export_df Call")
                export_df = CodeReviewCheck.df_crc_result[
                    [COL_CR_CLASS, COL_CR_ITEM, COL_CR_RESULT, COL_CR_LINE, COL_CR_RESULT_DETAIL]]
                return export_df
            except Exception as e:
                Logger.error("CodeReviewCheck.set_column_width - Exception : " + str(e))


    # 코드 리뷰 검증 기능 구현 클래스
    class CodeCheck:
        @classmethod
        def removed_comments(cls, code):
            try:
                # 한 줄 주석 제거
                code = re.sub(r'//.*', '', code)

                # 여러 줄 주석 제거
                code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

                # 여러 줄 주석 내의 모든 행 삭제
                code = re.sub(r'(/\*.*?\*/)', lambda x: '\n' * x.group(0).count('\n'), code, flags=re.DOTALL)

                return code
            except Exception as e:
                Logger.error("CodeReviewCheck.test_check_code - Exception : " + str(e))

        # 파일을 읽어서 텍스트 반환
        @staticmethod
        def get_file_to_text(file_path):
            try:
                # 파일의 인코딩 확인
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    encoding = chardet.detect(raw_data)['encoding']

                # 파일 읽기
                with open(file_path, 'r', encoding=encoding) as file:
                    file_text = file.read()
                return file_text
            except FileNotFoundError:
                Logger.error("CodeReviewCheck.test_check_code - File Not found" + file_path)
            except Exception as e:
                Logger.error("CodeReviewCheck.test_check_code - Exception : " + str(e))
                return None

        @staticmethod
        def save_to_file(content : str, file_name : str , dict_content : dict = None ):
            try :

                # 최대 열 너비 설정 (기본값: 50)
                pd.set_option('display.max_colwidth', None)

                # 생략 표시 비활성화
                pd.set_option('display.max_rows', None)  # 모든 행 출력
                pd.set_option('display.max_columns', None)  # 모든 열 출력
                path = os.path.join(os.getcwd(), file_name + ".txt")
                if dict_content is not None :
                    content = json.dumps(dict_content, ensure_ascii=False, indent=4)

                with open(path, 'w') as file:
                    file.write(content)
            except Exception as e:
                Logger.error("CodeReviewCheck.CodeUI - Exception : " + str(e))

        @classmethod
        def update_result_df(cls, cr_item : str , check_result : str, check_detail : list ):
            try:
                Logger.debug("CodeCheck.update_result_df - Start")
                cr_result_df = CodeReviewCheck.df_crc_result
                
                # 코드 리뷰 점검 항목 결과 동작
                for list_data in check_detail :
                    list_line = list_data[0]
                    list_detail = list_data[1]

                    item_indx = cr_result_df.index[cr_result_df[COL_CR_ITEM] == cr_item].tolist()[0]    # item index 검색
                    new_data = cr_result_df.loc[cr_result_df[COL_CR_ITEM] == cr_item].copy()            # item record 복사
                    cr_result_df = cr_result_df.drop(item_indx)                                         # item index 삭제

                    # row_data 업데이트
                    new_data[COL_CR_LINE] = list_line
                    new_data[COL_CR_RESULT_DETAIL] = list_detail
                    CodeReviewCheck.df_crc_result = pd.concat([cr_result_df.loc[:item_indx],new_data, cr_result_df.loc[item_indx+1:]], ignore_index=True)

            except Exception as e:
                Logger.error("CodeCheck.update_result_df - Exception : " + str(e))

        @staticmethod
        def code_check_start( file_name : str , check_svr : bool) -> pd.DataFrame :
            try:
                #1. Load Code File
                file_path = CodeReviewCheck.CodeData.get_file_path(file_name)  # 파일 Full 경로 가져오기
                text_code = CodeReviewCheck.CodeCheck.get_file_to_text(file_path)  # 파일 코드 불러와서 문자열 변수 저장

                # 모두 해당되는 코드 리뷰 항목
                CodeReviewCheck.CodeCheck.code_check_UnnecessaryCode(text_code, ROW_CR_ITEM_UNNECESSARY_CODE[CR_ITEM_IDX])

                # Code + 코드 리뷰 아이템 정보 전달 -> 코드 리뷰  진행 후 해당 DataFrame에 결과 저장하여 반환
                if (check_svr == True):
                    Logger.info("CodeCheck.code_check_start(SVR)")
                    # SVR에서만 점검하는 코드 리뷰 항목
                    CodeReviewCheck.CodeCheck.code_check_version(text_code, ROW_CR_ITEM_VERSION[CR_ITEM_IDX])
                    None
                else:
                    Logger.info("CodeCheck.code_check_start(CLI)")
                    # Client에서만 점검하는 코드 리뷰 항목
                    None




                # 1. 불필요한 코드 지양 : 스크립트 파일 + 체크 ITEM
                # 2. 하드코딩 지양
                #  결과

                # return CodeReviewCheck.df_crc_result
            except Exception as e:
                Logger.error("CodeReviewCheck.test_check_code - Exception : " + str(e))

        # [코드 표준] 불필요한 코드 지양 -> SVR
        @classmethod
        def code_check_UnnecessaryCode(cls, text_code : str, cr_item : str) -> tuple:
            try:
                Logger.debug("CodeCheck.code_check_UNUSED - Start")
                result = ROW_CR_RESULT_OK
                result_data = []

                # 0. 주석 코드 삭제
                new_text_code = CodeReviewCheck.CodeCheck.removed_comments(text_code)
                CodeReviewCheck.CodeCheck.save_to_file(new_text_code, "[Step1] removed_comments")


                # 1. 함수이름, Body 부분을 분리하여 Dictionary에 저장 : key -> Function 이름, value -> body
                # 함수 이름을 -> Key 로 저장 | 함수 Body -> Value로 저장
                code_dict = CodeReviewCheck.CodeCheck.extract_functions_from_code(new_text_code)
                CodeReviewCheck.CodeCheck.save_to_file("", "[Step2] Function&Body", code_dict)

                # 2. Global 변수 저장 -> List 저장
                global_vars = CodeReviewCheck.CodeCheck.extract_global_variables(new_text_code)
                CodeReviewCheck.CodeCheck.save_to_file(str(global_vars), "[Step3] GlobalVariable")

                # 3. Global 변수 사용 체크



                # 3-1. 미사용 변수 찾기
                # 3-2. 미사용 함수 찾기


                # [Result] 코드 리뷰 결과 DafaFrame 업데이트
                return result, result_data
            except Exception as e:
                Logger.error("CodeCheck.test_check_code - Exception : " + str(e))

        # [코드 표준] 스크립트 이력 관리 -> SVR
        @classmethod
        def code_check_version(cls, text_code, cr_item)  :
            try :
                #1. 버전 이력 관리 변수 확인
                version_variable_list = ["g_script_release_version", "g_script_release_date"]
                check_result = True
                for list_item in version_variable_list :
                    if CodeReviewCheck.CodeCheck.is_variable_used(text_code, list_item) :
                        Logger.info("CodeReviewCheck.code_check_version - Check OK. " + list_item)
                    else :
                        check_result = False
                        Logger.error("CodeReviewCheck.code_check_version - Check NG. " + list_item)

                ng_detail_msg = "스크립트 이력이 설정되어 있지 않습니다. (g_script_release_version, g_script_release_date)"

                # DataTable 업데이트
                if check_result == True :
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_RESULT] = ROW_CR_RESULT_OK
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_LINE] = "-"
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_RESULT_DETAIL] = ""
                if check_result == False :
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_RESULT] = ROW_CR_RESULT_NG
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_LINE] = "-"
                    CodeReviewCheck.df_crc_result.loc[CodeReviewCheck.df_crc_result[COL_CR_ITEM] == cr_item, COL_CR_RESULT_DETAIL] = ng_detail_msg

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_version - Exception : " + str(e))

        # [코드 표준] 하드 코딩 지양 -> 공통
        @classmethod
        def code_check_hardcoding(cls, text_code):
            try :
                # 스크립트에서 함수 확인



                None
            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [코드 표준] Try, Catch 예외 처리 -> 공통
        @classmethod
        def code_check_hardcoding(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [코드 표준] DP 함수 예외 처리 -> 공통
        @classmethod
        def code_check_hardcoding(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [성능] 스크립트 동작 Active 감시 적용
        @classmethod
        def code_check_hardcoding(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [성능] Loop문 내 처리조건 확인
        @ classmethod
        def code_check_hardcoding(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [성능] 이벤트 교환 횟수 최소화
        @ classmethod
        def code_check_eventminimize(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [성능] 적절한 DP 함수 사용
        @ classmethod
        def code_check_callback(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        # [성능] Raima DB 증가 방지
        @ classmethod
        def code_check_raimaDB(cls, text_code):
            try:
                None

            except Exception as e:
                Logger.error("CodeReviewCheck.code_check_hardcoding - Exception : " + str(e))

        @classmethod
        def extract_functions_from_code(cls, text):
            try:
                function_dict = {}

                # 함수 이름과 본문을 찾는 정규 표현식
                # pattern = re.compile(r'(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)
                pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'

                # matches에서는 1번 캡처는 함수이름 2번 캠처는 body 부분입니다.
                matches = re.finditer(pattern, text, re.DOTALL)
                results = []

                for match in matches:
                    function_name = match.group(1)
                    function_body = match.group(2)
                    start_pos = match.start()
                    end_pos = match.end()
                    start_line = __class__.calculate_line_number(text, start_pos)
                    end_line = __class__.calculate_line_number(text, end_pos)
                    results.append((function_name, function_body, start_line, end_line))

                return function_dict
            except Exception as e:
                Logger.error("CodeReviewCheck.extract_functions_from_code - Exception : " + str(e))

        @classmethod
        def calculate_line_number(cls, text, index):
            try :
                return text.count('\n', 0, index) + 1
            except Exception as e:
                Logger.error("CodeReviewCheck.calculate_line_number - Exception : " + str(e))

        @classmethod
        def remove_comments(cls, code: str) -> str:
            try:
                # 라인 주석 제거
                code = re.sub(r'//.*', '', code)
                # 블록 주석 제거
                code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

                return code
            except Exception as e:
                Logger.error("CodeReviewCheck.remove_comments - Exception : " + str(e))

        # 전역 변수 찾기
        @staticmethod
        def extract_global_variables(code: str) -> list:
            try:

                # . 중괄호 내용(함수 정의 등)을 제외하고 전역 영역의 코드만 추출
                # 1. 주석 삭제
                code = __class__.remove_comments(code)

                # 2. 함수 영여 제거
                code_without_braces = __class__.extract_global_scope_code(code)
                # code_without_braces = re.sub(r'{[^{}]*}', '', code_without_braces)

                # 3. 라인 별로 처리하여 주석 제거
                lines = code_without_braces.split('\n')
                lines_without_comments = [re.sub(r'//.*', '', line).strip() for line in lines if
                                          '//' in line or line.strip() != '']


                # 전역 변수를 찾기 위한 정규식 패턴: 세미콜론으로 끝나는 모든 선언 찾기
                pattern = re.compile(r'\b(\w+)\s*([^;]+);')

                global_variables = []

                for line in lines_without_comments:
                    matches = pattern.finditer(line)
                    for match in matches:
                        # 변수 이름만 추출
                        variables_part = match.group(2)
                        # 쉼표로 구분된 여러 변수 처리
                        variables = [var.split('=')[0].strip() for var in variables_part.split(',')]
                        global_variables.extend(variables)

                return global_variables
            except Exception as e:
                Logger.error("CodeReviewCheck.extract_global_variables - Exception : " + str(e))

        # 전역 코드 영역만 찾기
        @classmethod
        def extract_global_scope_code(cls, code: str) -> str:
            # 괄호 안의 내용(지역 영역)을 제외하고 전역 영역의 코드만을 추출
            nested_braces_pattern = re.compile(r'{[^{}]*}')
            while re.search(nested_braces_pattern, code):
                code = re.sub(nested_braces_pattern, '', code)
            return code

        # 코드에서 변수 선언 확인
        @classmethod
        def is_variable_used(cls, script_code : str, variable_name : str) -> bool:
            try:
                # \b : 단어 경계, escape : 특수문자 이스케이프 처리, \s* : 변수 이름 뒤 공백, (?:=|;|,) : "=",  ";", "," 문자 포함
                pattern = re.compile(r'\b' + re.escape(variable_name) + r'\b\s*(?:=|;|,)')

                # Search for the pattern in the code
                if re.search(pattern, script_code):
                    return True
                return False

            except Exception as e:
                Logger.error("CodeReviewCheck.extract_global_variables - Exception : " + str(e))

        # 변수의 값 확인
        def get_variable_value(c_code, variable_name):

            #1. 전달한 변수 정규식 생성 :
            pattern = re.compile(r'\b' + re.escape(variable_name) + r'\b\s*=\s*("[^"]*"|\d+|[^,;]+)')

            # Search for the pattern in the code
            match = re.search(pattern, c_code)
            if match:
                return match.group(1).strip()
            return None 

    @staticmethod
    def add_crc_info(new_dict):
        try:
            pass
            # 1. UI에서 선택한 파일


        except Exception as e:
            Logger.error("CodeReviewCheck.add_crc_info -  Exception : " + str(e))
