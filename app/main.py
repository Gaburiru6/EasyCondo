from fastapi import FastAPI
from app.api.routes import auth, solicitacao
from app.db.session import engine, Base
from app.models import usuario, morador, sindico, area, reserva

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(solicitacao.router)