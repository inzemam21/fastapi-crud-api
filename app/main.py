from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.endpoints import user

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the user router
app.include_router(user.router)