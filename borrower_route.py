from fastapi import APIRouter, Depends, HTTPException, status
from book_routes import get_db
from sqlalchemy.orm import Session
from database import  Borrower as Borrower_DB
from models import BorrowModel, UpdateBorrower


borrow_router = APIRouter(prefix="/api", tags=['Borrower'])

@borrow_router.get("/borrowers")
def get_borrowers(db: Session = Depends(get_db)):
    try:
        borrowers = db.query(Borrower_DB).all()
        return borrowers
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@borrow_router.get("/borrowers/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    borrower = db.query(Borrower_DB).filter(Borrower_DB.id == id).first()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower Not Found")
    return borrower

@borrow_router.post("/borrowers")
def create(borrower: BorrowModel , db: Session = Depends(get_db)):
    existing_borrower = db.query(Borrower_DB).filter(Borrower_DB.name == borrower.name).first()
    if existing_borrower:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Borrower Already Exist")
    new_borrower = Borrower_DB(id = borrower.id, name = borrower.name, email = borrower.email, phone = borrower.phone)
    db.add(new_borrower)
    db.commit()
    db.refresh(new_borrower)
    return new_borrower

@borrow_router.put("/borrowers/{id}")
def update(id: int, update_borrower: UpdateBorrower, db: Session = Depends(get_db)):
    borrower = db.query(Borrower_DB).filter(Borrower_DB.id == id).first()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower Not Found")
    try:
        for field in ["name", "email", "phone"]:
            new_value = getattr(update_borrower, field)
            if new_value is not None and new_value != "":
                setattr(borrower, field, new_value)

        db.commit()
        db.refresh(borrower)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Borrower Not Updated")
    return borrower


@borrow_router.delete("/borrowers/{id}")
def delete_borrower(id: int, db: Session = Depends(get_db)):
    borrower = db.query(Borrower_DB).filter(Borrower_DB.id == id).first()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrower Not Found")
    db.delete(borrower)
    db.commit()

    return {"Message": "Borrower Deleted Successfully"}
