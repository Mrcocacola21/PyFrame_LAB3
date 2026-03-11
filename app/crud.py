from sqlalchemy.orm import Session

from . import models, schemas


def get_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, db_product: models.Product, product: schemas.ProductUpdate):
    for field, value in product.model_dump().items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, db_product: models.Product):
    db.delete(db_product)
    db.commit()
