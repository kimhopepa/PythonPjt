import logging


class Logger:
    def __init__(self, log_file="logfile.log", log_level=logging.INFO):
        self.log_file = log_file
        self.log_level = log_level

        # 로그 출력 포맷 정의
        self.log_format = "%(asctime)s - %(levelname)s - %(message)s"

        # 로거 생성
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        # 파일 핸들러 추가
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(file_handler)

        # 콘솔 핸들러 추가
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)