import logging

class RedirectToLoggerHandler(logging.Handler):
    def __init__(self, target_name: str):
        super().__init__()
        self.target_logger = logging.getLogger(target_name)

    def emit(self, record: logging.LogRecord):
        self.target_logger.handle(record)
