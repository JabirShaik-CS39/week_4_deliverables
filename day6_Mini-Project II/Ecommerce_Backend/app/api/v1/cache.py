from fastapi import APIRouter
from app.core.redis import redis_client

router = APIRouter(
    prefix="/cache",
    tags=["Cache"]
)


@router.get("/")
async def cache_dashboard():

    keys = await redis_client.keys("*")

    return {
        "keys": keys,
        "count": len(keys)
    }