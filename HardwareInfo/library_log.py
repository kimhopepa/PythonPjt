import logging

# Logger.logger instance 생성
Logger.logger = logging.getLogger.logger(__name__)

# formatter 생성
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

# handler 생성 (stream, file)
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./test.log')

# Logger.logger instance에 fomatter 설정
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# Logger.logger instance에 handler 설정
Logger.logger.addHandler(streamHandler)
Logger.logger.addHandler(fileHandler)

# Logger.logger instnace로 log 찍기
Logger.logger.setLevel(level=logging.DEBUG)
Logger.logger.debug('my DEBUG log')
Logger.logger.info('my INFO log')
Logger.logger.warning('my WARNING log')
Logger.logger.error('my ERROR log')
Logger.logger.critical('my CRITICAL log')