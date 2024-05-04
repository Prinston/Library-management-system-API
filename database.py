from sqlalchemy import create_engine, String, Column, Integer, ForeignKey
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv




load_dotenv()




DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")


DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}/{DB_NAME}"


engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)





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

class Borrower(Base):

    __tablename__ = "borrower"

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    email= Column(String(80), unique=True)
    phone = Column(Integer)
    books = relationship('Book', back_populates='borrower')
