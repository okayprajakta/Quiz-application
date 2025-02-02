# src/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), default=Role.USER)
    score = Column(Integer, default=0)

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    subject = Column(String, index=True)
    genre = Column(String, index=True)
    questions = relationship("Question", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(String)
    image_url = Column(String, nullable=True)
    choices = relationship("Choice", back_populates="question")
    quiz = relationship("Quiz", back_populates="questions")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    choice_text = Column(String)
    is_correct = Column(Boolean, default=False)
    question = relationship("Question", back_populates="choices")