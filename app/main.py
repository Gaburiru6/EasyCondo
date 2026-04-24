from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os

from app.api.routes import auth, solicitacao, area, reserva, dashboard
from app.db.session import engine, Base

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(solicitacao.router)
app.include_router(area.router)
app.include_router(reserva.router)
app.include_router(dashboard.router)

from fastapi import Request

@app.get("/")
def home():
    return RedirectResponse(url="/login")

@app.get("/login")
def page_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.get("/register")
def page_register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@app.get("/morador")
def morador_page(request: Request, nome: str = "Usuário"):
    return templates.TemplateResponse(
        request=request,
        name="morador.html",
        context={"nome": nome}
    )

@app.get("/area")
def area_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="area.html",
        context={}
    )