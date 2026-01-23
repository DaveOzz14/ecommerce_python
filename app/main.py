import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Load environment variables
load_dotenv()

# Configure OpenTelemetry BEFORE app creation
from app.telemetry import configure_telemetry, get_tracer, get_meter

# Initialize telemetry
trace_provider, meter_provider, logger_provider = configure_telemetry()

# Get logger
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Simple Ecommerce")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Import routers
from app.routers import auth, products, checkout

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(checkout.router)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

logger.info("Ecommerce application started with OpenTelemetry instrumentation")

#Prueba
