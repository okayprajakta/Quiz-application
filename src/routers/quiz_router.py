# src/routers/quiz_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..repository.quiz_repository import QuizRepository
from .user_router import admin_required
from typing import List

router = APIRouter()

@router.get("/genres", response_model=List[str])
def get_genres(db: Session = Depends(database.get_db)):
    try:
        genres = db.query(models.Quiz.genre).distinct().all()
        if not genres:
            return []
        return [genre[0] for genre in genres]
    except Exception as e:
        print(f"Error fetching genres: {e}")  # Debugging line
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/subjects", response_model=List[str])
def get_subjects(genre: str, db: Session = Depends(database.get_db)):
    subjects = db.query(models.Quiz.subject).filter(models.Quiz.genre == genre).distinct().all()
    return [subject[0] for subject in subjects]

@router.post("/quizzes", response_model=schemas.Quiz, dependencies=[Depends(admin_required)])
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(database.get_db)):
    quiz_repo = QuizRepository(db)
    return quiz_repo.create_quiz(quiz)

@router.put("/quizzes/{quiz_id}", response_model=schemas.Quiz, dependencies=[Depends(admin_required)])
def update_quiz(quiz_id: int, quiz: schemas.QuizCreate, db: Session = Depends(database.get_db)):
    quiz_repo = QuizRepository(db)
    db_quiz = quiz_repo.get_quiz(quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_repo.update_quiz(quiz_id, quiz)

@router.delete("/quizzes/{quiz_id}", dependencies=[Depends(admin_required)])
def delete_quiz(quiz_id: int, db: Session = Depends(database.get_db)):
    quiz_repo = QuizRepository(db)
    db_quiz = quiz_repo.get_quiz(quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz_repo.delete_quiz(quiz_id)
    return {"detail": "Quiz deleted successfully"}

@router.get("/quizzes/{quiz_id}/questions", response_model=List[schemas.Question])
def get_quiz_questions(quiz_id: int, db: Session = Depends(database.get_db)):
    quiz_repo = QuizRepository(db)
    db_quiz = quiz_repo.get_quiz(quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz.questions

@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(quiz_id: int, answers: List[int], db: Session = Depends(database.get_db)):
    quiz_repo = QuizRepository(db)
    questions = quiz_repo.get_random_questions(quiz_id, len(answers))
    score = 0
    feedback = []
    for question, answer in zip(questions, answers):
        correct_choice = next((choice for choice in question.choices if choice.is_correct), None)
        user_choice = next((choice for choice in question.choices if choice.id == answer), None)
        if correct_choice and correct_choice.id == answer:
            score += 1
        feedback.append({
            "question": question.question_text,
            "correct_answer": correct_choice.choice_text if correct_choice else None,
            "your_answer": user_choice.choice_text if user_choice else None
        })
    return {"score": score, "feedback": feedback}