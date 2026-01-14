from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Sesión simulada en memoria
session = {}

@router.get("/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def do_login(username: str = Form(...)):
    session["user"] = username
    return RedirectResponse("/products", status_code=302)
