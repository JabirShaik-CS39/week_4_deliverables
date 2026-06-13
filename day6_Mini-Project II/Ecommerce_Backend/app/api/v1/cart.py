from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.security import get_current_user
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add")
async def add_to_cart(
    product_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await CartService.add_to_cart(
        db, user.id, product_id, quantity
    )

from sqlalchemy import select
from app.models.cart import Cart

@router.get("/")
async def view_cart(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(Cart.user_id == user.id)
    )
    cart = result.scalars().first()

    return cart

from app.models.cart import CartItem

@router.delete("/item/{item_id}")
async def remove_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    item = await db.get(CartItem, item_id)

    if not item:
        return {"message": "Item not found"}

    await db.delete(item)
    await db.commit()

    return {"message": "Item removed"}

@router.get("/total")
async def cart_total(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(Cart.user_id == user.id)
    )
    cart = result.scalars().first()

    if not cart:
        return {"total": 0}

    total = sum(item.quantity * item.price_snapshot for item in cart.items)

    return {"total": total}

