from __future__ import annotations

from typing import Optional, Sequence, List

from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session

from . import models, schemas


# ======================
# User CRUD
# ======================

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.get(models.User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.email == email)
    return db.execute(stmt).scalars().first()


def get_user_by_login(db: Session, login: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.login == login)
    return db.execute(stmt).scalars().first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[models.User]:
    stmt = select(models.User).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_user(db: Session, user_in: schemas.UserCreate, password_hasher=lambda s: s) -> models.User:
    hashed_password = password_hasher(user_in.password)
    user = models.User(
        full_name=user_in.full_name,
        login=user_in.login,
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=hashed_password,
        access_level=user_in.access_level,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: models.User, user_in: schemas.UserUpdate, password_hasher=lambda s: s) -> models.User:
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.login is not None:
        user.login = user_in.login
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.phone_number is not None:
        user.phone_number = user_in.phone_number
    if user_in.password is not None:
        user.hashed_password = password_hasher(user_in.password)
    if user_in.access_level is not None:
        user.access_level = user_in.access_level
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User) -> None:
    db.delete(user)
    db.commit()


# ======================
# Color CRUD
# ======================

def create_color(db: Session, color_in: schemas.ColorCreate) -> models.Color:
    color = models.Color(**color_in.dict())
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def get_color(db: Session, color_id: int) -> Optional[models.Color]:
    return db.get(models.Color, color_id)


def list_colors(db: Session, skip: int = 0, limit: int = 100) -> Sequence[models.Color]:
    stmt = select(models.Color).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_color(db: Session, color: models.Color, color_in: schemas.ColorUpdate) -> models.Color:
    for field, value in color_in.dict(exclude_unset=True).items():
        setattr(color, field, value)
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def delete_color(db: Session, color: models.Color) -> None:
    db.delete(color)
    db.commit()


# ======================
# Module CRUD
# ======================

def create_module(db: Session, module_in: schemas.ModuleCreate) -> models.Module:
    module_data = module_in.dict()
    color_ids = module_data.pop('color_ids', [])
    
    module = models.Module(**module_data)
    db.add(module)
    db.flush()  # получить ID модуля
    
    # Добавить связи с цветами
    if color_ids:
        colors = db.execute(select(models.Color).where(models.Color.id.in_(color_ids))).scalars().all()
        module.colors.extend(colors)
    
    db.commit()
    db.refresh(module)
    return module


def get_module(db: Session, module_id: int) -> Optional[models.Module]:
    return db.get(models.Module, module_id)


