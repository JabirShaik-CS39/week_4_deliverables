    # Redis Async Connection
import asyncio
import redis.asyncio as redis

async def main():
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    await redis_client.set("name", "jabir")

    value = await redis_client.get("name")

    print(value)

asyncio.run(main())

# FastAPI Redis Dependency
from fastapi import FastAPI
import redis.asyncio as redis

app = FastAPI()

redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

# 
import redis.asyncio as redis

pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    decode_responses=True,
    max_connections=20
)

redis_client = redis.Redis(
    connection_pool=pool
)

# FastAPI Lifespan Management

from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.redis = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    yield

    await app.state.redis.close()

app = FastAPI(
    lifespan=lifespan
)

# Cache Aside Pattern
#FastAPI Example
@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession
):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(404)

    product.price = data.price

    await db.commit()

    await redis.delete(f"product:{product_id}")

    return {"message": "updated"}

# login endpoint
import uuid

@app.post("/login")
async def login():

    session_id = str(uuid.uuid4())

    await redis.set(
        f"session:{session_id}",
        "10",
        ex=3600
    )

    return {
        "session_id": session_id
    }


## Cache-Aside Pattern
# fastapi
import json
from fastapi import APIRouter

router = APIRouter()

@router.get("/products/{id}")
async def get_product(id: int):

    cache_key = f"product:{id}"

    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    product = await session.get(Product, id)

    result = {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }

    await redis.set(
        cache_key,
        json.dumps(result),
        ex=300
    )

    return result

#Update product
@router.put("/products/{id}")
async def update_product(id: int, data: ProductUpdate):

    product = await session.get(Product, id)

    product.price = data.price

    await session.commit()

    result = {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }

    await redis.set(
        f"product:{id}",
        json.dumps(result),
        ex=300
    )

    return result


## TTL
# Implementation
import json

@router.get("/products")
async def get_products():

    cache_key = "products:list"

    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    products = await session.execute(
        select(Product)
    )

    products = products.scalars().all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price
        }
        for p in products
    ]

    await redis.set(
        cache_key,
        json.dumps(result),
        ex=300
    )

    return result

## Sliding Window
# FastAPI Implementation
import time
from fastapi import HTTPException

LIMIT = 5
WINDOW = 60
async def rate_limit(
    user_id: int,
    redis
):
    key = f"rate:{user_id}"

    now = time.time()

    await redis.zremrangebyscore(
        key,
        0,
        now - WINDOW
    )

    count = await redis.zcard(key)

    if count >= LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    await redis.zadd(
        key,
        {str(now): now}
    )

    await redis.expire(
        key,
        WINDOW
    )