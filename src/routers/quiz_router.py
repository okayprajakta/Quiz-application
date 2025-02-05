from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..utils.unit_of_work import UnitOfWork
from .user_router import admin_required
from typing import List
import random

router = APIRouter()

@router.get("/genres-subjects", response_model=List[schemas.GenreSubjectResponse])
def get_genres_and_subjects(db: Session = Depends(database.get_db)):
    genres = db.query(models.Quiz.genre).distinct().all()
    if not genres:
        return []

    genre_subjects = []
    for genre in genres:
        subjects = db.query(models.Quiz.subject).filter(models.Quiz.genre == genre[0]).distinct().all()
        genre_subjects.append(schemas.GenreSubjectResponse(
            genre=genre[0],
            subjects=[subject[0] for subject in subjects]
        ))

    return genre_subjects

@router.get("/random-questions", response_model=List[schemas.QuestionResponse])
def get_random_questions(
    genre: schemas.GenreEnum,
    subject: schemas.SubjectEnum,
    title: schemas.TitleEnum,
    num_questions: int,
    db: Session = Depends(database.get_db)
):
    questions = db.query(models.Question).join(models.Quiz).filter(
        models.Quiz.genre == genre,
        models.Quiz.subject == subject,
        models.Quiz.title == title
    ).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for the specified genre, subject, and title")
    
    random_questions = random.sample(questions, min(len(questions), num_questions))

    question_responses = []
    for question in random_questions:
        choices = [schemas.ChoiceResponse(id=choice.id, question_id=choice.question_id, choice_text=choice.choice_text) for choice in question.choices]
        question_responses.append(schemas.QuestionResponse(id=question.id, quiz_id=question.quiz_id, question_text=question.question_text, image_url=question.image_url, choices=choices))
    
    return question_responses

@router.post("/submit-quiz", response_model=schemas.SubmissionResponse)
def submit_quiz(submission: schemas.QuizSubmission, db: Session = Depends(database.get_db)):
    with UnitOfWork(db) as uow:
        response = uow.quiz_repository.submit_quiz(submission)
        uow.commit()
        return response

@router.post("/quizzes", response_model=schemas.Quiz, dependencies=[Depends(admin_required)])
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(database.get_db)):
    with UnitOfWork(db) as uow:
        db_quiz = uow.quiz_repository.create_quiz(quiz)
        uow.commit()
        return db_quiz

