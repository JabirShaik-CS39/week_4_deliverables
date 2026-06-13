from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem


class OrderService:

    @staticmethod
    async def create_order(db: AsyncSession, user_id: int):

        # 1. Get cart
        result = await db.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalars().first()

        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        # 2. Calculate total
        total = sum(item.quantity * item.price_snapshot for item in cart.items)

        # 3. Create order
        order = Order(
            user_id=user_id,
            total_price=total,
            status="PENDING"
        )
        db.add(order)
        await db.flush()  # get order.id before commit

        # 4. Move cart items → order items
        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_snapshot=item.price_snapshot
            )
            db.add(order_item)

        # 5. Clear cart
        for item in cart.items:
            await db.delete(item)

        await db.commit()

        return order