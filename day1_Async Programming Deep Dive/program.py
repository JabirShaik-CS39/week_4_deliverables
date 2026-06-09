# Traditional Synchronous Execution
import time

def task1():
    time.sleep(3)
    print("Task 1 completed")

def task2():
    time.sleep(2)
    print("Task 2 completed")

task1()
task2()

# Asynchronous Execution
import asyncio

async def task1():
    await asyncio.sleep(3)
    print("Task 1 completed")

async def task2():
    await asyncio.sleep(2)
    print("Task 2 completed")

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    await t1
    await t2

asyncio.run(main())

## Main Components
# Event Loop
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(2)
    print("World")

asyncio.run(hello())

# Coroutines
import asyncio

async def work():
    print("Start")

    await asyncio.sleep(3)

    print("End")

asyncio.run(work())

# Tasks
import asyncio

async def worker(name):
    print(f"{name} started")

    await asyncio.sleep(2)

    print(f"{name} finished")

async def main():
    t1 = asyncio.create_task(worker("A"))
    t2 = asyncio.create_task(worker("B"))

    await t1
    await t2

asyncio.run(main())

# Futures
import asyncio

async def main():

    future = asyncio.Future()

    future.set_result("Data Received")

    result = await future

    print(result)

asyncio.run(main())

## GIL 
import threading

def task():
    for i in range(10000000):
        pass

t1 = threading.Thread(target=task)
t2 = threading.Thread(target=task)

t1.start()
t2.start()

t1.join()
t2.join()


## Asyncio.gather()
import asyncio

async def fetch1():
    await asyncio.sleep(2)
    return "API1"

async def fetch2():
    await asyncio.sleep(3)
    return "API2"

async def fetch3():
    await asyncio.sleep(1)
    return "API3"

async def main():
    result = await asyncio.gather(
        fetch1(),
        fetch2(),
        fetch3()
    )

    print(result)

asyncio.run(main())



## Async SQLAlchemy Queries
# Async Engine
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/db"
)


#Async Session
from sqlalchemy.ext.asyncio import async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

#Query Example
from sqlalchemy import select
import User

async def get_users(session):

    result = await session.execute(
        select(User)
    )

    return result.scalars().all()

#Insert Example
async def create_user(session, user):

    session.add(user)

    await session.commit()

    await session.refresh(user)

    return user


## Async HTTP Calls with HTTPX
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

@app.get("/dashboard")
async def dashboard():

    async with httpx.AsyncClient() as client:

        user_task = client.get(
            "http://user-service/user/1"
        )

        order_task = client.get(
            "http://order-service/orders/1"
        )

        payment_task = client.get(
            "http://payment-service/payments/1"
        )

        user, orders, payments = await asyncio.gather(
            user_task,
            order_task,
            payment_task
        )

    return {
        "user": user.json(),
        "orders": orders.json(),
        "payments": payments.json()
    }


## asyncio.sleep
import asyncio

async def task1():
    print("Task1 started")
    await asyncio.sleep(3)
    print("Task1 finished")

async def task2():
    print("Task2 started")
    await asyncio.sleep(2)
    print("Task2 finished")

async def main():
    await asyncio.gather(
        task1(),
        task2()
    )

asyncio.run(main())


## practice: endpoint that fetches data from 3 external APIs in parallel vs sequential 
# Sequential
import requests
import time

start = time.time()

r1 = requests.get("https://httpbin.org/delay/2")
r2 = requests.get("https://httpbin.org/delay/2")
r3 = requests.get("https://httpbin.org/delay/2")

print(time.time() - start)

# Async Implementation
import asyncio
import aiohttp
import time

URL = "https://httpbin.org/delay/2"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main():
    start = time.time()

    async with aiohttp.ClientSession() as session:

        results = await asyncio.gather(
            fetch(session, URL),
            fetch(session, URL),
            fetch(session, URL)
        )

    print(f"Time: {time.time() - start}")


asyncio.run(main())


# FastAPI Endpoint Example
# Sequential Endpoint
from fastapi import FastAPI
import aiohttp
import time

app = FastAPI()

URL = "https://httpbin.org/delay/2"


@app.get("/sequential")
async def sequential():

    start = time.time()

    async with aiohttp.ClientSession() as session:

        async with session.get(URL) as r1:
            await r1.json()

        async with session.get(URL) as r2:
            await r2.json()

        async with session.get(URL) as r3:
            await r3.json()

    return {
        "execution_time": time.time() - start
    }


# Parallel Endpoint
from fastapi import FastAPI
import aiohttp
import asyncio
import time

app = FastAPI()

URL = "https://httpbin.org/delay/2"


async def fetch(session):
    async with session.get(URL) as response:
        return await response.json()


@app.get("/parallel")
async def parallel():

    start = time.time()

    async with aiohttp.ClientSession() as session:

        await asyncio.gather(
            fetch(session),
            fetch(session),
            fetch(session)
        )

    return {
        "execution_time": time.time() - start
    }
