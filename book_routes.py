from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
from sqlalchemy.orm import Session
from database import Book as Book_DB, Borrower as Borrower_DB
from models import BookModel, UpdateBook, BorrowSuccessResponse

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creating a new APIRouter instance with a prefix and tags
api_router = APIRouter(prefix="/api", tags=['Books'])

# GET endpoint to retrieve all books
@api_router.get("/books", response_model=list[BookModel], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    try:
        books = db.query(Book_DB).all()
        return books
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# GET endpoint to retrieve a book by its ID
@api_router.get("/books/{id}", response_model=BookModel, status_code=status.HTTP_200_OK)
def get_by_id(id: int, db: Session = Depends(get_db)):
    book = db.query(Book_DB).filter(Book_DB.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    return book

# POST endpoint to create a new book
@api_router.post("/books", response_model=BookModel,status_code=status.HTTP_201_CREATED)
def create(book: BookModel, db: Session = Depends(get_db)):
    existing_book = db.query(Book_DB).filter(Book_DB.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book Already Exist")
    new_book = Book_DB(id=book.id, title=book.title, author=book.author, ISBN=book.ISBN, quantity_available=book.quantity_available)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# POST endpoint to borrow a book by ID and borrower ID
@api_router.post("/books/{id}/{borrower_id}", response_model=BorrowSuccessResponse, status_code=status.HTTP_200_OK)
def borrow_book(id: int, borrower_id: int, db: Session = Depends(get_db)):
    book = db.query(Book_DB).filter(Book_DB.id == id).first()
    borrower = db.query(Borrower_DB).filter(Borrower_DB.id == borrower_id).first()

    if not book or not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book or Borrower Not Found")
    if book.quantity_available <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No copies available")

    book.borrower_id = borrower_id
    book.quantity_available -= 1
    db.commit()

    return {"message": "Book borrowed successfully"}


# PUT endpoint to update a book by ID
@api_router.put("/books/{id}", response_model=BookModel, status_code=status.HTTP_200_OK)
def update(id: int, update_book: UpdateBook, db: Session = Depends(get_db)):
    book = db.query(Book_DB).filter(Book_DB.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    try:
        for field in ['title', 'author', 'ISBN', 'quantity_available', 'borrower_id']:
            new_value = getattr(update_book, field)
            if new_value is not None:
                setattr(book, field, new_value)

        db.commit()
        db.refresh(book)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Not Updated")
    return book

# DELETE endpoint to delete a book by ID
@api_router.delete("/books/{id}",status_code=status.HTTP_200_OK)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book_DB).filter(Book_DB.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    db.delete(book)
    db.commit()

    return {"Message": "Book Deleted Successfully"}


