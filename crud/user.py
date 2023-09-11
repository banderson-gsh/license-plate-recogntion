from sqlalchemy.orm.session import Session
from passlib.context import CryptContext
from schemas.models import UserCreate, UserUpdate
from db.models import Users


class UserManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, db: Session, username: str) -> Users:
        return db.query(Users).filter(Users.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Users:
        return db.query(Users).filter(Users.email == email).first()

    def create_user(self, db: Session, user: UserCreate) -> Users:
        hashed_password = self.pwd_context.hash(user.password)
        db_user = Users(username=user.username, email=user.email, hashed_password=hashed_password, full_name=user.full_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        return self.pwd_context.verify(provided_password, stored_password)

    def update_user_profile(self, db: Session, username: str, updated_profile: dict) -> Users:
        user = self.get_user(db, username)

        if user:
            user_update = UserUpdate(**updated_profile)
            user_update_data = user_update.dict(exclude_unset=True)
            for key, value in user_update_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user

        else:
            return None

user_manager = UserManager()
