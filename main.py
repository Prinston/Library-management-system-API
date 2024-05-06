from fastapi import FastAPI
from database import Base, engine
from book_routes import api_router
from borrower_route import borrow_router

# Create the database tables based on the models
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Define a route for the home page
@app.get("/")
def home():
    return {"message": "Welcome"}

# Include the API routers for books and borrowers
app.include_router(api_router)
app.include_router(borrow_router)
