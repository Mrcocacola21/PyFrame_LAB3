from fastapi import FastAPI

from .database import engine
from .routers import products
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Products Lab")

app.include_router(products.router)
