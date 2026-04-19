# Arquivo: app/api/routes/reserva.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.schemas.reserva import ReservaCreate, ReservaResponse
from app.services import reserva_service

# ALERADO AQUI: prefix="/api/reserva" (no singular)
router = APIRouter(prefix="/api/reserva", tags=["Reserva"])

@router.post("/", response_model=ReservaResponse)
def criar(data: ReservaCreate, db: Session = Depends(get_db)):
    return reserva_service.criar_reserva(db, data)

@router.get("/morador/{morador_id}", response_model=List[ReservaResponse])
def listar_do_morador(morador_id: int, db: Session = Depends(get_db)):
    return reserva_service.listar_reservas_por_morador(db, morador_id)