def list_modules(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None) -> Sequence[models.Module]:
    stmt = select(models.Module)
    if name:
        stmt = stmt.where(models.Module.name.ilike(f"%{name}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_module(db: Session, module: models.Module, module_in: schemas.ModuleUpdate) -> models.Module:
    module_data = module_in.dict(exclude_unset=True)
    color_ids = module_data.pop('color_ids', None)
    
    for field, value in module_data.items():
        setattr(module, field, value)
    
    # Обновить связи с цветами если указано
    if color_ids is not None:
        colors = db.execute(select(models.Color).where(models.Color.id.in_(color_ids))).scalars().all()
        module.colors = colors
    
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module: models.Module) -> None:
    db.delete(module)
    db.commit()


# ======================
# Furniture CRUD
# ======================

def create_furniture(db: Session, furniture_in: schemas.FurnitureCreate) -> models.Furniture:
    furniture_data = furniture_in.dict()
    color_ids = furniture_data.pop('color_ids', [])
    
    furniture = models.Furniture(**furniture_data)
    db.add(furniture)
    db.flush()  # получить ID мебели
    
    # Добавить связи с цветами
    if color_ids:
        colors = db.execute(select(models.Color).where(models.Color.id.in_(color_ids))).scalars().all()
        furniture.colors.extend(colors)
    
    db.commit()
    db.refresh(furniture)
    return furniture


def get_furniture(db: Session, furniture_id: int) -> Optional[models.Furniture]:
    return db.get(models.Furniture, furniture_id)


def list_furniture(db: Session, skip: int = 0, limit: int = 100, furniture_type: Optional[str] = None) -> Sequence[models.Furniture]:
    stmt = select(models.Furniture)
    if furniture_type:
        stmt = stmt.where(models.Furniture.furniture_type.ilike(f"%{furniture_type}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_furniture(db: Session, furniture: models.Furniture, furniture_in: schemas.FurnitureUpdate) -> models.Furniture:
    furniture_data = furniture_in.dict(exclude_unset=True)
    color_ids = furniture_data.pop('color_ids', None)
    
    for field, value in furniture_data.items():
        setattr(furniture, field, value)
    
    # Обновить связи с цветами если указано
    if color_ids is not None:
        colors = db.execute(select(models.Color).where(models.Color.id.in_(color_ids))).scalars().all()
        furniture.colors = colors
    
    db.add(furniture)
    db.commit()
    db.refresh(furniture)
    return furniture


def delete_furniture(db: Session, furniture: models.Furniture) -> None:
    db.delete(furniture)
    db.commit()


# ======================
# Cart CRUD
# ======================

def get_or_create_cart(db: Session, user_id: int) -> models.Cart:
    stmt = select(models.Cart).where(models.Cart.user_id == user_id)
    cart = db.execute(stmt).scalars().first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def update_cart(db: Session, cart: models.Cart, cart_in: schemas.CartUpdate) -> models.Cart:
    cart_data = cart_in.dict(exclude_unset=True)
    module_ids = cart_data.pop('module_ids', None)
    
    for field, value in cart_data.items():
        setattr(cart, field, value)
    
    # Обновить связи с модулями если указано
    if module_ids is not None:
        modules = db.execute(select(models.Module).where(models.Module.id.in_(module_ids))).scalars().all()
        cart.modules = modules
    
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_module_to_cart(db: Session, user_id: int, module_id: int) -> models.Cart:
    cart = get_or_create_cart(db, user_id)
    module = db.get(models.Module, module_id)
    if module and module not in cart.modules:
        cart.modules.append(module)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def remove_module_from_cart(db: Session, user_id: int, module_id: int) -> models.Cart:
    cart = get_or_create_cart(db, user_id)
    module = db.get(models.Module, module_id)
    if module and module in cart.modules:
        cart.modules.remove(module)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


# ======================
# Order CRUD
# ======================

def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    order_data = order_in.dict()
    module_ids = order_data.pop('module_ids', [])
    
    order = models.Order(**order_data)
    db.add(order)
    db.flush()  # получить ID заказа
    
    # Добавить связи с модулями
    if module_ids:
        modules = db.execute(select(models.Module).where(models.Module.id.in_(module_ids))).scalars().all()
        order.modules.extend(modules)
    
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.get(models.Order, order_id)


def list_orders(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> Sequence[models.Order]:
    stmt = select(models.Order)
    if user_id is not None:
        stmt = stmt.where(models.Order.user_id == user_id)
    stmt = stmt.order_by(models.Order.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_order(db: Session, order: models.Order, order_in: schemas.OrderUpdate) -> models.Order:
    order_data = order_in.dict(exclude_unset=True)
    module_ids = order_data.pop('module_ids', None)
    
    for field, value in order_data.items():
        setattr(order, field, value)
    
    # Обновить связи с модулями если указано
    if module_ids is not None:
        modules = db.execute(select(models.Module).where(models.Module.id.in_(module_ids))).scalars().all()
        order.modules = modules
    
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order: models.Order) -> None:
    db.delete(order)
    db.commit()


# ======================
# News CRUD
# ======================

def create_news(db: Session, news_in: schemas.NewsCreate) -> models.News:
    news = models.News(**news_in.dict())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def get_news(db: Session, news_id: int) -> Optional[models.News]:
    return db.get(models.News, news_id)


def list_news(db: Session, skip: int = 0, limit: int = 100) -> Sequence[models.News]:
    stmt = select(models.News).order_by(models.News.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_news(db: Session, news: models.News, news_in: schemas.NewsUpdate) -> models.News:
    for field, value in news_in.dict(exclude_unset=True).items():
        setattr(news, field, value)
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def delete_news(db: Session, news: models.News) -> None:
    db.delete(news)
    db.commit()


# ======================
# Support Request CRUD
# ======================

def create_support_request(db: Session, request_in: schemas.SupportRequestCreate, user_id: Optional[int] = None) -> models.SupportRequest:
    request = models.SupportRequest(user_id=user_id, **request_in.dict())
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def get_support_request(db: Session, request_id: int) -> Optional[models.SupportRequest]:
    return db.get(models.SupportRequest, request_id)


def list_support_requests(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> Sequence[models.SupportRequest]:
    stmt = select(models.SupportRequest)
    if status:
        stmt = stmt.where(models.SupportRequest.status == status)
    stmt = stmt.order_by(models.SupportRequest.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_support_request(db: Session, request: models.SupportRequest, request_in: schemas.SupportRequestUpdate) -> models.SupportRequest:
    for field, value in request_in.dict(exclude_unset=True).items():
        setattr(request, field, value)
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def delete_support_request(db: Session, request: models.SupportRequest) -> None:
    db.delete(request)
    db.commit()


# ======================
# Shop CRUD
# ======================

def create_shop(db: Session, shop_in: schemas.ShopCreate) -> models.Shop:
    shop = models.Shop(**shop_in.dict())
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


def get_shop(db: Session, shop_id: int) -> Optional[models.Shop]:
    return db.get(models.Shop, shop_id)


def list_shops(db: Session, skip: int = 0, limit: int = 100, city: Optional[str] = None) -> Sequence[models.Shop]:
    stmt = select(models.Shop)
    if city:
        stmt = stmt.where(models.Shop.city.ilike(f"%{city}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_shop(db: Session, shop: models.Shop, shop_in: schemas.ShopUpdate) -> models.Shop:
    for field, value in shop_in.dict(exclude_unset=True).items():
        setattr(shop, field, value)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


def delete_shop(db: Session, shop: models.Shop) -> None:
    db.delete(shop)
    db.commit()


# ======================
# Where To Buy CRUD
# ======================

def create_where_to_buy(db: Session, where_to_buy_in: schemas.WhereToBuyCreate) -> models.WhereToBuy:
    where_to_buy = models.WhereToBuy(**where_to_buy_in.dict())
    db.add(where_to_buy)
    db.commit()
    db.refresh(where_to_buy)
    return where_to_buy


def get_where_to_buy(db: Session, where_to_buy_id: int) -> Optional[models.WhereToBuy]:
    return db.get(models.WhereToBuy, where_to_buy_id)


def list_where_to_buy(db: Session, skip: int = 0, limit: int = 100, location: Optional[str] = None) -> Sequence[models.WhereToBuy]:
    stmt = select(models.WhereToBuy)
    if location:
        stmt = stmt.where(models.WhereToBuy.location.ilike(f"%{location}%"))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def update_where_to_buy(db: Session, where_to_buy: models.WhereToBuy, where_to_buy_in: schemas.WhereToBuyUpdate) -> models.WhereToBuy:
    for field, value in where_to_buy_in.dict(exclude_unset=True).items():
        setattr(where_to_buy, field, value)
    db.add(where_to_buy)
    db.commit()
    db.refresh(where_to_buy)
    return where_to_buy


def delete_where_to_buy(db: Session, where_to_buy: models.WhereToBuy) -> None:
    db.delete(where_to_buy)
    db.commit()