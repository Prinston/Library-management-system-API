from pydantic import BaseModel
from typing import Optional



class BookModel(BaseModel):
    id : int
    title : str
    author : str
    ISBN : str
    quantity_available : int

class UpdateBook(BaseModel):
    
    title : Optional[str] = None
    author : Optional[str] = None
    ISBN :Optional[str] = None
    quantity_available : Optional[int]


class BorrowModel(BaseModel):
    id : int
    name : str
    email: str
    phone : int

class UpdateBorrower(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None

    
   