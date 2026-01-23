import logging
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 3000},
    {"id": 2, "name": "Mouse", "price": 80},
    {"id": 3, "name": "Teclado", "price": 150},
]

@router.get("/products")
def products(request: Request):
    """Display products catalog."""
    with tracer.start_as_current_span("view_product_catalog") as span:
        try:
            span.set_attribute("http.route", "/products")
            span.set_attribute("page.name", "products")
            span.set_attribute("product.count", len(PRODUCTS))
            
            logger.info(f"Product catalog viewed, {len(PRODUCTS)} products available")
            span.set_status(Status(StatusCode.OK))
            
            return templates.TemplateResponse(
                "products.html",
                {
                    "request": request,
                    "products": PRODUCTS
                }
            )
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            logger.error(f"Error displaying products: {str(e)}")
            raise
