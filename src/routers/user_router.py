from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from .. import schemas, database
from ..utils.auth import authenticate_user, get_current_user, create_access_token
from datetime import timedelta
from ..service.user_service import UserService
from ..models import Role
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

def admin_required(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user

@router.get("/register", response_class=HTMLResponse, name="register_form")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse, name="create_user")
async def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = user_service.get_user_by_username(username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = schemas.UserCreate(username=username, email=email, password=password)
    new_user = user_service.create_user(user)
    return templates.TemplateResponse("register_success.html", {"request": request, "user": new_user})

@router.get("/login", response_class=HTMLResponse, name="login_form")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse, name="login_for_access_token")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    user_service = UserService(db)
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return templates.TemplateResponse("login_success.html", {"request": request, "access_token": access_token})

@router.get("/leaderboard", response_class=HTMLResponse, name="leaderboard")
async def get_leaderboard(request: Request, limit: int = 10, db: Session = Depends(database.get_db)):
    user_service = UserService(db)
    top_scorers = user_service.get_top_scorers(limit)
    leaderboard_entries = [schemas.LeaderboardEntry(username=user.username, score=user.score) for user in top_scorers]
    return templates.TemplateResponse("leaderboard.html", {"request": request, "leaderboard": leaderboard_entries})