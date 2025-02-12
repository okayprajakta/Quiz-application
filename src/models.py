from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLAlchemyEnum 
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class DifficultyLevel(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), default=Role.USER)
    score = Column(Integer, default=0)
    attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    subject = Column(String, index=True)
    genre = Column(String, index=True)
    difficulty = Column(SQLAlchemyEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    duration = Column(Integer, nullable=True)  # Duration in minutes
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    question_text = Column(String)
    image_url = Column(String, nullable=True)
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")
    quiz = relationship("Quiz", back_populates="questions")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    choice_text = Column(String)
    is_correct = Column(Boolean, default=False)
    question = relationship("Question", back_populates="choices")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    score = Column(Integer)
    timestamp = Column(String)
    user = relationship("User", back_populates="attempts")
    quiz = relationship("Quiz")
