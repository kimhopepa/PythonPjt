import logging

def log_test1():
    # Logger 객체의 로그 레벨을 정해 줍니다.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Handler 객체를 만들고, 로그 레벨을 정해 줍니다. StreamHandler에 아무 옵션이 없다면 stderr로 로그를 내보냅니다.
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Handler 객체를 Logger 객체에 붙여 줍니다.
    logger.addHandler(handler)

    logger.critical('Critical log')
    logger.error('Error log')
    logger.warning('Warning log')
    logger.info('Info log')
    logger.debug('Debug log')

def log_test2():
    logger = logging.getLogger(__name__)
    # JSON 문자열로 로그를 구성해 봅니다.
    formatter = logging.Formatter('{"Name": "%(name)s", "Message": "%(message)s"}')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

log_test2()