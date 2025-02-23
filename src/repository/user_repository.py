from sqlalchemy.orm import Session
from src import models, schemas
from src.utils.auth import get_password_hash
from typing import List

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,  
            score=0,       
            role=models.Role.USER  
        )
        self.db.add(db_user)
        self.db.flush()  
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()
    
    def get_top_scorers(self, limit: int = 10) -> List[schemas.User]:
        return self.db.query(models.User).order_by(models.User.score.desc()).limit(limit).all()