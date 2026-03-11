from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    category: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
