from sqlalchemy import create_engine, String, Column, Integer, ForeignKey,DateTime
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Create the database URL
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create the database engine
engine = create_engine(DB_URL)

# Create a base class for declarative class definitions
Base = declarative_base()

# Create a sessionmaker that will be used to create sessions
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Define the Book class
class Book(Base):

    __tablename__ = "books"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String(90), unique=True)
    author = Column(String(90))
    ISBN = Column(String(13), unique=True)
    quantity_available = Column(Integer)
    borrower_id = Column(Integer, ForeignKey('borrower.id'))
    borrower = relationship('Borrower', back_populates='books')

# Define the Borrower class
class Borrower(Base):

    __tablename__ = "borrower"

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    email= Column(String(80), unique=True)
    phone = Column(Integer)
    books = relationship('Book', back_populates='borrower')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    