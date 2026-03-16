from logger import Logger
from loglevel import LogLevel
from async_log_processor import AsyncLogProcessor


class LogManager:
    _instance = None

    def __init__(self):
        self._processor = AsyncLogProcessor()

        self._root_logger = Logger("root", self._processor, level=LogLevel.DEBUG)

        self._loggers: dict[str, Logger] = {}
        self._loggers["root"] = self._root_logger

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LogManager()

        return cls._instance

    def get_logger(self, name: str) -> Logger:
        if name in self._loggers:
            return self._loggers[name]

        logger = self._create_logger(name)
        self._loggers[name] = logger
        return logger

    def _create_logger(self, name: str) -> Logger:
        logger = Logger(name, self._processor)

        # determine parent logger
        parent_name = name.rpartition('.')[0]

        if parent_name == "":
            logger.parent = self._root_logger
        else:
            logger.parent = self.get_logger(parent_name)

        return logger

    def shutdown(self):
        self._processor.stop()

        for logger in self._loggers.values():
            for appender in logger.appenders:
                appender.close()