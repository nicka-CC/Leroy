from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas
from ...uploads import save_upload

router = APIRouter(prefix="/news", tags=["news"])


@router.post("/", response_model=schemas.News, status_code=status.HTTP_201_CREATED)
def create_news(
    db: Session = Depends(get_db),
    title: str = Form(...),
    text1: Optional[str] = Form(None),
    text2: Optional[str] = Form(None),
    main_photo: Optional[UploadFile] = File(None),
    photos: List[UploadFile] = File(default=[])
):
    """Создать новую новость с загрузкой фотографий"""
    # Обработка главного фото
    main_photo_url = None
    if main_photo and main_photo.filename:
        main_photo_url = save_upload(main_photo, prefix="news_main")
    
    # Обработка дополнительных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="news"))
    
    # Создание объекта новости
    news_data = {
        "title": title,
        "text1": text1,
        "text2": text2,
        "main_photo": main_photo_url,
        "photos": photo_urls
    }
    
    news_in = schemas.NewsCreate(**news_data)
    return crud.create_news(db=db, news_in=news_in)


@router.get("/", response_model=List[schemas.News])
def list_news(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список новостей"""
    news_list = crud.list_news(db=db, skip=skip, limit=limit)
    return news_list


@router.get("/{news_id}", response_model=schemas.News)
def get_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Получить новость по ID"""
    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news


@router.put("/{news_id}", response_model=schemas.News)
def update_news(
    news_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    text1: Optional[str] = Form(None),
    text2: Optional[str] = Form(None),
    main_photo: Optional[UploadFile] = File(None),
    photos: List[UploadFile] = File(default=[])
):
    """Обновить новость с загрузкой фотографий"""
    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    
    # Обработка главного фото
    main_photo_url = None
    if main_photo and main_photo.filename:
        main_photo_url = save_upload(main_photo, prefix="news_main")
    
    # Обработка дополнительных фотографий
    photo_urls = []
    for photo in photos:
        if photo.filename:
            photo_urls.append(save_upload(photo, prefix="news"))
    
    # Создание объекта обновления
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if text1 is not None:
        update_data["text1"] = text1
    if text2 is not None:
        update_data["text2"] = text2
    if main_photo_url is not None:
        update_data["main_photo"] = main_photo_url
    if photo_urls:
        update_data["photos"] = photo_urls
    
    news_update = schemas.NewsUpdate(**update_data)
    return crud.update_news(db=db, news=news, news_in=news_update)


@router.delete("/{news_id}")
def delete_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Удалить новость"""
    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    crud.delete_news(db=db, news=news)
    return {"message": "Новость успешно удалена"}
