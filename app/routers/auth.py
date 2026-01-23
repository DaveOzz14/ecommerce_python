import logging
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

# Sesión simulada en memoria
session = {}

@router.get("/")
def login(request: Request):
    """Display login page."""
    with tracer.start_as_current_span("render_login_page") as span:
        span.set_attribute("http.route", "/")
        span.set_attribute("page.name", "login")
        logger.info("Login page rendered")
        return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def do_login(username: str = Form(...)):
    """Process user login."""
    with tracer.start_as_current_span("user_login") as span:
        try:
            span.set_attribute("user.name", username)
            span.set_attribute("action", "login")
            span.set_attribute("http.route", "/login")
            
            # Simulate login logic
            if not username or len(username.strip()) == 0:
                span.set_status(Status(StatusCode.ERROR, "Empty username"))
                span.record_exception(ValueError("Username cannot be empty"))
                logger.error(f"Login failed: empty username")
                raise ValueError("Username cannot be empty")
            
            session["user"] = username
            logger.info(f"User logged in successfully: {username}")
            span.set_status(Status(StatusCode.OK))
            
            return RedirectResponse("/products", status_code=302)
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            logger.error(f"Login error: {str(e)}")
            raise
