from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

PRODUCTS = {
    1: {"name": "Laptop", "price": 3000},
    2: {"name": "Mouse", "price": 80},
    3: {"name": "Teclado", "price": 150},
}

@router.get("/checkout/{product_id}")
def checkout(request: Request, product_id: int):
    product = PRODUCTS.get(product_id)

    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "product": product
        }
    )
