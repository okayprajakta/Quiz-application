# src/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class ChoiceCreate(ChoiceBase):
    pass

class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str
    image_url: Optional[str] = None

class QuestionCreate(QuestionBase):
    choices: List[ChoiceCreate]

class Question(QuestionBase):
    id: int
    quiz_id: int
    choices: List[Choice]

    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    subject: str
    genre: str 

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class Quiz(QuizBase):
    id: int
    questions: List[Question]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    score: int
    role: str

    class Config:
        from_attributes = True