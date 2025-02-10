#src\routers\quiz_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..service.quiz_service import QuizService
from ..utils.auth import get_current_user
from .user_router import admin_required
from typing import List

router = APIRouter()

@router.get("/genres-subjects", response_model=List[schemas.GenreSubjectResponse], dependencies=[Depends(get_current_user)])
def get_genres_and_subjects(db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    return quiz_service.get_genres_and_subjects()

@router.get("/random-questions", response_model=List[schemas.QuestionResponse], dependencies=[Depends(get_current_user)])
def get_random_questions(
    genre: schemas.GenreEnum,
    subject: schemas.SubjectEnum,
    title: schemas.TitleEnum,
    num_questions: int,
    db: Session = Depends(database.get_db)
):
    quiz_service = QuizService(db)
    questions = quiz_service.get_random_questions_by_genre_subject_title(genre, subject, title, num_questions)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for the specified genre, subject, and title")
    return questions

@router.post("/submit-quiz", response_model=schemas.SubmissionResponse, dependencies=[Depends(get_current_user)])
def submit_quiz(submission: schemas.QuizSubmission, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    return quiz_service.submit_quiz(submission)

@router.post("/quizzes", response_model=schemas.Quiz, dependencies=[Depends(admin_required)])
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    return quiz_service.create_quiz(quiz)
    
@router.patch("/questions/{question_id}", response_model=schemas.Question, dependencies=[Depends(admin_required)])
def update_question_and_choices(question_id: int, question_update: schemas.QuestionUpdate, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    db_question = quiz_service.update_question_and_choices(question_id, question_update)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.delete("/questions/bulk-delete", status_code=status.HTTP_200_OK, dependencies=[Depends(admin_required)])
def delete_questions(question_ids: List[int], db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    db_questions = quiz_service.delete_questions(question_ids)
    if not db_questions:
        raise HTTPException(status_code=404, detail="Questions not found")
    return {"detail": "Questions successfully deleted"}