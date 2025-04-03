from abc import ABC, abstractmethod

# The Port for logging in the application (can be swapped with any other logging system)
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
