from log_manager import LogManager
from loglevel import LogLevel
from formatter.simple_text_formatter import SimpleTextFormatter
from appender.console_appender import ConsoleAppender

# 1. Get the singleton LogManager instance
manager = LogManager.get_instance()

# 2. Create a formatter and console appender
formatter = SimpleTextFormatter()
console = ConsoleAppender()
console.formatter = formatter

# 3. Add appender to root logger (all child loggers inherit via additivity)
root = manager.get_logger("root")
root.add_appender(console)

# 4. Get a child logger and log messages at different levels
logger = manager.get_logger("com.app.service")
logger.debug("Starting service...")
logger.info("Service is running")
logger.warn("Memory usage high")
logger.error("Connection failed")
logger.fatal("System crash")

# 5. Test level filtering — set child logger to ERROR level
logger.level = LogLevel.ERROR
logger.info("This should NOT appear")
logger.error("This SHOULD appear")

# 6. Shutdown
manager.shutdown()
