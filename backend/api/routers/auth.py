from __future__ import annotations

import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", summary="Регистрация, выдача токена")
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_email = crud.get_user_by_email(db, user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user_in.password)
    user = crud.create_user(db, user_in, password_hasher=lambda _: hashed)
    token = create_access_token(user_id=user.id, access_level=user.access_level)
    return {"access_token": token, "token_type": "bearer", "level": user.access_level}


@router.post("/login", summary="Логин, выдача токена")
def login(login: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, login)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(user_id=user.id, access_level=user.access_level)
    return {"access_token": token, "token_type": "bearer", "level": user.access_level}


@router.post("/elevate", summary="Выдать токен с повышенным уровнем доступа (только для админа)")
def elevate_token(user_id: int, level: int = 3, x_admin_secret: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    admin_secret_env = os.getenv("ADMIN_SECRET", "change-me")
    if not x_admin_secret or x_admin_secret != admin_secret_env:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin secret")
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Invalid level")
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.set_user_access_level(db, user, level)
    token = create_access_token(user_id=user.id, access_level=user.access_level)
    return {"access_token": token, "token_type": "bearer", "level": user.access_level, "user_id": user.id}
