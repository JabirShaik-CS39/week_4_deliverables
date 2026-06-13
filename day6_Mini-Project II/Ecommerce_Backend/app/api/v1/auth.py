from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

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


@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.register(
        db,
        user
    )


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