from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from crud.user import user_manager as crud_user
from core.security import create_access_token
from core.config import settings
from db.session import SessionLocal
from schemas.models import Token


router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    user = crud_user.get_user(db, username=form_data.username)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not crud_user.verify_password(user.hashed_password, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

