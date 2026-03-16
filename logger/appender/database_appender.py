
from log_appender import LogAppender
from formatter.log_formatter import LogFormatter
from log_message import LogMessage

class DatabaseAppender(LogAppender):

    _formatter:LogFormatter= None
    connection= None

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    @property
    def formatter(self)->LogFormatter:
        return self._formatter
       

    @formatter.setter
    def formatter(self, formatter) -> None:
        self._formatter = formatter
    
    def append(self, message:LogMessage):
        self._formatter.format(message)
    
    def close(self):
       if self.connection:
            self.connection.close()
