from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("/", response_model=schemas.Shop, status_code=status.HTTP_201_CREATED)
def create_shop(
    shop: schemas.ShopCreate,
    db: Session = Depends(get_db)
):
    """Создать новый магазин"""
    return crud.create_shop(db=db, shop_in=shop)


@router.get("/", response_model=List[schemas.Shop])
def list_shops(
    skip: int = 0,
    limit: int = 100,
    city: str = None,
    db: Session = Depends(get_db)
):
    """Получить список магазинов"""
    shops = crud.list_shops(db=db, skip=skip, limit=limit, city=city)
    return shops


@router.get("/{shop_id}", response_model=schemas.Shop)
def get_shop(
    shop_id: int,
    db: Session = Depends(get_db)
):
    """Получить магазин по ID"""
    shop = crud.get_shop(db=db, shop_id=shop_id)
    if shop is None:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return shop


@router.put("/{shop_id}", response_model=schemas.Shop)
def update_shop(
    shop_id: int,
    shop_update: schemas.ShopUpdate,
    db: Session = Depends(get_db)
):
    """Обновить магазин"""
    shop = crud.get_shop(db=db, shop_id=shop_id)
    if shop is None:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return crud.update_shop(db=db, shop=shop, shop_in=shop_update)


@router.delete("/{shop_id}")
def delete_shop(
    shop_id: int,
    db: Session = Depends(get_db)
):
    """Удалить магазин"""
    shop = crud.get_shop(db=db, shop_id=shop_id)
    if shop is None:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    crud.delete_shop(db=db, shop=shop)
    return {"message": "Магазин успешно удален"}
