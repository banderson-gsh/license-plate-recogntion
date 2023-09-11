from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.user import user_manager as crud_user
from core.dependencies import get_db
from schemas.models import UserCreate, UserInDB


router = APIRouter()

@router.post("/create-user/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/users/{username}/", response_model=UserInDB)
def get_user_details(username: str, db: Session = Depends(get_db)):
    try:
        db_user = crud_user.get_user(db, username=username)

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

