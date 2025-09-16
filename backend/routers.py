from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from . import crud, schemas, models


router = APIRouter()


# ======================
# Users
# ======================
@router.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["users"], summary="Создать пользователя")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user_in)


@router.get("/users", response_model=List[schemas.User], tags=["users"], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=schemas.User, tags=["users"], summary="Получить пользователя по ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=schemas.User, tags=["users"], summary="Обновить пользователя")
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user, user_in)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"], summary="Удалить пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
    return None


# ======================
# Legacy Items (kept)
# ======================
@router.post("/users/{user_id}/items", response_model=schemas.Item, status_code=status.HTTP_201_CREATED, tags=["items"], summary="Создать item для пользователя")
def create_item_for_user(user_id: int, item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_item(db, owner_id=user_id, item_in=item_in)


@router.get("/items", response_model=List[schemas.Item], tags=["items"], summary="Список items")
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_items(db, skip=skip, limit=limit)


@router.get("/items/{item_id}", response_model=schemas.Item, tags=["items"], summary="Получить item")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/items/{item_id}", response_model=schemas.Item, tags=["items"], summary="Обновить item")
def update_item(item_id: int, item_in: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db, item, item_in)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"], summary="Удалить item")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return None


# ======================
# Blogs
# ======================
@router.post("/blogs", response_model=schemas.Blog, status_code=status.HTTP_201_CREATED, tags=["blogs"], summary="Создать блог")
def create_blog(blog_in: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog_in)


@router.get("/blogs", response_model=List[schemas.Blog], tags=["blogs"], summary="Список блогов")
def list_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_blogs(db, skip=skip, limit=limit)


@router.get("/blogs/{blog_id}", response_model=schemas.Blog, tags=["blogs"], summary="Получить блог")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.patch("/blogs/{blog_id}", response_model=schemas.Blog, tags=["blogs"], summary="Обновить блог")
def update_blog(blog_id: int, blog_in: schemas.BlogUpdate, db: Session = Depends(get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return crud.update_blog(db, blog, blog_in)


@router.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"], summary="Удалить блог")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    crud.delete_blog(db, blog)
    return None


# ======================
# Products
# ======================
@router.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED, tags=["products"], summary="Создать продукт")
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product_in)


@router.get("/products", response_model=List[schemas.Product], tags=["products"], summary="Список продуктов с фильтрами")
def list_products(name: str | None = None, company: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_products(db, skip=skip, limit=limit, name=name, company=company)


@router.get("/products/{product_id}", response_model=schemas.Product, tags=["products"], summary="Получить продукт")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/products/{product_id}", response_model=schemas.Product, tags=["products"], summary="Обновить продукт")
def update_product(product_id: int, product_in: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db, product, product_in)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["products"], summary="Удалить продукт")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, product)
    return None


# Product Prices
@router.post(
    "/products/{product_id}/prices",
    response_model=schemas.PriceHistory,
    status_code=status.HTTP_201_CREATED,
    tags=["products"],
    summary="Добавить запись цены для продукта",
)
def add_product_price(product_id: int, price_in: schemas.PriceHistoryCreate, db: Session = Depends(get_db)):
    if price_in.product_id != product_id:
        raise HTTPException(status_code=400, detail="product_id mismatch")
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.add_price_entry(db, price_in)


@router.get(
    "/products/{product_id}/prices",
    response_model=List[schemas.PriceHistory],
    tags=["products"],
    summary="Список цен продукта с фильтром по магазину (company)",
)
def list_product_prices(product_id: int, company: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.list_product_prices(db, product_id=product_id, company=company, skip=skip, limit=limit)


# ======================
# Cart
# ======================
@router.post(
    "/users/{user_id}/cart/items",
    response_model=schemas.CartItem,
    status_code=status.HTTP_201_CREATED,
    tags=["cart"],
    summary="Добавить товар в корзину пользователя",
)
def add_item_to_cart(user_id: int, item_in: schemas.CartItemCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.add_item_to_cart(db, user_id=user_id, item_in=item_in)


@router.get(
    "/users/{user_id}/cart/items",
    response_model=List[schemas.CartItem],
    tags=["cart"],
    summary="Получить товары в корзине пользователя",
)
def get_cart_items(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.list_cart_items(db, user_id=user_id)


@router.patch(
    "/users/{user_id}/cart/items/{cart_item_id}",
    response_model=schemas.CartItem,
    tags=["cart"],
    summary="Обновить позицию в корзине",
)
def update_cart_item(user_id: int, cart_item_id: int, item_in: schemas.CartItemUpdate, db: Session = Depends(get_db)):
    cart_items = crud.list_cart_items(db, user_id=user_id)
    target = next((ci for ci in cart_items if ci.id == cart_item_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return crud.update_cart_item(db, target, item_in)


@router.delete(
    "/users/{user_id}/cart/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["cart"],
    summary="Удалить позицию из корзины",
)
def delete_cart_item(user_id: int, cart_item_id: int, db: Session = Depends(get_db)):
    cart_items = crud.list_cart_items(db, user_id=user_id)
    target = next((ci for ci in cart_items if ci.id == cart_item_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Cart item not found")
    crud.remove_cart_item(db, target)
    return None


# ======================
# Orders
# ======================
@router.post("/orders", response_model=schemas.Order, status_code=status.HTTP_201_CREATED, tags=["orders"], summary="Создать заказ")
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, order_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_order(db, order_in)


@router.get("/orders", response_model=List[schemas.Order], tags=["orders"], summary="Список заказов (фильтр по user_id)")
def list_orders(user_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_orders(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=schemas.Order, tags=["orders"], summary="Получить заказ")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/orders/{order_id}", response_model=schemas.Order, tags=["orders"], summary="Обновить заказ")
def update_order(order_id: int, order_in: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.update_order(db, order, order_in)


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["orders"], summary="Удалить заказ")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.delete_order(db, order)
    return None





