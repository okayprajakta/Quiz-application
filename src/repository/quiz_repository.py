# src/repository/quiz_repository.py
from sqlalchemy.orm import Session
from .. import models, schemas
import random

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_quiz(self, quiz: schemas.QuizCreate):
        db_quiz = models.Quiz(title=quiz.title, subject=quiz.subject, genre=quiz.genre)
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        for question in quiz.questions:
            db_question = models.Question(
                quiz_id=db_quiz.id,
                question_text=question.question_text,
                image_url=question.image_url
            )
            self.db.add(db_question)
            self.db.commit()
            self.db.refresh(db_question)
            for choice in question.choices:
                db_choice = models.Choice(
                    question_id=db_question.id,
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct
                )
                self.db.add(db_choice)
                self.db.commit()
                self.db.refresh(db_choice)
        return db_quiz

    def get_quiz(self, quiz_id: int):
        return self.db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

    def get_all_quizzes(self):
        return self.db.query(models.Quiz).all()

    def get_random_questions(self, quiz_id: int, num_questions: int):
        questions = self.db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
        return random.sample(questions, min(len(questions), num_questions))

    def update_quiz(self, quiz_id: int, quiz: schemas.QuizCreate):
        db_quiz = self.get_quiz(quiz_id)
        db_quiz.title = quiz.title
        db_quiz.subject = quiz.subject
        db_quiz.genre = quiz.genre
        self.db.commit()
        self.db.refresh(db_quiz)
        # Update questions and choices as needed
        return db_quiz

    def delete_quiz(self, quiz_id: int):
        db_quiz = self.get_quiz(quiz_id)
        self.db.delete(db_quiz)
        self.db.commit()