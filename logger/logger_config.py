from loglevel import LogLevel
from appender.log_appender import LogAppender
from typing import List

class LoggerConfig:
     _level:LogLevel
     _appenders:list[LogAppender]

     def __init__(self, level):
          self._level = level
          self._appenders = []

     @property
     def level(self)->LogLevel:
          return self._level
     
     @level.setter
     def level(self, level:LogLevel)->None:
          self._level = level
     
     
     def get_appender(self) -> List[LogAppender]:
           return list(self._appenders)      

     def add_appender(self, appender: LogAppender)->None:
          self._appenders.append(appender)
     
 
