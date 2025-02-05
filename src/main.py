from fastapi import FastAPI
from .routers import user_router, quiz_router
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(quiz_router.router, prefix="/quizzes", tags=["quizzes"])

