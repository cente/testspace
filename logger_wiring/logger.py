import logging

class UvicornRedirectLogger(logging.Handler):
    def __init__(self, target_name):
        super().__init__()
        self.target_logger = logging.getLogger(target_name)

    def emit(self, record):
        self.target_logger.handle(record)
