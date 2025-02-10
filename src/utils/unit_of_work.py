#src/utils/unit_of_work.py
from sqlalchemy.orm import Session
from ..repository.quiz_repository import QuizRepository
from ..repository.user_repository import UserRepository

class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.quiz_repository = QuizRepository(db)
        self.user_repository = UserRepository(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()