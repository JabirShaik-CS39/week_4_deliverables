from fastapi import APIRouter
from fastapi import Depends

from app.api.deps import (
    get_current_user
)

from app.schemas.user import (
    UserResponse
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/profile",
    response_model=UserResponse
)
async def profile(
    current_user=Depends(
        get_current_user
    )
):
    return current_user