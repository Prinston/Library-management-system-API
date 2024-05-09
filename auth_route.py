from datetime import timedelta, datetime
from utils import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import  User, SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError



auth_router = APIRouter(prefix="/auth", tags=['auth'])

SECRET_KEY = 'c6fe1dae80152a34dc6eae9c240d341a8291422137ab6b32712fe2fa3cbd353e'
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



@auth_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user:CreateUserRequest, db: Session = Depends(get_db), ):
    new_user = User(username = user.username, email = user.email, hashed_password = pwd_context.hash(user.password))
    
    

    db.add(new_user)
    db.commit()
    return new_user

@auth_router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db),data_form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data_form.username, data_form.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate User")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User")
    
















    