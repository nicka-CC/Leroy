from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...uploads import save_upload

router = APIRouter(prefix="/furniture", tags=["furniture"])


@router.post("/", response_model=schemas.Furniture, status_code=status.HTTP_201_CREATED)
def create_furniture(
    db: Session = Depends(get_db),
    furniture_type: str = Form(...),
    name: str = Form(...),
    price: float = Form(...),
    discounted_price: Optional[float] = Form(None),
    technical_characteristics: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    article: str = Form(...),
    color_ids: Optional[str] = Form(None),  # JSON строка с массивом ID
    photos: List[UploadFile] = File(default=[])
):
    """Создать новую мебель с загрузкой фотографий"""
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="furniture"))
    
    # Парсинг color_ids если они переданы
    color_ids_list = []
    if color_ids:
        try:
            import json
            color_ids_list = json.loads(color_ids)
        except:
            color_ids_list = []
    
    # Создание объекта мебели
    furniture_data = {
        "furniture_type": furniture_type,
        "name": name,
        "price": price,
        "discounted_price": discounted_price,
        "technical_characteristics": technical_characteristics,
        "model": model,
        "article": article,
        "photos": photo_urls,
        "color_ids": color_ids_list
    }
    
    furniture_in = schemas.FurnitureCreate(**furniture_data)
    return crud.create_furniture(db=db, furniture_in=furniture_in)


@router.get("/", response_model=List[schemas.Furniture])
def list_furniture(
    skip: int = 0,
    limit: int = 100,
    furniture_type: str = None,
    db: Session = Depends(get_db)
):
    """Получить список мебели"""
    furniture_items = crud.list_furniture(db=db, skip=skip, limit=limit, furniture_type=furniture_type)
    return furniture_items


@router.get("/{furniture_id}", response_model=schemas.Furniture)
def get_furniture(
    furniture_id: int,
    db: Session = Depends(get_db)
):
    """Получить мебель по ID"""
    furniture = crud.get_furniture(db=db, furniture_id=furniture_id)
    if furniture is None:
        raise HTTPException(status_code=404, detail="Мебель не найдена")
    return furniture


@router.put("/{furniture_id}", response_model=schemas.Furniture)
def update_furniture(
    furniture_id: int,
    db: Session = Depends(get_db),
    furniture_type: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    discounted_price: Optional[float] = Form(None),
    technical_characteristics: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    article: Optional[str] = Form(None),
    color_ids: Optional[str] = Form(None),
    photos: List[UploadFile] = File(default=[])
):
    """Обновить мебель с загрузкой фотографий"""
    furniture = crud.get_furniture(db=db, furniture_id=furniture_id)
    if furniture is None:
        raise HTTPException(status_code=404, detail="Мебель не найдена")
    
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="furniture"))
    
    # Парсинг color_ids если они переданы
    color_ids_list = None
    if color_ids:
        try:
            import json
            color_ids_list = json.loads(color_ids)
        except:
            color_ids_list = None
    
    # Создание объекта обновления
    update_data = {}
    if furniture_type is not None:
        update_data["furniture_type"] = furniture_type
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    if discounted_price is not None:
        update_data["discounted_price"] = discounted_price
    if technical_characteristics is not None:
        update_data["technical_characteristics"] = technical_characteristics
    if model is not None:
        update_data["model"] = model
    if article is not None:
        update_data["article"] = article
    if photo_urls:
        update_data["photos"] = photo_urls
    if color_ids_list is not None:
        update_data["color_ids"] = color_ids_list
    
    furniture_update = schemas.FurnitureUpdate(**update_data)
    return crud.update_furniture(db=db, furniture=furniture, furniture_in=furniture_update)


@router.delete("/{furniture_id}")
def delete_furniture(
    furniture_id: int,
    db: Session = Depends(get_db)
):
    """Удалить мебель"""
    furniture = crud.get_furniture(db=db, furniture_id=furniture_id)
    if furniture is None:
        raise HTTPException(status_code=404, detail="Мебель не найдена")
    crud.delete_furniture(db=db, furniture=furniture)
    return {"message": "Мебель успешно удалена"}
