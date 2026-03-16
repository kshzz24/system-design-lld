from loglevel import LogLevel
from typing import List
from log_message import LogMessage
from appender.log_appender import LogAppender
from async_log_processor import AsyncLogProcessor


class Logger:

    def __init__(self, name, processor: AsyncLogProcessor, level: LogLevel = None, additivity: bool = True):
        self.name = name
        self.level = level
        self.parent = None
        self.appenders: List[LogAppender] = []
        self.additivity = additivity
        self.processor = processor

    def get_effective_level(self) -> LogLevel:
        """
        Walks up parent chain to find first logger with level set
        """
        logger = self

        while logger is not None:
            if logger.level is not None:
                return logger.level
            logger = logger.parent

        return LogLevel.INFO  # default fallback

    def log(self, level: LogLevel, message: str) -> None:
        """
        Core logging function
        """

        effective_level = self.get_effective_level()

        if level.value >= effective_level.value:
            log_message = LogMessage(level, message, self.name)
            self.call_appenders(log_message)

    def call_appenders(self, msg: LogMessage):
        """
        Sends log message to appenders
        """

        if self.appenders:
            self.processor.process(msg, self.appenders)

        if self.additivity and self.parent:
            self.parent.call_appenders(msg)

    def add_appender(self, appender: LogAppender):
        self.appenders.append(appender)

    # Convenience methods

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def warn(self, message: str):
        self.log(LogLevel.WARN, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)

    def fatal(self, message: str):
        self.log(LogLevel.FATAL, message)