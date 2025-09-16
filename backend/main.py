from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from .api.routers.users import router as users_router
from .api.routers.orders import router as orders_router
from .api.routers.cart import router as cart_router
from .api.routers.auth import router as auth_router
from .api.routers.modules import router as modules_router
from .api.routers.furniture import router as furniture_router
from .api.routers.colors import router as colors_router
from .api.routers.news import router as news_router
from .api.routers.support import router as support_router
from .api.routers.shops import router as shops_router
from .api.routers.where_to_buy import router as where_to_buy_router
from .database import init_db
import os

app = FastAPI()

# Создание таблиц при запуске
@app.on_event("startup")
def on_startup():
    init_db()

# Static uploads
uploads_path = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

# Подключение роутеров по доменам
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(modules_router, prefix="/api")
app.include_router(furniture_router, prefix="/api")
app.include_router(colors_router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(support_router, prefix="/api")
app.include_router(shops_router, prefix="/api")
app.include_router(where_to_buy_router, prefix="/api")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Behoof API",
        version="1.0.0",
        description="Backend API",
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi