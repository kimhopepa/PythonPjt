import os.path

import pandas as pd
from lib.libLog import Logger

from pycparser import parse_file, c_ast
# from lib import libConfig
from enum import Enum

# config_handler = libConfig.ConfigHandler('config.ini')
# Logger.logger = libLog.Logger.logger(config_level= config_handler.config_dict["system"]["log_level"])

COL_FILE_NAME = "파일 이름"
COL_FILE_PATH = "파일 경로"

COL_CR_CLASS = '분류'
COL_CR_ITEM = '코드 리뷰 항목'
COL_CR_RESULT = '코드 리뷰 결과'
COL_CR_RESULT_DETAIL = '코드 리뷰 결과 상세 내용'


ROW_CR_RESULT_NONE = 'NONE'
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
    detail : 전달받은 DataFrame에 Dicionary를 추가하여 반환 
    return : 변경된 DataFrame을 반환
    '''
    @classmethod
    def df_concat(cls, update_df, new_dict):
        try:
            Logger.debug("CodeReviewCheck - df_concat start")
            new_record_df = pd.DataFrame([new_dict])
            update_df = pd.concat([update_df, new_record_df], ignore_index=True)

        except Exception as e:
            Logger.error("CodeReviewCheck.df_concat - Exception" + str(e))
        return update_df

    @staticmethod
    def check_code(cls, file_path):
        try :
            # C 코드 파싱
            ast = parse_file(filename=file_path,
                             use_cpp=True,
                             cpp_args=['-E', '-Iutils/fake_libc_include'])

            print(ast)
            # AST 노드 순회
            # visitor = FuncCallVisitor()
            # visitor.visit(ast)
            # ast_CallVistor()
        except Exception as e:
            Logger.error("CodeReviewCheck.check_version - Exception" + str(e))

    @classmethod
    def ast_CallVistor(cls, node):
        try:
            print(f'Function call: {node.name.name}')
        except Exception as e:
            Logger.error("CodeReviewCheck.check_version - Exception" + str(e))


    # 함수 이름 :
    # 전달 파라미터 :
    # return :
    # 기능 :
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