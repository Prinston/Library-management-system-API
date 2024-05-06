from pydantic import BaseModel
from typing import Optional

# Pydantic model for a book
class BookModel(BaseModel):
    id : int  
    title : str  
    author : str  
    ISBN : str  
    quantity_available : int  

# Pydantic model for updating a book
class UpdateBook(BaseModel):
    title : Optional[str] = None  
    author : Optional[str] = None  
    ISBN : Optional[str] = None  
    quantity_available : Optional[int] = None  

# Pydantic model for a borrower
class BorrowModel(BaseModel):
    id : int  
    name : str 
    email: str 
    phone : int  

# Pydantic model for updating a borrower
class UpdateBorrower(BaseModel):
    name: Optional[str] = None  
    email: Optional[str] = None  
    phone: Optional[int] = None  


# Pydantic model for borrowing 
class BorrowSuccessResponse(BaseModel):
    message: str