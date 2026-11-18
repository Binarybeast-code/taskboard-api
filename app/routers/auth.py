from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(
        select(models.User).where(models.User.username == user_in.username)
    )
    if existing:
        raise HTTPException(status_code=409, detail="Username already exist")
    user = models.User(
        username=user_in.username, hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(get_db), db: Session = Depends(get_db)
):

    user = db.scalar(select(models.User).where(models.User.username == form.username))
    if not user or not verify_password:
        raise HTTPException(
            status_code=401,
            detail="Ïncorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_Token=create_access_token(str(user.i)), token_type="bearer")
