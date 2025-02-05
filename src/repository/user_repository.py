from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils.auth import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()