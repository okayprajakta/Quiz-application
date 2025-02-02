#src/routers/leaderboard_router.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from .. import database, models
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/leaderboard", response_class=HTMLResponse)
def get_leaderboard(request: Request, db: Session = Depends(database.get_db)):
    leaderboard = db.query(models.User).order_by(models.User.score.desc()).limit(10).all()
    return get_leaderboard