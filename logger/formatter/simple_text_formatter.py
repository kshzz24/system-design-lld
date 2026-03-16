from formatter.log_formatter import LogFormatter
from log_message import LogMessage

class SimpleTextFormatter(LogFormatter):
     

     def __init__(self):
          super().__init__()

     def format(self, message:LogMessage)->str:
          return f"[{message.timestamp}] [{message.level}] [{message.thread_name}] [{message.logger_name}] -- {message.message}"
