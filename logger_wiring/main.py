import logging

# Ensure logging configuration is set at the very start
logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG globally

from logger_wiring.infrastructure.logging.logging_service import LoggingService
from logger_wiring.interface_adapters.logging.logger_adapter import LoggerAdapter
from fastapi import FastAPI
from contextlib import asynccontextmanager
from uvicorn import run
from logger_wiring.routes.test_log import router as test_log_router

# Initialize the framework service (LoggingService)
logging_service = LoggingService(log_to_file=False)  # Set to True for file logging

# Initialize the adapter and pass the logging service to it
logger = LoggerAdapter(logging_service)

# Ensure logging is working right from the start
logger.info("💡 Starting setup...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = logger  # Attach logger to FastAPI state
    logger.redirect_uvicorn_logs()  # Redirect Uvicorn logs to our custom logger
    logger.info("✅ Uvicorn and FastAPI logs are now redirected")
    yield
    logger.info("🛑 Graceful shutdown initiated...")

app = FastAPI(lifespan=lifespan)
app.include_router(test_log_router)

def start():
    logger.info("🚀 Launching server...")
    run(app, host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    start()
