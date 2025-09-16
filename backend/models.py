from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float, Boolean, Table, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# ======================
# ВСПОМОГАТЕЛЬНЫЕ ТАБЛИЦЫ
# ======================

# Связь многие-ко-многим между заказами и модулями
order_modules = Table(
    "order_modules",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("module_id", ForeignKey("modules.id"), primary_key=True),
)

# Связь многие-ко-многим между корзиной и модулями
cart_modules = Table(
    "cart_modules",
    Base.metadata,
    Column("cart_id", ForeignKey("carts.id"), primary_key=True),
    Column("module_id", ForeignKey("modules.id"), primary_key=True),
)

# Связь многие-ко-многим между модулями и цветами
module_colors = Table(
    "module_colors",
    Base.metadata,
    Column("module_id", ForeignKey("modules.id"), primary_key=True),
    Column("color_id", ForeignKey("colors.id"), primary_key=True),
)

# Связь многие-ко-многим между мебелью и цветами
furniture_colors = Table(
    "furniture_colors",
    Base.metadata,
    Column("furniture_id", ForeignKey("furniture.id"), primary_key=True),
    Column("color_id", ForeignKey("colors.id"), primary_key=True),
)

# ======================
# ОСНОВНЫЕ СУЩНОСТИ
# ======================

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)  # ФИО
    login = Column(String, unique=True, nullable=False)  # логин
    email = Column(String, unique=True, nullable=False)  # почта
    phone_number = Column(String, nullable=False)  # номер телефона
    hashed_password = Column(String, nullable=False)  # пароль
    access_level = Column(Integer, nullable=False, default=1)  # уровень доступа

    # связи
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    support_requests = relationship("SupportRequest", back_populates="user")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Информация о получателе
    full_name = Column(String, nullable=False)  # ФИО получателя
    email = Column(String, nullable=False)  # почта получателя
    delivery_address = Column(String, nullable=False)  # адрес доставки
    city = Column(String, nullable=False)  # город
    street = Column(String, nullable=False)  # улица
    house = Column(String, nullable=False)  # дом
    building = Column(String, nullable=True)  # корпус (опционально)
    floor = Column(String, nullable=True)  # этаж (опционально)
    entrance_code = Column(String, nullable=True)  # код подъезда (опционально)
    
    # Информация о заказе
    payment_method = Column(String, nullable=False)  # метод оплаты
    recipient = Column(String, nullable=False)  # получатель
    date = Column(DateTime, default=datetime.utcnow)  # дата заказа
    total_amount = Column(Float, nullable=False)  # итоговая сумма
    status = Column(String, default="pending")  # статус заказа
    
    # связи
    user = relationship("User", back_populates="orders")
    modules = relationship("Module", secondary=order_modules, back_populates="orders")


class Cart(Base, TimestampMixin):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="active")  # статус корзины
    total_amount = Column(Float, default=0)  # итоговая сумма

    # связи
    user = relationship("User", back_populates="cart")
    modules = relationship("Module", secondary=cart_modules, back_populates="carts")


class Module(Base, TimestampMixin):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # название
    article = Column(String, unique=True, nullable=False)  # артикул
    price = Column(Float, nullable=False)  # цена
    discounted_price = Column(Float, nullable=True)  # цена со скидкой
    technical_details = Column(Text, nullable=True)  # технические детали
    assembly_instruction = Column(Text, nullable=True)  # инструкция сборки
    photos = Column(JSON, nullable=True)  # массив фото

    # связи
    orders = relationship("Order", secondary=order_modules, back_populates="modules")
    carts = relationship("Cart", secondary=cart_modules, back_populates="modules")
    colors = relationship("Color", secondary=module_colors, back_populates="modules")


class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # название цвета
    hex_code = Column(String, nullable=True)  # HEX код цвета
    additional_price = Column(Float, default=0)  # дополнительная цена за цвет
    photos = Column(JSON, nullable=True)  # массив фото цветов

    # связи
    modules = relationship("Module", secondary=module_colors, back_populates="colors")
    furniture = relationship("Furniture", secondary=furniture_colors, back_populates="colors")


class Furniture(Base, TimestampMixin):
    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True, index=True)
    furniture_type = Column(String, nullable=False)  # тип мебели
    name = Column(String, nullable=False)  # название
    price = Column(Float, nullable=False)  # цена
    discounted_price = Column(Float, nullable=True)  # цена со скидкой
    photos = Column(JSON, nullable=True)  # фото
    technical_characteristics = Column(Text, nullable=True)  # технические характеристики
    model = Column(String, nullable=True)  # модель
    article = Column(String, unique=True, nullable=False)  # артикул

    # связи
    colors = relationship("Color", secondary=furniture_colors, back_populates="furniture")


class News(Base, TimestampMixin):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # заголовок
    main_photo = Column(String, nullable=True)  # главное фото
    text1 = Column(Text, nullable=True)  # первый текст
    text2 = Column(Text, nullable=True)  # второй текст
    photos = Column(JSON, nullable=True)  # массив фоток


class SupportRequest(Base, TimestampMixin):
    __tablename__ = "support_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # может быть анонимным
    contact_info = Column(Text, nullable=False)  # контактная информация пользователя
    status = Column(String, default="new")  # статус запроса (new, in_progress, resolved)
    operator_response = Column(Text, nullable=True)  # ответ оператора
    operator_status = Column(String, nullable=True)  # статус оператора

    # связи
    user = relationship("User", back_populates="support_requests")


class Shop(Base, TimestampMixin):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # название магазина
    country = Column(String, nullable=False)  # страна
    city = Column(String, nullable=False)  # город
    address = Column(String, nullable=False)  # адрес


class WhereToBuy(Base, TimestampMixin):
    __tablename__ = "where_to_buy"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)  # локация
    name = Column(String, nullable=False)  # название
    address = Column(String, nullable=False)  # адрес
    phone = Column(String, nullable=False)  # телефон