from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.order import Order, OrderStatus
from app.core.security import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/pay/{order_id}")
async def pay_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    order = await db.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = OrderStatus.PAID
    await db.commit()

    return {"message": "Payment successful", "order_id": order_id}