from fastapi import Request, Response
import logging
import time
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler with rotation (max 5MB, keep 3 backups)
file_handler = RotatingFileHandler(
    filename=os.path.join(log_dir, "app.log"),
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=3
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration_ms:.1f}ms")
    return response