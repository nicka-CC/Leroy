from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...auth import require_access, AuthContext

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.User, status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(3))):
    existing_email = crud.get_user_by_email(db, user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    existing_login = crud.get_user_by_login(db, user_in.login)
    if existing_login:
        raise HTTPException(status_code=400, detail="Логин уже занят")
    
    return crud.create_user(db, user_in)


@router.get("", response_model=List[schemas.User], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User, summary="Получить пользователя по ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schemas.User, summary="Обновить пользователя")
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(3))):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(3))):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
    return None
