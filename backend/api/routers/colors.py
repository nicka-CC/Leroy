from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...uploads import save_upload

router = APIRouter(prefix="/colors", tags=["colors"])


@router.post("/", response_model=schemas.Color, status_code=status.HTTP_201_CREATED)
def create_color(
    db: Session = Depends(get_db),
    name: str = Form(...),
    hex_code: Optional[str] = Form(None),
    additional_price: float = Form(0),
    photos: List[UploadFile] = File(default=[])
):
    """Создать новый цвет с загрузкой фотографий"""
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="color"))
    
    # Создание объекта цвета
    color_data = {
        "name": name,
        "hex_code": hex_code,
        "additional_price": additional_price,
        "photos": photo_urls
    }
    
    color_in = schemas.ColorCreate(**color_data)
    return crud.create_color(db=db, color_in=color_in)


@router.get("/", response_model=List[schemas.Color])
def list_colors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список цветов"""
    colors = crud.list_colors(db=db, skip=skip, limit=limit)
    return colors


@router.get("/{color_id}", response_model=schemas.Color)
def get_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """Получить цвет по ID"""
    color = crud.get_color(db=db, color_id=color_id)
    if color is None:
        raise HTTPException(status_code=404, detail="Цвет не найден")
    return color


@router.put("/{color_id}", response_model=schemas.Color)
def update_color(
    color_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    hex_code: Optional[str] = Form(None),
    additional_price: Optional[float] = Form(None),
    photos: List[UploadFile] = File(default=[])
):
    """Обновить цвет с загрузкой фотографий"""
    color = crud.get_color(db=db, color_id=color_id)
    if color is None:
        raise HTTPException(status_code=404, detail="Цвет не найден")
    
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="color"))
    
    # Создание объекта обновления
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if hex_code is not None:
        update_data["hex_code"] = hex_code
    if additional_price is not None:
        update_data["additional_price"] = additional_price
    if photo_urls:
        update_data["photos"] = photo_urls
    
    color_update = schemas.ColorUpdate(**update_data)
    return crud.update_color(db=db, color=color, color_in=color_update)


@router.delete("/{color_id}")
def delete_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """Удалить цвет"""
    color = crud.get_color(db=db, color_id=color_id)
    if color is None:
        raise HTTPException(status_code=404, detail="Цвет не найден")
    crud.delete_color(db=db, color=color)
    return {"message": "Цвет успешно удален"}
