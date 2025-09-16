from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...auth import require_access, AuthContext

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=schemas.Order, status_code=status.HTTP_201_CREATED, summary="Создать заказ")
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(1))):
    user = crud.get_user_by_id(db, order_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверить, что все модули существуют
    if order_in.module_ids:
        for module_id in order_in.module_ids:
            module = crud.get_module(db, module_id)
            if not module:
                raise HTTPException(status_code=404, detail=f"Модуль с ID {module_id} не найден")
    
    return crud.create_order(db, order_in)


@router.get("", response_model=List[schemas.Order], summary="Список заказов (фильтр по user_id)")
def list_orders(user_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_orders(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=schemas.Order, summary="Получить заказ")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.put("/{order_id}", response_model=schemas.Order, summary="Обновить заказ")
def update_order(order_id: int, order_in: schemas.OrderUpdate, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(2))):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    # Проверить, что все модули существуют
    if order_in.module_ids:
        for module_id in order_in.module_ids:
            module = crud.get_module(db, module_id)
            if not module:
                raise HTTPException(status_code=404, detail=f"Модуль с ID {module_id} не найден")
    
    return crud.update_order(db, order, order_in)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить заказ")
def delete_order(order_id: int, db: Session = Depends(get_db), ctx: AuthContext = Depends(require_access(3))):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    crud.delete_order(db, order)
    return None