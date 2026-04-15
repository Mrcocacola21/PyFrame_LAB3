from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(tags=["products"])

templates = Jinja2Templates(directory="app/templates")

DbSession = Annotated[Session, Depends(get_db)]
ProductCreateForm = Annotated[schemas.ProductCreate, Depends(schemas.ProductCreate.as_form)]
ProductUpdateForm = Annotated[schemas.ProductUpdate, Depends(schemas.ProductUpdate.as_form)]


def get_product_or_404(product_id: int, db: DbSession) -> models.Product:
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.get("/", response_class=HTMLResponse)
def read_products(request: Request, db: DbSession):
    products = crud.get_products(db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"products": products},
    )


@router.get("/products/new", response_class=HTMLResponse)
def create_product_form(request: Request):
    return templates.TemplateResponse(request, "create.html")


@router.post("/products/new")
def create_product(product_in: ProductCreateForm, db: DbSession):
    crud.create_product(db, product_in)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_form(
    request: Request,
    product: models.Product = Depends(get_product_or_404),
):
    return templates.TemplateResponse(
        request,
        "edit.html",
        {"product": product},
    )


@router.post("/products/{product_id}/edit")
def update_product(
    product_in: ProductUpdateForm,
    db: DbSession,
    product: models.Product = Depends(get_product_or_404),
):
    crud.update_product(db, product, product_in)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/products/{product_id}/delete")
def delete_product(
    db: DbSession,
    product: models.Product = Depends(get_product_or_404),
):
    crud.delete_product(db, product)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/api/products", response_model=list[schemas.ProductRead])
def api_list_products(db: DbSession):
    return crud.get_products(db)


@router.get("/api/products/{product_id}", response_model=schemas.ProductRead)
def api_get_product(product: models.Product = Depends(get_product_or_404)):
    return product


@router.post(
    "/api/products",
    response_model=schemas.ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def api_create_product(product_in: schemas.ProductCreate, db: DbSession):
    return crud.create_product(db, product_in)


@router.put("/api/products/{product_id}", response_model=schemas.ProductRead)
def api_update_product(
    product_in: schemas.ProductUpdate,
    db: DbSession,
    product: models.Product = Depends(get_product_or_404),
):
    return crud.update_product(db, product, product_in)


@router.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_product(
    db: DbSession,
    product: models.Product = Depends(get_product_or_404),
):
    crud.delete_product(db, product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
