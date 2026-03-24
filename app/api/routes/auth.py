from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.solicitacao import SolicitacaoCreate
from app.services import auth_service
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: SolicitacaoCreate, db: Session = Depends(get_db)):
    return auth_service.criar_solicitacao(db, data)


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    return auth_service.login(db, email, senha)