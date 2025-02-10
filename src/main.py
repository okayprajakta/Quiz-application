# src/main.py
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from jose import jwt
from config import SECRET_KEY, ALGORITHM
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .database import get_db
from .service.quiz_service import QuizService

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'bearer':
                return
            token = credentials
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        except Exception as e:
            return

app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

# Set up templates directory
templates = Jinja2Templates(directory="src/templates")

# Set up static files directory for CSS, JS, etc.
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Include your routers
from .routers import user_router, quiz_router
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(quiz_router.router, prefix="/quizzes", tags=["quizzes"])

# Example route to render a template
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    genres_subjects = quiz_service.get_genres_and_subjects()
    return templates.TemplateResponse("home.html", {"request": request, "genres_subjects": genres_subjects})