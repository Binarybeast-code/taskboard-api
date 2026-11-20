import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 

from app import models
from app.config import settings

from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #knows how to read the token from the request

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_error = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_error

    user = db.get(models.User, user_id)
    if user is None:
        raise credentials_error
    return user
