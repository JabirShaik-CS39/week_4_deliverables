from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    # CREATE
    @staticmethod
    async def create_product(db: AsyncSession, data: ProductCreate):
        product = Product(**data.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    # GET BY ID
    @staticmethod
    async def get_product(db: AsyncSession, product_id: int):
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    # DELETE
    @staticmethod
    async def delete_product(db: AsyncSession, product: Product):
        await db.delete(product)
        await db.commit()

    # UPDATE
    @staticmethod
    async def update_product(db: AsyncSession, product: Product, data: ProductUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product

    # LIST with SEARCH + FILTER + PAGINATION + SORT
    @staticmethod
    async def list_products(
        db: AsyncSession,
        search: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        query = select(Product)

        # SEARCH
        if search:
            query = query.where(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%")
                )
            )

        # FILTER
        if min_price is not None:
            query = query.where(Product.price >= min_price)

        if max_price is not None:
            query = query.where(Product.price <= max_price)

        # SORT
        if sort == "price_asc":
            query = query.order_by(asc(Product.price))
        elif sort == "price_desc":
            query = query.order_by(desc(Product.price))
        else:
            query = query.order_by(desc(Product.created_at))

        # PAGINATION
        total_result = await db.execute(select(func.count()).select_from(Product))
        total = total_result.scalar()

        query = query.offset((page - 1) * limit).limit(limit)

        result = await db.execute(query)
        products = result.scalars().all()

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "items": products
        }