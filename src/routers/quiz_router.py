# src/routers/quiz_router.py
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from .. import schemas, database
from ..service.quiz_service import QuizService
from ..utils.auth import get_current_user
from fastapi.templating import Jinja2Templates
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/genres-subjects", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def get_genres_and_subjects(request: Request, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    genres_subjects = quiz_service.get_genres_and_subjects()
    return templates.TemplateResponse("genres_subjects.html", {"request": request, "genres_subjects": genres_subjects})

@router.get("/quiz-list/{genre}/{subject}", response_class=HTMLResponse, name="quiz_list", dependencies=[Depends(get_current_user)])
async def quiz_list(request: Request, genre: str, subject: str, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    quizzes = quiz_service.get_quizzes_by_genre_subject(genre, subject)
    return templates.TemplateResponse("quiz_list.html", {"request": request, "genre": genre, "subject": subject, "quizzes": quizzes})

@router.get("/quiz-detail/{quiz_id}", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def quiz_detail(request: Request, quiz_id: int, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    quiz = quiz_service.get_quiz_by_id(quiz_id)
    return templates.TemplateResponse("quiz_detail.html", {"request": request, "quiz": quiz})

@router.post("/submit-quiz", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def submit_quiz(request: Request, submission: schemas.QuizSubmission = Depends(), db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    result = quiz_service.submit_quiz(submission)
    return templates.TemplateResponse("submission_result.html", {"request": request, "result": result})

@router.get("/update-question/{question_id}", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def update_question(request: Request, question_id: int, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    question = quiz_service.get_question_by_id(question_id)
    return templates.TemplateResponse("update_question.html", {"request": request, "question": question})

@router.post("/update-question/{question_id}", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def update_question_and_choices(request: Request, question_id: int, db: Session = Depends(database.get_db),
                                      question_text: str = Form(...), image_url: str = Form(...), choices: List[schemas.ChoiceUpdate] = Depends()):
    question_update = schemas.QuestionUpdate(question_text=question_text, image_url=image_url, choices=choices)
    quiz_service = QuizService(db)
    db_question = quiz_service.update_question_and_choices(question_id, question_update)
    return templates.TemplateResponse("update_question.html", {"request": request, "question": db_question})

@router.get("/delete-questions", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def delete_questions_form(request: Request, db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    questions = quiz_service.get_all_questions()
    return templates.TemplateResponse("delete_questions.html", {"request": request, "questions": questions})

@router.post("/delete-questions", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def delete_questions(request: Request, question_ids: List[int] = Form(...), db: Session = Depends(database.get_db)):
    quiz_service = QuizService(db)
    db_questions = quiz_service.delete_questions(question_ids)
    return templates.TemplateResponse("delete_questions.html", {"request": request, "questions": db_questions})