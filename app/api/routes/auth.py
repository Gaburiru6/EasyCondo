from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.solicitacao import SolicitacaoCreate
from app.services.auth_service import register, login
from app.api.deps import get_db
from app.schemas.login import LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: SolicitacaoCreate, db: Session = Depends(get_db)):
    return register(db, data)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login(db, data.email, data.senha)