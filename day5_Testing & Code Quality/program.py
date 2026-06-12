## Example Async Test
# Function:
async def add(a, b):
    return a + b
# Test:

import pytest
@pytest.mark.asyncio
async def test_add():
    result = await add(2, 3)

    assert result == 5

## Example API
@app.get("/hello")
async def hello():
    return {"message": "Hello"}
# Test
from httpx import AsyncClient

async def test_hello(app):

    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:

        response = await client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello"
    }

## Example Fixture
import pytest

@pytest.fixture
def sample_user():

    return {
        "name": "Jabir",
        "email": "jabir@test.com"
    }

## FastAPI App Fixture
@pytest.fixture
def app():

    from app.main import app

    return app


## Client Fixture
from httpx import AsyncClient

@pytest.fixture
async def client(app):

    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:

        yield client

## Create User Test
async def test_create_user(client):

    response = await client.post(
        "/users",
        json={
            "name":"Jabir",
            "email":"jabir@test.com"
        }
    )

    assert response.status_code == 201
# Get Users
async def test_get_users(client):

    response = await client.get("/users")

    assert response.status_code == 200
# Update User
async def test_update_user(client):

    response = await client.put(
        "/users/1",
        json={"name":"Updated"}
    )

    assert response.status_code == 200
# Delete User
async def test_delete_user(client):

    response = await client.delete(
        "/users/1"
    )

    assert response.status_code == 204

## Testing Authentication Flow
# Register Test
async def test_register(client):

    response = await client.post(
        "/auth/register",
        json={
            "email":"test@test.com",
            "password":"123456"
        }
    )

    assert response.status_code == 201

# Login Test
async def test_login(client):

    response = await client.post(
        "/auth/login",
        json={
            "email":"test@test.com",
            "password":"123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
