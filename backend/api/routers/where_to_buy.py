from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas

router = APIRouter(prefix="/where-to-buy", tags=["where-to-buy"])


@router.post("/", response_model=schemas.WhereToBuy, status_code=status.HTTP_201_CREATED)
def create_where_to_buy(
    where_to_buy: schemas.WhereToBuyCreate,
    db: Session = Depends(get_db)
):
    """Создать новую точку продаж"""
    return crud.create_where_to_buy(db=db, where_to_buy_in=where_to_buy)


@router.get("/", response_model=List[schemas.WhereToBuy])
def list_where_to_buy(
    skip: int = 0,
    limit: int = 100,
    location: str = None,
    db: Session = Depends(get_db)
):
    """Получить список точек продаж"""
    where_to_buy_list = crud.list_where_to_buy(db=db, skip=skip, limit=limit, location=location)
    return where_to_buy_list


@router.get("/{where_to_buy_id}", response_model=schemas.WhereToBuy)
def get_where_to_buy(
    where_to_buy_id: int,
    db: Session = Depends(get_db)
):
    """Получить точку продаж по ID"""
    where_to_buy = crud.get_where_to_buy(db=db, where_to_buy_id=where_to_buy_id)
    if where_to_buy is None:
        raise HTTPException(status_code=404, detail="Точка продаж не найдена")
    return where_to_buy


@router.put("/{where_to_buy_id}", response_model=schemas.WhereToBuy)
def update_where_to_buy(
    where_to_buy_id: int,
    where_to_buy_update: schemas.WhereToBuyUpdate,
    db: Session = Depends(get_db)
):
    """Обновить точку продаж"""
    where_to_buy = crud.get_where_to_buy(db=db, where_to_buy_id=where_to_buy_id)
    if where_to_buy is None:
        raise HTTPException(status_code=404, detail="Точка продаж не найдена")
    return crud.update_where_to_buy(db=db, where_to_buy=where_to_buy, where_to_buy_in=where_to_buy_update)


@router.delete("/{where_to_buy_id}")
def delete_where_to_buy(
    where_to_buy_id: int,
    db: Session = Depends(get_db)
):
    """Удалить точку продаж"""
    where_to_buy = crud.get_where_to_buy(db=db, where_to_buy_id=where_to_buy_id)
    if where_to_buy is None:
        raise HTTPException(status_code=404, detail="Точка продаж не найдена")
    crud.delete_where_to_buy(db=db, where_to_buy=where_to_buy)
    return {"message": "Точка продаж успешно удалена"}
