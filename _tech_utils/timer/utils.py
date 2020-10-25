import time
from _tech_utils.logger.utils import Logger


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
