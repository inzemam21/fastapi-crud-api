from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict  # New import

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # Replace Config class