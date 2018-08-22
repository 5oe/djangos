import logging
import os
from conf import setting


class Log(object):
    __instance = None

    def __init__(self):
        self.error_log_path = setting.ERROR_LOG_PATH
        self.run_log_path = setting.RUN_LOG_PATH
        self.error_log = None
        self.run_log = None
        self.__init_error_log()
        self.__init_error_log()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __check_path_exists(self, file_path):
        if not os.path.exists(file_path):
            raise Exception('%s not exists' % file_path)

    def __init_error_log(self):
        self.__check_path_exists(self.error_log_path)
        logger = logging.Logger('error_log', logging.ERROR)
        h = logging.FileHandler(self.error_log_path, 'a', encoding='utf8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
        self.error_log = logger

    def __init_run_log(self):
        self.__check_path_exists(self.run_log_path)
        logger = logging.Logger('run_log', logging.INFO)
        h = logging.FileHandler(self.run_log_path, 'a', encoding='utf8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
        self.run_log = logger

    def log(self, msg, status=True):
        if status:
            self.run_log.info(msg)
        else:
            self.error_log.error(msg)


logger = Log()
