from datetime import timedelta, datetime
from utils import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import User, SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import logging
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Create a new APIRouter instance for authentication routes
auth_router = APIRouter(prefix="/auth", tags=['auth'])

# Secret key and algorithm for JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Create a password context for hashing passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Create an OAuth2PasswordBearer instance for token management
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Pydantic model for creating a new user
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Endpoint to create a new user
@auth_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exists")

        new_user = User(username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# Endpoint to generate an access token for authentication
@auth_router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), data_form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data_form.username, data_form.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate User")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}

# Function to authenticate a user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

# Function to create an access token
def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to get the current user using the access token
def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User")

    
















    