from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database 
from ..utils.auth import authenticate_user, get_current_user, create_access_token
from datetime import timedelta
from ..utils.unit_of_work import UnitOfWork
from ..models import Role

router = APIRouter()

def admin_required(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user

@router.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    with UnitOfWork(db) as uow:
        db_user = uow.user_repository.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user = uow.user_repository.get_user_by_username(user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        new_user = uow.user_repository.create_user(user)
        uow.commit()
        return new_user

@router.post("/login")
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    with UnitOfWork(db) as uow:
        user = authenticate_user(db, form_data.username, form_data.password)
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
        return {"access_token": access_token, "token_type": "bearer"}

@router.get("/leaderboard", response_model=schemas.LeaderboardResponse)
def get_leaderboard(limit: int = 10, db: Session = Depends(database.get_db)):
    with UnitOfWork(db) as uow:
        top_scorers = uow.user_repository.get_top_scorers(limit)
        leaderboard_entries = [schemas.LeaderboardEntry(username=user.username, score=user.score) for user in top_scorers]
        return schemas.LeaderboardResponse(top_scorers=leaderboard_entries)