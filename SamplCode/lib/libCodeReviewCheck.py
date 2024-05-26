import pandas as pd
from lib.libLog import Logger
# from lib import libConfig
from enum import Enum

# config_handler = libConfig.ConfigHandler('config.ini')
# Logger.logger = libLog.Logger.logger(config_level= config_handler.config_dict["system"]["log_level"])

COL_FILE_NAME = "파일 이름"
COL_FILE_PATH = "파일 경로"

COL_CR_CLASS = '구분'
COL_CR_ITEM = '코드 리뷰 항목'
COL_CR_RESULT = '코드 리뷰 결과'


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

    def __init__(self):
        self.count = 0;
        self.df_crc_info = pd.DataFrame(columns=[COL_FILE_NAME, COL_FILE_PATH])
        self.df_crc_result = pd.DataFrame(columns=[COL_CR_ITEM, COL_CR_RESULT])
        self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_ACTIVE}, {COL_CR_RESULT : ROW_CR_RESULT_NONE}, ignore_index=True)
        # self.df_crc_result = pd.DataFrame(columns=['코드 리뷰 항목', '코드 리뷰 결과'])

        #1. DataFrame 데이터 초기화 : 코드 리뷰 체크 항목
        # self.init_check_list()

    def init_check_list(self):
        try:
            self.count += 1
            Logger.debug("CodeReviewCheck.init_check_list Start")
            # new_record = {'A': 4, 'B': 'd'}
            new_record = {COL_CR_ITEM: ROW_CR_ITEM_ACTIVE, COL_CR_RESULT: ROW_CR_RESULT_NONE}
            self.df_crc_result.append(new_record, ignore_index=True)
            df_concat()
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_ACTIVE}, {COL_CR_RESULT : ROW_CR_RESULT_NONE}, ignore_index=True)
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_LOOP}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_EVENT_CHANGE}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_PROPER_DP_FCT}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_DP_QUERY_OPT}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM : ROW_CR_ITEM_RAIMA_UP}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_DB_BIND}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_DB_COMMENT}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_DB_EXCEPTION}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_DP_EXCEPTION}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_TRY_EXCEPTION}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_VERSION}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_CONSTRAINTS}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})
            # self.df_crc_result.append({COL_CR_ITEM: ROW_CR_ITEM_UNNECESSARY_CODE}, {COL_CR_RESULT: ROW_CR_RESULT_NONE})


            # self.df_crc_result.loc[2] = ['이벤트 교환 횟수 최소화', 'None']
            # self.df_crc_result.loc[3] = ['적절한 DP 처리 함수 사용', 'None']
            # self.df_crc_result.loc[4] = ['Raima DB 증가 방지', 'None']
            # self.df_crc_result.loc[5] = ['DB 쿼리 바딩인 처리', 'None']
            # self.df_crc_result.loc[6] = ['DB 쿼리 주석 처리', 'None']
            # self.df_crc_result.loc[7] = ['DB 쿼리 실패 예외 처리', 'None']
            # self.df_crc_result.loc[8] = ['DB 쿼리 실패 예외 처리', 'None']
            # self.df_crc_result.loc[9] = ['DP 함수 예외 처리', 'None']
            # self.df_crc_result.loc[10] = ['DP 함수 예외 처리', 'None']
            # self.df_crc_result.loc[11] = ['Try Catch 예외 처리', 'None']
            # self.df_crc_result.loc[12] = ['스크립트 이력 관리', 'None']
            # self.df_crc_result.loc[13] = ['하드 코드 지양', 'None']
            # self.df_crc_result.loc[14] = ['불필요한 코드 지양', 'None']
        except Exception as e:
            Logger.error("CodeReviewCheck - init_UI2 Exception" + str(e))


    def df_concat(df, data_dict):
        try:
            Logger.Debug("CodeReviewCheck - df_concat")
            new_record = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, new_record], ignore_index=True)



        except Exception as e:
            Logger.error("CodeReviewCheck - df_concat Exception" + str(e))