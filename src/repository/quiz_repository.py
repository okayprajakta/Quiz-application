from sqlalchemy.orm import Session
from .. import models, schemas
import random
from typing import List

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_quiz(self, quiz: schemas.QuizCreate): 
        existing_quiz = self.db.query(models.Quiz).filter(
            models.Quiz.genre == quiz.genre,
            models.Quiz.subject == quiz.subject,
            models.Quiz.title == quiz.title
        ).first()

        if existing_quiz:
            existing_question_texts = {q.question_text for q in existing_quiz.questions}
            for question in quiz.questions:
                if question.question_text not in existing_question_texts:
                    db_question = models.Question(
                        quiz_id=existing_quiz.id,
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
            return existing_quiz
        else:
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

    def get_genres_and_subjects(self):
        genres = self.db.query(models.Quiz.genre).distinct().all()
        if not genres:
            return []

        genre_subjects = []
        for genre in genres:
            subjects = self.db.query(models.Quiz.subject).filter(models.Quiz.genre == genre[0]).distinct().all()
            genre_subjects.append(schemas.GenreSubjectResponse(
                genre=genre[0],
                subjects=[subject[0] for subject in subjects]
            ))

        return genre_subjects

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

    def update_question_and_choices(self, question_id: int, question_update: schemas.QuestionUpdate):
        db_question = self.db.query(models.Question).filter(models.Question.id == question_id).first()
        if not db_question:
            return None

        db_question.question_text = question_update.question_text
        db_question.image_url = question_update.image_url

        for choice_update in question_update.choices:
            db_choice = self.db.query(models.Choice).filter(models.Choice.id == choice_update.id).first()
            if db_choice:
                db_choice.choice_text = choice_update.choice_text
                db_choice.is_correct = choice_update.is_correct

        self.db.commit()
        return db_question

    def delete_questions(self, question_ids: List[int]):
        db_questions = self.db.query(models.Question).filter(models.Question.id.in_(question_ids)).all()
        if not db_questions:
            return None
        for question in db_questions:
            self.db.delete(question)
        self.db.commit()
        return db_questions