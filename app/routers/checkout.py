import logging
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

PRODUCTS = {
    1: {"name": "Laptop", "price": 3000},
    2: {"name": "Mouse", "price": 80},
    3: {"name": "Teclado", "price": 150},
}

@router.get("/checkout/{product_id}")
def checkout(request: Request, product_id: int):
    """Process checkout for a product."""
    with tracer.start_as_current_span("checkout_product") as span:
        try:
            span.set_attribute("http.route", "/checkout/{product_id}")
            span.set_attribute("product.id", product_id)
            span.set_attribute("action", "checkout")
            
            product = PRODUCTS.get(product_id)
            
            if not product:
                span.set_status(Status(StatusCode.ERROR, "Product not found"))
                error_msg = f"Product {product_id} not found"
                logger.error(error_msg)
                span.record_exception(ValueError(error_msg))
                raise ValueError(error_msg)
            
            span.set_attribute("product.name", product["name"])
            span.set_attribute("product.price", product["price"])
            
            logger.info(f"Checkout initiated for product: {product['name']} (ID: {product_id})")
            span.set_status(Status(StatusCode.OK))
            
            return templates.TemplateResponse(
                "checkout.html",
                {
                    "request": request,
                    "product": product
                }
            )
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            logger.error(f"Checkout error: {str(e)}")
            raise
