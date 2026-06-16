from app.core.redis import redis_client
import asyncio

async def test():

    await redis_client.set(
        "name",
        "jabir"
    )

    value = await redis_client.get("name")

    print(value)

asyncio.run(test())