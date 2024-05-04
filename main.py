from fastapi import FastAPI
from database import Base, engine
from book_routes import api_router
from borrower_route import borrow_router





Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome"}


app.include_router(api_router)
app.include_router(borrow_router)
