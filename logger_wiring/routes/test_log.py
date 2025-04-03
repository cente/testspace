from fastapi import APIRouter
import logging

# Use the same globally defined logger
logger = logging.getLogger("app.system.logger")
# Diagnostic Print: Check if the logger is properly instantiated
print("Logger instance:", logger)
print("Logger level:", logger.level)  # Should print the numeric value for the level (e.g., 20 for INFO)

# Check the handlers to see if they are properly set
print("Logger handlers:", logger.handlers)


logger.info ('hi')
router = APIRouter()

@router.get("/test-log")
async def test_log():
    logger.info("Test log triggered in /routes/test_log.py")  # This should now log correctly
    return {"message": "Log test triggered"}
