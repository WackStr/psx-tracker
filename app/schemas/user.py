from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    
class UserCreateRequest(UserBase):
    password: str
    
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str    

class UserCreateResponse(UserBase):
    id: int
    created_on: datetime # The timestamp when the user was created
    
    class Config:
        orm_mode = True # helps pydantic read data from SQLAlchemy models