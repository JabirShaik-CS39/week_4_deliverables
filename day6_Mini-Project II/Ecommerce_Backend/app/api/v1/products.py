from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.core.websocket_manager import manager

router = APIRouter(prefix="/products", tags=["Products"])


# CREATE
@router.post("", response_model=ProductResponse)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    product = await ProductService.create_product(
        db,
        data
    )

    await manager.broadcast({
        "event": "new_product",
        "product_id": product.id,
        "name": product.name
    })

    return product
    

# LIST (SEARCH + FILTER + PAGINATION + SORT)
@router.get("")
async def list_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await ProductService.list_products(
        db, search, min_price, max_price, sort, page, limit
    )


# GET BY ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    product = await ProductService.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return await ProductService.update_product(db, product, data)


# DELETE
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await ProductService.delete_product(db, product)

    return {"message": "Product deleted successfully"}