from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 3000},
    {"id": 2, "name": "Mouse", "price": 80},
    {"id": 3, "name": "Teclado", "price": 150},
]

@router.get("/products")
def products(request: Request):
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": PRODUCTS
        }
    )
