from fastapi import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

from app.schemas.user import UserCreate

from app.repositories.user_repository import (
    UserRepository
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    async def register(
        db: AsyncSession,
        user_data: UserCreate
    ):

        existing_user = (
            await UserRepository.get_by_email(
                db,
                user_data.email
            )
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            )
        )

        return await UserRepository.create(
            db,
            user
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str
    ):

        user = await UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "is_admin": user.is_admin
            }
        )

        return token