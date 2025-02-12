from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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

class DifficultyEnum(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

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

class GenreSubjectResponse(BaseModel):
    genre: str
    subjects: List[str]

class QuestionBase(BaseModel):
    question_text: str
    image_url: Optional[str] = None

class QuestionCreate(QuestionBase):
    choices: List[ChoiceCreate]

class Question(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    image_url: Optional[str] = None
    choices: List[Choice]
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    subject: str
    genre: str
    difficulty: DifficultyEnum
    duration: Optional[int] = None

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class Quiz(QuizBase):
    id: int
    questions: List[Question]
    class Config:
        from_attributes = True

class ChoiceUpdate(BaseModel):
    id: int
    choice_text: str
    is_correct: bool

class QuestionUpdate(BaseModel):
    question_text: str
    image_url: Optional[str] = None
    choices: List[ChoiceUpdate]

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    score: int
    role: str
    class Config:
        from_attributes = True

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    score: int
    timestamp: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    score: int
    attempts: List[QuizAttemptResponse]

class LeaderboardEntry(BaseModel):
    username: str
    score: int

class LeaderboardResponse(BaseModel):
    top_scorers: List[LeaderboardEntry]
