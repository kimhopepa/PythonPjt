def get_level(config_number):
    return {
        1: "logging.DEBUG",
        2: "logging.INFO",
        3: "logging.WARNING",
        4: "logging.ERROR",
        5: "logging.CRITICAL",
    }.get(config_number,"default")


print(get_level(6))