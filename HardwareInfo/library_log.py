import logging

# logger instance 생성
logger = logging.getLogger(__name__)

# formatter 생성
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

# handler 생성 (stream, file)
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./test.log')

# logger instance에 fomatter 설정
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# logger instance에 handler 설정
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

# logger instnace로 log 찍기
logger.setLevel(level=logging.DEBUG)
logger.debug('my DEBUG log')
logger.info('my INFO log')
logger.warning('my WARNING log')
logger.error('my ERROR log')
logger.critical('my CRITICAL log')