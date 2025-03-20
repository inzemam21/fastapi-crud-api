from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()  # Roll back the transaction to avoid partial commits
        raise HTTPException(status_code=400, detail="Email already exists")

@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user: User = Depends(get_user_by_id)):
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db), user: User = Depends(get_user_by_id)):
    try:
        for key, value in user_data.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

@router.delete("/{user_id}", response_model=dict)
def delete_user(user: User = Depends(get_user_by_id), db: Session = Depends(get_db)):
    db.delete(user)
    db.commit()
    return {"message": f"User {user.id} deleted"}