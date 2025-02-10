#src\service\quiz_service.py
from sqlalchemy.orm import Session
from .. import models, schemas
from ..repository.quiz_repository import QuizRepository
from ..utils.unit_of_work import UnitOfWork
from typing import List

class QuizService:
    def __init__(self, db: Session):
        self.uow = UnitOfWork(db)

    def create_quiz(self, quiz: schemas.QuizCreate):
        with self.uow:
            db_quiz = self.uow.quiz_repository.create_quiz(quiz)
            self.uow.commit()
            return db_quiz

    def get_genres_and_subjects(self):
        with self.uow:
            return self.uow.quiz_repository.get_genres_and_subjects()

    def get_random_questions_by_genre_subject_title(self, genre: str, subject: str, title: str, num_questions: int):
        with self.uow:
            return self.uow.quiz_repository.get_random_questions_by_genre_subject_title(genre, subject, title, num_questions)

    def submit_quiz(self, submission: schemas.QuizSubmission):
        with self.uow:
            response = self.uow.quiz_repository.submit_quiz(submission)
            self.uow.commit()
            return response

    def update_question_and_choices(self, question_id: int, question_update: schemas.QuestionUpdate):
        with self.uow:
            db_question = self.uow.quiz_repository.update_question_and_choices(question_id, question_update)
            self.uow.commit()
            return db_question

    def delete_questions(self, question_ids: List[int]):
        with self.uow:
            db_questions = self.uow.quiz_repository.delete_questions(question_ids)
            self.uow.commit()
            return db_questions