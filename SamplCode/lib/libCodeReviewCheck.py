import pandas as pd
from lib import libLog
from lib import libConfig

config_handler = libConfig.ConfigHandler('config.ini')
logger = libLog.Logger(config_level= config_handler.config_dict["system"]["log_level"])





class CodeReviewCheck :
    def __init__(self):
        self.df_crc = pd.DataFrame(columns=[""])
        self.df_crc_result = pd.DataFrame(columns=["코드리뷰항목", "결과"])
        
        #1. DataFrame 데이터 초기화 : 코드 리뷰 체크 항목
        self.init_check_list()

    def init_check_list(self):
        try:
            logger.debug("CodeReviewCheck.init_check_list Start")
            self.df_crc.result.loc[0] =['서버 스크립트 Active 감시', 'None']
            self.df_crc.result.loc[1] = ['Loop문내 처리 조건', 'None']
            self.df_crc.result.loc[2] = ['이벤트 교환 횟수 최소화', 'None']
            self.df_crc.result.loc[3] = ['적절한 DP 처리 함수 사용', 'None']
            self.df_crc.result.loc[4] = ['Raima DB 증가 방지', 'None']
            self.df_crc.result.loc[5] = ['DB 쿼리 바딩인 처리', 'None']
            self.df_crc.result.loc[6] = ['DB 쿼리 주석 처리', 'None']
            self.df_crc.result.loc[7] = ['DB 쿼리 실패 예외 처리', 'None']
            self.df_crc.result.loc[8] = ['DB 쿼리 실패 예외 처리', 'None']
            self.df_crc.result.loc[9] = ['DP 함수 예외 처리', 'None']
            self.df_crc.result.loc[10] = ['DP 함수 예외 처리', 'None']
            self.df_crc.result.loc[11] = ['Try Catch 예외 처리', 'None']
            self.df_crc.result.loc[12] = ['스크립트 이력 관리', 'None']
            self.df_crc.result.loc[13] = ['하드 코드 지양', 'None']
            self.df_crc.result.loc[14] = ['불필요한 코드 지양', 'None']
        except Exception as e:
            logger.error("init_UI Exception" + str(e))
