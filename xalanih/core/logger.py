import logging

class Logger:
    
    def __init__(self, logfile, verbosity):
        level = self.__get_log_level(verbosity)
        self.pythonLogger = logging.getLogger("xalanih")
        self.pythonLogger.setLevel(logging.DEBUG)
        self.pythonLogger.addHandler(self.__get_console_handler(level))
        if logfile != None:
            self.pythonLogger.addHandler(self.__get_file_handler(logfile))

    def error(self, msg):
        self.pythonLogger.error(msg)

    def warning(self, msg):
        self.pythonLogger.warning(msg)

    def info(self, msg):
        self.pythonLogger.info(msg)

    def debug(self, msg):
        self.pythonLogger.debug(msg)

    def shutdown(self):
        logging.shutdown()

    def __get_log_level(self, verbosity):
        if verbosity == 0:
            return 60
        elif verbosity == 1:
            return logging.ERROR
        elif verbosity == 2:
            return logging.WARNING
        elif verbosity == 3:
            return logging.INFO
        elif verbosity == 4:
            return logging.DEBUG
        return logging.INFO

    def __get_file_handler(self, logfile):
        handler = logging.FileHandler(logfile, mode="w")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.__get_file_formatter())
        return handler

    def __get_console_handler(self, level):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.__get_console_formatter())
        return handler

    def __get_file_formatter(self):
        return logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

    def __get_console_formatter(self):
        return logging.Formatter("%(levelname)s: %(message)s")
