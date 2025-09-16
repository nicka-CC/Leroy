from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# ========== USER ==========
class UserBase(BaseModel):
    full_name: str
    login: str
    email: EmailStr
    phone_number: str
    access_level: int = 1


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    access_level: Optional[int] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== COLOR ==========
class ColorBase(BaseModel):
    name: str
    hex_code: Optional[str] = None
    additional_price: float = 0
    photos: Optional[List[str]] = None


class ColorCreate(ColorBase):
    pass


class ColorUpdate(BaseModel):
    name: Optional[str] = None
    hex_code: Optional[str] = None
    additional_price: Optional[float] = None
    photos: Optional[List[str]] = None


class Color(ColorBase):
    id: int

    class Config:
        from_attributes = True


# ========== MODULE ==========
class ModuleBase(BaseModel):
    name: str
    article: str
    price: float
    discounted_price: Optional[float] = None
    technical_details: Optional[str] = None
    assembly_instruction: Optional[str] = None
    photos: Optional[List[str]] = None


class ModuleCreate(ModuleBase):
    color_ids: Optional[List[int]] = []


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    article: Optional[str] = None
    price: Optional[float] = None
    discounted_price: Optional[float] = None
    technical_details: Optional[str] = None
    assembly_instruction: Optional[str] = None
    photos: Optional[List[str]] = None
    color_ids: Optional[List[int]] = None


class Module(ModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    colors: List[Color] = []

    class Config:
        from_attributes = True


# ========== FURNITURE ==========
class FurnitureBase(BaseModel):
    furniture_type: str
    name: str
    price: float
    discounted_price: Optional[float] = None
    photos: Optional[List[str]] = None
    technical_characteristics: Optional[str] = None
    model: Optional[str] = None
    article: str


class FurnitureCreate(FurnitureBase):
    color_ids: Optional[List[int]] = []


class FurnitureUpdate(BaseModel):
    furniture_type: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    discounted_price: Optional[float] = None
    photos: Optional[List[str]] = None
    technical_characteristics: Optional[str] = None
    model: Optional[str] = None
    article: Optional[str] = None
    color_ids: Optional[List[int]] = None


class Furniture(FurnitureBase):
    id: int
    created_at: datetime
    updated_at: datetime
    colors: List[Color] = []

    class Config:
        from_attributes = True


# ========== CART ==========
class CartBase(BaseModel):
    status: str = "active"
    total_amount: float = 0


class CartCreate(CartBase):
    module_ids: Optional[List[int]] = []


class CartUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
    module_ids: Optional[List[int]] = None


class Cart(CartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    modules: List[Module] = []

    class Config:
        from_attributes = True


# ========== ORDER ==========
class OrderBase(BaseModel):
    full_name: str
    email: EmailStr
    delivery_address: str
    city: str
    street: str
    house: str
    building: Optional[str] = None
    floor: Optional[str] = None
    entrance_code: Optional[str] = None
    payment_method: str
    recipient: str
    total_amount: float
    status: str = "pending"


class OrderCreate(OrderBase):
    module_ids: Optional[List[int]] = []


class OrderUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    delivery_address: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    entrance_code: Optional[str] = None
    payment_method: Optional[str] = None
    recipient: Optional[str] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    module_ids: Optional[List[int]] = None


class Order(OrderBase):
    id: int
    user_id: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    modules: List[Module] = []

    class Config:
        from_attributes = True


# ========== NEWS ==========
class NewsBase(BaseModel):
    title: str
    main_photo: Optional[str] = None
    text1: Optional[str] = None
    text2: Optional[str] = None
    photos: Optional[List[str]] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    main_photo: Optional[str] = None
    text1: Optional[str] = None
    text2: Optional[str] = None
    photos: Optional[List[str]] = None


class News(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== SUPPORT REQUEST ==========
class SupportRequestBase(BaseModel):
    contact_info: str
    status: str = "new"
    operator_response: Optional[str] = None
    operator_status: Optional[str] = None


class SupportRequestCreate(SupportRequestBase):
    pass


class SupportRequestUpdate(BaseModel):
    contact_info: Optional[str] = None
    status: Optional[str] = None
    operator_response: Optional[str] = None
    operator_status: Optional[str] = None


class SupportRequest(SupportRequestBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== SHOP ==========
class ShopBase(BaseModel):
    name: str
    country: str
    city: str
    address: str


class ShopCreate(ShopBase):
    pass


class ShopUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None


class Shop(ShopBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== WHERE TO BUY ==========
class WhereToBuyBase(BaseModel):
    location: str
    name: str
    address: str
    phone: str


class WhereToBuyCreate(WhereToBuyBase):
    pass


class WhereToBuyUpdate(BaseModel):
    location: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class WhereToBuy(WhereToBuyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== RESPONSE SCHEMAS ==========
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None