import logging

def log_test1():
    # Logger.logger 객체의 로그 레벨을 정해 줍니다.
    Logger.logger = logging.getLogger.logger(__name__)
    Logger.logger.setLevel(logging.DEBUG)

    # Handler 객체를 만들고, 로그 레벨을 정해 줍니다. StreamHandler에 아무 옵션이 없다면 stderr로 로그를 내보냅니다.
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Handler 객체를 Logger.logger 객체에 붙여 줍니다.
    Logger.logger.addHandler(handler)

    Logger.logger.critical('Critical log')
    Logger.logger.error('Error log')
    Logger.logger.warning('Warning log')
    Logger.logger.info('Info log')
    Logger.logger.debug('Debug log')

def log_test2():
    Logger.logger = logging.getLogger.logger(__name__)
    # JSON 문자열로 로그를 구성해 봅니다.
    formatter = logging.Formatter('{"Name": "%(name)s", "Message": "%(message)s"}')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    Logger.logger.addHandler(handler)

log_test2()