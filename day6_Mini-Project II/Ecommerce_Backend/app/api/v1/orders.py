from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database.session import get_db
from app.core.security import get_current_user, require_admin

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem

from app.services.cart_service import CartService

router = APIRouter(prefix="/orders", tags=["Orders"])


# =========================
# CREATE ORDER (CART → ORDER)
# =========================
@router.post("/create")
async def create_order(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    cart = await CartService.get_user_cart(
        db,
        user.id
    )

    if not cart or not hasattr(cart, "items") or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = sum(
        item.quantity * item.price_snapshot
        for item in cart.items
    )

    order = Order(
        user_id=user.id,
        total_amount=total,
        status=OrderStatus.PENDING
    )

    db.add(order)
    await db.flush()

    for item in cart.items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price_snapshot
            )
        )

    await db.execute(
        delete(CartItem).where(
            CartItem.cart_id == cart.id
        )
    )

    await db.commit()

    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "total": total
    }

# =========================
# GET USER ORDERS
# =========================
@router.get("/my")
async def my_orders(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Order).where(Order.user_id == user.id)
    )
    return result.scalars().all()


# =========================
# ADMIN: UPDATE ORDER STATUS
# =========================
@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    require_admin(user)

    order = await db.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    await db.commit()

    return {
        "message": "Order status updated",
        "order_id": order_id,
        "status": status
    }