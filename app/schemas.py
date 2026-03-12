from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    category: str

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(...)],
        price: Annotated[float, Form(...)],
        quantity: Annotated[int, Form(...)],
        category: Annotated[str, Form(...)],
    ):
        return cls(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
        )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


Product = ProductRead
