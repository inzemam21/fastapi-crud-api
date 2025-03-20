from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import Base, engine
from app.api.endpoints import user
from app.core.middleware import log_requests
import logging

app = FastAPI()

# Logger from middleware
logger = logging.getLogger("fastapi_app")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for SQLAlchemy errors (not caught in endpoints)
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Please try again later."}
    )

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. We're working on it!"}
    )

# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(user.router)

@app.middleware("http")
async def custom_middleware(request, call_next):
    return await log_requests(request, call_next)