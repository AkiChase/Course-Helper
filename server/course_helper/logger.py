from loguru import logger
from enum import Enum, unique


class Logger:
    """
    loguru二次封装，实现不同名称的logger对应不同的消息前缀
    """
    logger_dict: dict = {}

    @unique
    class Level(Enum):
        DEBUG = 1
        INFO = 2
        SUCCESS = 3
        WARNING = 4
        ERROR = 5

    @classmethod
    def __add(cls, _logger):
        cls.logger_dict[_logger.log_name] = _logger

    @classmethod
    def get_logger(cls, name: str):
        if name not in cls.logger_dict:
            raise Exception(f"the logger with name '{name}' doesn't exists")
        return cls.logger_dict[name]

    def __init__(self, log_name: str):
        if log_name in Logger.logger_dict:
            raise Exception(f"the logger with name '{log_name}' already exists")

        self.log_name = log_name
        #   添加到Logger字典中
        Logger.__add(self)

    def debug(self, msg, *args, **kwargs):
        return logger.debug(f'[{self.log_name}]\t{msg}', __log_name=self.log_name, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return logger.info(f'[{self.log_name}]\t{msg}', __log_name=self.log_name, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        return logger.success(f'[{self.log_name}]\t{msg}', __log_name=self.log_name, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return logger.warning(f'[{self.log_name}]\t{msg}', __log_name=self.log_name, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return logger.error(f'[{self.log_name}]\t{msg}', __log_name=self.log_name, *args, **kwargs)
