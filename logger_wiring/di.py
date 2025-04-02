import logging
import os
from logger import UvicornRedirectLogger
from pathlib import Path

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

class ColorFormatter(logging.Formatter):
    def format(self, record):
        full_path = Path(record.pathname).resolve()

        if "site-packages" in str(full_path) or "venv" in str(full_path):
            scope = "📦 EXTERNAL"
            color = COLOR_MAP["EXTERNAL"]

            # Trim to just the last 2 components: package/file.py:line
            parts = full_path.parts
            try:
                idx = parts.index("site-packages")
                shortened = "/".join(parts[idx+1:])
            except ValueError:
                # fallback if not in site-packages
                shortened = full_path.name
            location = f"{shortened}:{record.lineno}"
        else:
            scope = "🧠 INTERNAL"
            color = COLOR_MAP.get(record.levelname, "")
            location = str(full_path.relative_to(PROJECT_ROOT)) + f":{record.lineno}"

        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        message = record.getMessage()

        return f"{color}[🔥 CUSTOM] {timestamp} | {record.levelname} | {record.name} | {scope} | 📍 {location} | {message}{RESET}"

    def formatTime(self, record, datefmt=None):
        return super().formatTime(record, "%Y-%m-%d %H:%M:%S")

    
class DIContainer:
    def __init__(self):
        self.logger = self._configure_logger()

    def _configure_logger(self):
        logger = logging.getLogger(f"app.{__name__}")


        logger.setLevel(logging.DEBUG)

        formatter = ColorFormatter()
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.handlers = [stream_handler]
        return logger

    def redirect_uvicorn_logs(self):
        for name in ["uvicorn.error", "uvicorn.access"]:
            logger = logging.getLogger(name)
            logger.handlers = []
            logger.addHandler(UvicornRedirectLogger("myapp.uvicorn_sink"))
            logger.propagate = False
