from datetime import datetime
from loglevel import LogLevel


class LogMessage:
    """Bundles all log metadata into a single object.
    Created by Logger, passed through AsyncLogProcessor -> LogAppender -> LogFormatter.
    """

    def __init__(self, level: LogLevel, message: str, logger_name: str):
        self._level = level
        self._message = message
        self._logger_name = logger_name
        self._thread_name = ""  # will be set by Logger using threading.current_thread().name
        self._timestamp = datetime.now()

    # --- read-only properties (log messages are immutable once created) ---

    @property
    def level(self) -> LogLevel:
        return self._level

    @property
    def message(self) -> str:
        return self._message

    @property
    def logger_name(self) -> str:
        return self._logger_name

    @property
    def thread_name(self) -> str:
        return self._thread_name

    @thread_name.setter
    def thread_name(self, name: str):
        self._thread_name = name

    @property
    def timestamp(self) -> datetime:
        return self._timestamp
