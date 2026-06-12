## FastAPI File Upload Basics
# FastAPI provides:

from fastapi import UploadFile, File

# Example:

from fastapi import FastAPI, UploadFile, File
app = FastAPI()
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


## Complete Upload Endpoint 
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...)
):

    if file.content_type not in [
        "image/jpeg",
        "image/png"
    ]:
        raise HTTPException(
            400,
            "Only images allowed"
        )

    content = await file.read()

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            400,
            "File too large"
        )

    filename = f"{uuid.uuid4()}_{file.filename}"

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(path, "wb") as f:
        f.write(content)

    return {
        "filename": filename
    }


## Configure S3
import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id="KEY",
    aws_secret_access_key="SECRET"
)

# Upload File
from assest import file
s3.upload_fileobj(
    file.file,
    "my-bucket",
    file.filename
)

# FastAPI WebSocket Endpoint
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        await websocket.send_text(
            f"You sent: {data}"
        )

## Connection Manager
# Track active users.

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(
        self,
        websocket
    ):
        await websocket.accept()

        self.active_connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket
    ):
        self.active_connections.remove(
            websocket
        )

# Broadcast Message
async def broadcast(
    self,
    message
):
    for connection in self.active_connections:
        await connection.send_text(
            message
        )


# Complete Manager
from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):
        await websocket.accept()

        self.active_connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket
    ):
        self.active_connections.remove(
            websocket
        )

    async def broadcast(
        self,
        message: str
    ):
        for connection in self.active_connections:
            await connection.send_text(
                message
            )

manager = ConnectionManager()

# Product Creation
@app.post("/products")
async def create_product():

    product = {
        "name": "iPhone 18"
    }

    await manager.broadcast(
        "New Product Added"
    )

    return product

## Verify Token
@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str
):
    

# Authenticated Connection

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str
):

    verify_token(token)

    await manager.connect(
        websocket
    )

    try:
        while True:
            await websocket.receive_text()

    except:
        manager.disconnect(
            websocket
        )

# Chat Server
@app.websocket("/chat")
async def chat(
    websocket: WebSocket
):

    await manager.connect(websocket)

    try:

        while True:

            msg = await websocket.receive_text()

            await manager.broadcast(msg)

    except:

        manager.disconnect(
            websocket
        )


    