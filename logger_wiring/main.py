from fastapi import FastAPI
from contextlib import asynccontextmanager
from uvicorn import run

from di import DIContainer
from routes.test_log import router as test_log_router

container = DIContainer()
container.logger.info("💡 Starting setup...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.container = container
    container.redirect_uvicorn_logs()
    container.logger.info("✅ Uvicorn logs are now redirected")

    yield  # App runs while paused here

    # Soft shutdown block runs here
    container.logger.info("🛑 Graceful shutdown initiated...")

app = FastAPI(lifespan=lifespan)
app.include_router(test_log_router)

if __name__ == "__main__":
    container.logger.info("🚀 Launching server...")
    run(app, host="127.0.0.1", port=8000, reload=False)
