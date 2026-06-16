from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from PIL import Image
import uuid
import os

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...)
):
    # =========================
    # VALIDATE FILE TYPE
    # =========================
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid image type"
        )

    # =========================
    # VALIDATE FILE SIZE
    # =========================
    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    await file.seek(0)

    # =========================
    # GENERATE UNIQUE NAME
    # =========================
    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = f"uploads/{filename}"

    # =========================
    # SAVE ORIGINAL FILE
    # =========================
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # =========================
    # RESIZE IMAGE
    # =========================
    image = Image.open(filepath)

    image.thumbnail((1200, 1200))

    image.save(
        filepath,
        optimize=True,
        quality=85
    )

    # =========================
    # CREATE THUMBNAIL
    # =========================
    thumbnail_path = f"thumbnails/{filename}"

    thumb = Image.open(filepath)

    thumb.thumbnail((300, 300))

    thumb.save(
        thumbnail_path,
        optimize=True,
        quality=80
    )

    return {
        "message": "File uploaded successfully",
        "filename": filename,
        "image_url": f"/uploads/{filename}",
        "thumbnail_url": f"/thumbnails/{filename}"
    }