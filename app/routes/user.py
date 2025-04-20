from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import get_db
from app.models.user import User as DBUser
from app.schemas.user import UserCreateRequest, UserCreateResponse


router = APIRouter()



@router.post("/create", response_model=UserCreateResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)) -> DBUser:
    
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    
    new_user = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

