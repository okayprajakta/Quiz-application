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
        self.db.flush()  

        for question in quiz.questions:
            db_question = models.Question(
                quiz_id=db_quiz.id,
                question_text=question.question_text,
                image_url=question.image_url
            )
            self.db.add(db_question)
            self.db.flush()  
            for choice in question.choices:
                db_choice = models.Choice(
                    question_id=db_question.id,
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct
                )
                self.db.add(db_choice)
        return db_quiz

    def get_quiz(self, quiz_id: int):
        return self.db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

    def get_all_quizzes(self):
        return self.db.query(models.Quiz).all()

    def get_random_questions_by_genre_subject_title(self, genre: str, subject: str, title: str, num_questions: int):
        questions = self.db.query(models.Question).join(models.Quiz).filter(
            models.Quiz.genre == genre,
            models.Quiz.subject == subject,
            models.Quiz.title == title
        ).all()
        return random.sample(questions, min(len(questions), num_questions))

    def submit_quiz(self, submission: schemas.QuizSubmission):
        score = 0
        feedback = []
        total_questions = len(submission.answers)

        for answer in submission.answers:
            choice = self.db.query(models.Choice).filter(
                models.Choice.id == answer.choice_id,
                models.Choice.question_id == answer.question_id
            ).first()
            correct_choice = self.db.query(models.Choice).filter(
                models.Choice.question_id == answer.question_id,
                models.Choice.is_correct == True
            ).first()

            if choice and choice.is_correct:
                score += 1
            else:
                feedback.append(schemas.Feedback(
                    question_id=answer.question_id,
                    correct_choice_id=correct_choice.id if correct_choice else None,
                    selected_choice_id=answer.choice_id
                ))

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Update user's score (assuming you have a User model with a score field)
        user = self.db.query(models.User).filter(models.User.id == submission.user_id).first()
        if user:
            user.score += score
            self.db.add(user)

        return schemas.SubmissionResponse(
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            feedback=feedback
        )

    def update_quiz(self, quiz_id: int, quiz: schemas.QuizUpdate):
        db_quiz = self.get_quiz(quiz_id)
        if db_quiz:
            for key, value in quiz.dict(exclude_unset=True).items():
                if key == "questions" and value is not None:
                    db_quiz.questions = []
                    for question in value:
                        db_question = models.Question(
                            quiz_id=db_quiz.id,
                            question_text=question["question_text"],
                            image_url=question.get("image_url")
                        )
                        self.db.add(db_question)
                        self.db.flush()  
                        for choice in question["choices"]:
                            db_choice = models.Choice(
                                question_id=db_question.id,
                                choice_text=choice["choice_text"],
                                is_correct=choice["is_correct"]
                            )
                            self.db.add(db_choice)
                        db_quiz.questions.append(db_question)
                else:
                    setattr(db_quiz, key, value)
        return db_quiz

    def delete_quiz(self, quiz_id: int):
        db_quiz = self.get_quiz(quiz_id)
        if db_quiz:
            self.db.delete(db_quiz)