import logging
from abc import ABC, abstractmethod
from logger_wiring.infrastructure.logging.redirect_handler import RedirectToLoggerHandler

# === Logger Port (for domain/application use) ===
class LoggerPort(ABC):
    @abstractmethod
    def info(self, message: str): ...
    
    @abstractmethod
    def warning(self, message: str): ...
    
    @abstractmethod
    def error(self, message: str): ...
    
    @abstractmethod
    def debug(self, message: str): ...
    
    @abstractmethod
    def critical(self, message: str): ...

# === Logger Adapter ===
class LoggerAdapter(LoggerPort):
    def __init__(self, logging_service):
        # Initialize with the logging service provided (either file or console logging)
        self._logging_service = logging_service
        self._logger = self._logging_service.logger

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def critical(self, message: str):
        self._logger.critical(message)

    @property
    def logger(self):
        # Expose the logger for direct access if needed
        return self._logger

    def redirect_uvicorn_logs(self):
        """
        Redirect Uvicorn logs to the custom logger.
        """
        for name in ["uvicorn.error", "uvicorn.access"]:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)  # Ensuring INFO level is captured for Uvicorn logs
            logger.handlers = []  # Remove existing handlers to avoid duplicates
            logger.addHandler(RedirectToLoggerHandler("app.system.logger"))
            logger.propagate = False
