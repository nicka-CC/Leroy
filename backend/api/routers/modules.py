from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas, models
from ...uploads import save_upload

router = APIRouter(prefix="/modules", tags=["modules"])


@router.post("/", response_model=schemas.Module, status_code=status.HTTP_201_CREATED)
def create_module(
    db: Session = Depends(get_db),
    name: str = Form(...),
    article: str = Form(...),
    price: float = Form(...),
    discounted_price: Optional[float] = Form(None),
    technical_details: Optional[str] = Form(None),
    assembly_instruction: Optional[str] = Form(None),
    color_ids: Optional[str] = Form(None),  # JSON строка с массивом ID
    photos: List[UploadFile] = File(default=[])
):
    """Создать новый модуль с загрузкой фотографий"""
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="module"))
    
    # Парсинг color_ids если они переданы
    color_ids_list = []
    if color_ids:
        try:
            import json
            color_ids_list = json.loads(color_ids)
        except:
            color_ids_list = []
    
    # Создание объекта модуля
    module_data = {
        "name": name,
        "article": article,
        "price": price,
        "discounted_price": discounted_price,
        "technical_details": technical_details,
        "assembly_instruction": assembly_instruction,
        "photos": photo_urls,
        "color_ids": color_ids_list
    }
    
    module_in = schemas.ModuleCreate(**module_data)
    return crud.create_module(db=db, module_in=module_in)


@router.get("/", response_model=List[schemas.Module])
def list_modules(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    db: Session = Depends(get_db)
):
    """Получить список модулей"""
    modules = crud.list_modules(db=db, skip=skip, limit=limit, name=name)
    return modules


@router.get("/{module_id}", response_model=schemas.Module)
def get_module(
    module_id: int,
    db: Session = Depends(get_db)
):
    """Получить модуль по ID"""
    module = crud.get_module(db=db, module_id=module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    return module


@router.put("/{module_id}", response_model=schemas.Module)
def update_module(
    module_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    article: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    discounted_price: Optional[float] = Form(None),
    technical_details: Optional[str] = Form(None),
    assembly_instruction: Optional[str] = Form(None),
    color_ids: Optional[str] = Form(None),
    photos: List[UploadFile] = File(default=[])
):
    """Обновить модуль с загрузкой фотографий"""
    module = crud.get_module(db=db, module_id=module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    
    # Обработка загруженных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="module"))
    
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
    if name is not None:
        update_data["name"] = name
    if article is not None:
        update_data["article"] = article
    if price is not None:
        update_data["price"] = price
    if discounted_price is not None:
        update_data["discounted_price"] = discounted_price
    if technical_details is not None:
        update_data["technical_details"] = technical_details
    if assembly_instruction is not None:
        update_data["assembly_instruction"] = assembly_instruction
    if photo_urls:
        update_data["photos"] = photo_urls
    if color_ids_list is not None:
        update_data["color_ids"] = color_ids_list
    
    module_update = schemas.ModuleUpdate(**update_data)
    return crud.update_module(db=db, module=module, module_in=module_update)


@router.delete("/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db)
):
    """Удалить модуль"""
    module = crud.get_module(db=db, module_id=module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    crud.delete_module(db=db, module=module)
    return {"message": "Модуль успешно удален"}
