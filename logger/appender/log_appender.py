from abc import ABC, abstractmethod
from formatter.log_formatter import LogFormatter
from log_message import LogMessage

class LogAppender(ABC): 
    
    @property
    @abstractmethod
    def formatter(self)->LogFormatter:
        pass

    @formatter.setter
    @abstractmethod
    def formatter(self, formatter:LogFormatter)->None:
        pass

    @abstractmethod
    def append(self, message:LogMessage) ->None:
        pass
    
    @abstractmethod
    def close(self)->None:
        pass




