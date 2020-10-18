import logging
from params import FileParams
import datetime
import time


class Logger(object):

    def __init__(self, name):
        self.name = name.upper()
        self.datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - [%(name)s] >> %(message)s', "%Y-%m-%d %H:%M:%S")

        self.file_handler = logging.FileHandler(f'{FileParams.logs_dir}/log_{self.datetime}.log')
        self.file_handler.setFormatter(formatter)

    def logger(self):
        logger = logging.getLogger(self.name)
        logger.addHandler(self.file_handler)
        logger.setLevel(logging.INFO)
        logger.isEnabledFor(logging.WARNING)
        logger.isEnabledFor(logging.ERROR)
        return logger


class Timer(object):

    def __init__(self, original_function):
        self.original_function = original_function
        self.time_log = Logger("time").logger()

    def __call__(self, *args, **kwargs):
        t1 = time.time()
        result = self.original_function(*args, **kwargs)
        t2 = time.time() - t1
        self.time_log.info(f'{self.original_function.__name__} ran in: {t2} sec')
        return result
