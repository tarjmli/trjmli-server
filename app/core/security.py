from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from requests import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer # type: ignore
from models.user import User
from db.session import SessionLocal
from models import user
from jose import JWTError
from core.config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
 
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(email=user.email, id=user.id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")