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

class ChoiceResponse(BaseModel):
    id: int
    question_id: int
    choice_text: str

class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    image_url: Optional[str] = None
    choices: List[ChoiceResponse]

class Answer(BaseModel):
    question_id: int
    choice_id: int

class QuizSubmission(BaseModel):
    quiz_id: int
    user_id: int
    answers: List[Answer]

class Feedback(BaseModel):
    question_id: int
    correct_choice_id: int
    selected_choice_id: int

class SubmissionResponse(BaseModel):
    score: int
    total_questions: int
    percentage: float
    feedback: List[Feedback]
    
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

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    genre: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None

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