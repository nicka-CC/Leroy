from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...auth import require_access, AuthContext

router = APIRouter(prefix="/users/{user_id}/cart", tags=["cart"])


@router.get("", response_model=schemas.Cart, summary="Получить корзину пользователя")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return crud.get_or_create_cart(db, user_id=user_id)


@router.put("", response_model=schemas.Cart, summary="Обновить корзину пользователя")
def update_cart(user_id: int, cart_update: schemas.CartUpdate, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(1))):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    cart = crud.get_or_create_cart(db, user_id=user_id)
    return crud.update_cart(db, cart=cart, cart_in=cart_update)


@router.post("/modules/{module_id}", response_model=schemas.Cart, summary="Добавить модуль в корзину")
def add_module_to_cart(user_id: int, module_id: int, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(1))):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    module = crud.get_module(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    
    return crud.add_module_to_cart(db, user_id=user_id, module_id=module_id)


@router.delete("/modules/{module_id}", response_model=schemas.Cart, summary="Удалить модуль из корзины")
def remove_module_from_cart(user_id: int, module_id: int, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(1))):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    module = crud.get_module(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    
    return crud.remove_module_from_cart(db, user_id=user_id, module_id=module_id)