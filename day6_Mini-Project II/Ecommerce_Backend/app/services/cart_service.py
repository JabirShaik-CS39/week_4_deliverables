from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import Cart, CartItem
from app.models.product import Product


class CartService:

    @staticmethod
    async def get_or_create_cart(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalars().first()

        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)

        return cart

    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        user_id: int,
        product_id: int,
        quantity: int
    ):
        cart = await CartService.get_or_create_cart(db, user_id)

        product = await db.get(Product, product_id)
        if not product:
            raise ValueError("Product not found")

        result = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id
            )
        )
        item = result.scalars().first()

        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                price_snapshot=product.price
            )
            db.add(item)

        await db.commit()
        return cart

    @staticmethod
    async def get_user_cart(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    