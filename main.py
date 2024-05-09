from fastapi import FastAPI,HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import Base, engine
from book_routes import api_router
from borrower_route import borrow_router
from auth_route import auth_router
from auth_route import get_current_user
from utils import get_db

# Create the database tables based on the models
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Define a route for the home page
@app.get("/", status_code=status.HTTP_200_OK)
def user(user: dict = Depends(get_current_user), db:Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return {"User": user}



# Include the API routers for books and borrowers
app.include_router(api_router)
app.include_router(borrow_router)
app.include_router(auth_router)