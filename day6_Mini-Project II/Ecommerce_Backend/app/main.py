from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.products import router as product_router
from app.api.v1.cart import router as cart_router
from app.api.v1.orders import router as order_router
from app.api.v1.payment import router as payment_router
from app.api.v1.cache import router as cache_router
from app.api.v1.tasks import router as task_router
from app.api.v1.uploads import router as uploads_router
from fastapi.staticfiles import StaticFiles
from app.api.v1.websocket import router as websocket_router
import os
os.makedirs("uploads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

app = FastAPI(
    title="E-Commerce API"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)
app.include_router(
    product_router
    
)

app.include_router(
    cart_router
    
)
app.include_router(
    order_router
)

app.include_router(
    payment_router
)

app.include_router(
    cache_router
)

app.include_router(
    task_router

)

app.include_router(
    uploads_router
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.mount(
    "/thumbnails",
    StaticFiles(directory="thumbnails"),
    name="thumbnails"
)

app.include_router(
    websocket_router
)

@app.get("/")
async def root():
    return {
        "message": "API Running"
    }