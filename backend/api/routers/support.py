from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ... import crud, schemas

router = APIRouter(prefix="/support", tags=["support"])


@router.post("/requests", response_model=schemas.SupportRequest, status_code=status.HTTP_201_CREATED)
def create_support_request(
    request: schemas.SupportRequestCreate,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Создать новый запрос в поддержку"""
    return crud.create_support_request(db=db, request_in=request, user_id=user_id)


@router.get("/requests", response_model=List[schemas.SupportRequest])
def list_support_requests(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список запросов в поддержку"""
    requests = crud.list_support_requests(db=db, skip=skip, limit=limit, status=status)
    return requests


@router.get("/requests/{request_id}", response_model=schemas.SupportRequest)
def get_support_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """Получить запрос в поддержку по ID"""
    request = crud.get_support_request(db=db, request_id=request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Запрос в поддержку не найден")
    return request


@router.put("/requests/{request_id}", response_model=schemas.SupportRequest)
def update_support_request(
    request_id: int,
    request_update: schemas.SupportRequestUpdate,
    db: Session = Depends(get_db)
):
    """Обновить запрос в поддержку"""
    request = crud.get_support_request(db=db, request_id=request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Запрос в поддержку не найден")
    return crud.update_support_request(db=db, request=request, request_in=request_update)


@router.delete("/requests/{request_id}")
def delete_support_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """Удалить запрос в поддержку"""
    request = crud.get_support_request(db=db, request_id=request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Запрос в поддержку не найден")
    crud.delete_support_request(db=db, request=request)
    return {"message": "Запрос в поддержку успешно удален"}
