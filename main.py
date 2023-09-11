from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uvicorn
from core.config import settings
from core.security import verify_token
from core.dependencies import get_db
from db.session import SessionLocal
from schemas import models
from routers import authentication, vehicles, users


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Vehicle License Plate Recognition API",
    openapi_prefix=settings.API_PREFIX,
)

# Include routers
app.include_router(authentication.router)
app.include_router(vehicles.router)
app.include_router(users.router)

# Database
models.Base.metadata.create_all(bind=SessionLocal().bind)

# OAuth2 Security dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception, db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
