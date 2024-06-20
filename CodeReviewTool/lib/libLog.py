import logging
import traceback

class Logger:
    # Class 정적 변수 선언
    log_file = None
    log_level = None

    # 로거 생성
    logger = logging.getLogger(__name__)

    @staticmethod
    def init(log_file="logfile.log", config_level=1):
        log_format = "%(asctime)s - %(levelname)s - %(message)s"

        # 1. Logger 설정
        Logger.logger.setLevel(config_level)

        # 2. 파일 햄들러 설정
        file_handler = logging.FileHandler(log_file)
        log_level = Logger.getLevel(int(config_level))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))

        # 3. 로거에 설정한 핸들러 추가
        Logger.logger.addHandler(file_handler)

        # 4. 콘솔 핸들러 추가
        # 콘솔 핸들러 생성
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)  # 로그 레벨
        console_handler.setFormatter(logging.Formatter(log_format))  # 로그 레벨
        Logger.logger.addHandler(console_handler)

    @staticmethod
    def getLevel(config_number: int):
        return {
            1: logging.DEBUG,
            2: logging.INFO,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL,
        }.get(config_number, -1)

    @staticmethod
    def debug( message):
        Logger.logger.debug(message)

    @staticmethod
    def info( message):
        Logger.logger.info(message)

    @staticmethod
    def warning( message):
        Logger.logger.warning(message)

    @staticmethod
    def error( message):
        Logger.logger.error(message)
        trace_msg = traceback.format_exc()
        Logger.logger.error(trace_msg)

    @staticmethod
    def critical( message):
        Logger.logger.critical(message)
