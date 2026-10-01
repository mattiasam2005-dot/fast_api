from typing import Annotated
from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field


app = FastAPI(
    title="Products API",
    description="Progetto didattico per replicare i concetti fondamentali di FastAPI.",
    version="1.0.0",
)


class Category(str, Enum):
    computer = "computer"
    smartphone = "smartphone"
    tablet = "tablet"


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: str | None = None
    category: Category


products = [
    {
        "id": 1,
        "name": "Laptop Pro",
        "price": 1299.99,
        "description": "Computer portatile professionale",
        "category": Category.computer,
    },
    {
        "id": 2,
        "name": "Smartphone X",
        "price": 799.99,
        "description": "Smartphone di ultima generazione",
        "category": Category.smartphone,
    },
    {
        "id": 3,
        "name": "Tablet Air",
        "price": 599.99,
        "description": "Tablet leggero e versatile",
        "category": Category.tablet,
    },
]


@app.get("/")
async def root():
    return {"message": "Benvenuto nella Products API"}


@app.get("/products")
async def get_products(
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    result = products

    if q:
        result = [
            product
            for product in result
            if q.lower() in product["name"].lower()
        ]

    return {
        "count": len(result[:limit]),
        "products": result[:limit],
    }


@app.get("/products/category/{category}")
async def get_products_by_category(category: Category):
    result = [
        product
        for product in products
        if product["category"] == category
    ]

    return {
        "category": category,
        "count": len(result),
        "products": result,
    }


@app.get("/products/{product_id}")
async def get_product(
    product_id: Annotated[int, Path(ge=1)],
):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Prodotto non trovato",
    )


@app.post("/products", status_code=201)
async def create_product(product: Product):
    new_id = max(item["id"] for item in products) + 1

    new_product = {
        "id": new_id,
        **product.model_dump(),
    }

    products.append(new_product)

    return new_product
