from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import bcrypt

from app.database import get_db
from app.auth import create_access_token, create_refresh_token, verify_token
from app.schemas.user import UserLoginRequest
from app.models.user import User as DBUser


router = APIRouter()

@router.post("/login")
def log(user: UserLoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if payload:
        username: str = payload.get("sub")
        
        new_access_token = create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    
@router.post("/verify")
def validate_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    payload = verify_token(token)
    if payload:
        return {"valid": True}
    raise HTTPException(status_code=401, detail="Invalid token")
