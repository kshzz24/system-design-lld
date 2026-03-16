
from log_appender import LogAppender
from formatter.log_formatter import LogFormatter
from log_message import LogMessage

class ConsoleAppender(LogAppender):

    _formatter:LogFormatter= None

    def __init__(self):
        super().__init__()

    @property
    def formatter(self)->LogFormatter:
        return self._formatter
       

    @formatter.setter
    def formatter(self, formatter) -> None:
        self._formatter = formatter
    
    def append(self, message:LogMessage):
        print(self._formatter.format(message))
    
    def close(self):
        pass
