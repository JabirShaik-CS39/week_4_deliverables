from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from app.tasks.email_tasks import send_welcome_email
from app.database.session import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.schemas.auth import (
    LoginRequest,
    Token
)

from app.services.auth_service import (
    AuthService
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    new_user = await UserService.create_user(
        db,
        user
    )

    background_tasks.add_task(
        send_welcome_email,
        new_user.email
    )

    return {
        "message": "User registered",
        "email": new_user.email
    }


@router.post(
    "/login",
    response_model=Token
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    token = await AuthService.login(
        db,
        data.email,
        data.password
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }