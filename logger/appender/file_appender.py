
from appender.log_appender import LogAppender
from formatter.log_formatter import LogFormatter
from log_message import LogMessage

class FileAppender(LogAppender):

    _formatter:LogFormatter= None
    writer = None

    def __init__(self,file_path):
        super().__init__()
        self.writer = open(file_path, "a")

    @property
    def formatter(self)->LogFormatter:
        return self._formatter
       

    @formatter.setter
    def formatter(self, formatter) -> None:
        self._formatter = formatter
    
    def append(self, message:LogMessage):
        formatted = self._formatter.format(message)    
        self.writer.write(formatted + "\n")
        self.writer.flush()
    
    def close(self):
         if self.writer:
            self.writer.close()
