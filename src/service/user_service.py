from sqlalchemy.orm import Session
from .. import models, schemas
from ..repository.user_repository import UserRepository
from ..utils.unit_of_work import UnitOfWork
from typing import List

class UserService:
    def __init__(self, db: Session):
        self.uow = UnitOfWork(db)

    def create_user(self, user: schemas.UserCreate):
        with self.uow:
            new_user = self.uow.user_repository.create_user(user)
            self.uow.commit()
            return new_user

    def get_user_by_email(self, email: str):
        with self.uow:
            return self.uow.user_repository.get_user_by_email(email)
    
    def get_user_by_username(self, username: str):
        with self.uow:
            return self.uow.user_repository.get_user_by_username(username)
    
    def get_top_scorers(self, limit: int = 10) -> List[schemas.User]:
        with self.uow:
            return self.uow.user_repository.get_top_scorers(limit)