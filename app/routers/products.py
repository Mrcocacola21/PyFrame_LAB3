from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products},
    )


@router.get("/products/new", response_class=HTMLResponse)
def create_product_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.post("/products/new")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db),
):
    product_in = schemas.ProductCreate(
        name=name,
        price=price,
        quantity=quantity,
        category=category,
    )
    crud.create_product(db, product_in)
    return RedirectResponse(url="/", status_code=303)


@router.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_form(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "product": product},
    )


@router.post("/products/{product_id}/edit")
def update_product(
    product_id: int,
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in = schemas.ProductUpdate(
        name=name,
        price=price,
        quantity=quantity,
        category=category,
    )
    crud.update_product(db, product, product_in)
    return RedirectResponse(url="/", status_code=303)


@router.post("/products/{product_id}/delete")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, product)
    return RedirectResponse(url="/", status_code=303)
