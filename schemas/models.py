from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from passlib.context import CryptContext

from db.session import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Vehicle management
class VehicleCreate(BaseModel):
    plate_number: Optional[str] = None

class VehicleInDB(VehicleCreate):
    id: int


# Vehicle details management
class VehicleDetailsCreate(BaseModel):
    image: str
    gps_details: str
    vehicle_id: int

class VehicleDetailsInDB(VehicleDetailsCreate):
    id: int


# User management
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    @validator("username", pre=True, always=True)
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty!")
        return v
    
    @validator("password", pre=True, always=True)
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long!")
        return pwd_context.hash(v)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str]


# OAuth2 related models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: Optional[List[str]] = []
    expired: Optional[bool] = False
