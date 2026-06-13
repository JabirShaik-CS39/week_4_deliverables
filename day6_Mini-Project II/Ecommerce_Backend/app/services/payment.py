from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderStatus


class PaymentService:

    @staticmethod
    async def process_payment(
        db: AsyncSession,
        order_id: int
    ):
        order = await db.get(Order, order_id)

        if not order:
            raise ValueError("Order not found")

        if order.status != OrderStatus.PENDING:
            raise ValueError(
                f"Order already {order.status}"
            )

        # Payment Gateway Simulation
        order.status = OrderStatus.PAID

        await db.commit()
        await db.refresh(order)

        return order