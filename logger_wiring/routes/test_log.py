import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("app.routes.test_log")  # consistent naming

@router.get("/test-log")
async def test_log():
    logger.info("Test log triggered in /routes/test_log.py")
    return {"message": "Log test triggered"}
