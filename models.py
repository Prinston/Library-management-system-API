from pydantic import BaseModel
from typing import Optional



  
class UpdateBook(BaseModel):

    title : Optional[str] = None
    author : Optional[str] = None
    ISBN :Optional[str] = None
    quantity_available : Optional[int] = None

class BookModel(UpdateBook):
    id : int
  
   

class UpdateBorrower(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None

class BorrowModel(UpdateBorrower):
    id : int


# Pydantic model for borrowing 
class BorrowSuccessResponse(BaseModel):
    message: str