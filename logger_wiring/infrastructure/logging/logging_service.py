import logging
from pathlib import Path

# Colors for logging output
COLOR_MAP = {
    "DEBUG": "\033[94m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[95m",
    "EXTERNAL": "\033[90m"
}
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[0]

class LoggingService:
    def __init__(self, log_to_file=False):
        # Set the base logging level to DEBUG before configuring the logger
        self.logger = self._configure_logger(log_to_file)

    def _configure_logger(self, log_to_file):
        # Create a logger instance
        logger = logging.getLogger("app.system.logger")
        logger.setLevel(logging.DEBUG)  # Setting the logging level to DEBUG globally

        # Format the log with colors based on level
        formatter = logging.Formatter(self._get_log_format())

        # Set up stream handler for terminal output
        stream_handler = logging.StreamHandler()

        if log_to_file:
            # If we want to log to a file, also create a file handler
            file_handler = logging.FileHandler("app.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def _get_log_format(self):
        return (
            f"{COLOR_MAP.get('%(levelname)s', '')}[🔥 CUSTOM] %(asctime)s | %(levelname)s | %(name)s "
            f"| %(message)s{RESET}"
        )

    def redirect_uvicorn_logs(self):
        # Redirect Uvicorn logs to the custom logger
        for name in ["uvicorn.error", "uvicorn.access"]:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)  # Ensuring that the Uvicorn logs are also set to DEBUG
            logger.handlers = []  # Clear existing handlers
            logger.addHandler(self._create_redirect_handler("app.system.logger"))
            logger.propagate = False

    def _create_redirect_handler(self, target_name):
        return RedirectToLoggerHandler(target_name)

class RedirectToLoggerHandler(logging.Handler):
    def __init__(self, target_name: str):
        super().__init__()
        self.target_logger = logging.getLogger(target_name)

    def emit(self, record: logging.LogRecord):
        self.target_logger.handle(record)
