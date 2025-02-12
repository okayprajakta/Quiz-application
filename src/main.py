from fastapi import FastAPI

app = FastAPI()

from .routers import user_router, quiz_router
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(quiz_router.router, prefix="/quizzes", tags=["quizzes"])
