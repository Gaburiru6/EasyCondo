from sqlalchemy.orm import Session
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate

def criar_reserva(db: Session, reserva_data: ReservaCreate):
    nova_reserva = Reserva(**reserva_data.model_dump())
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva

def listar_reservas_por_morador(db: Session, morador_id: int):
    # Retorna todas as reservas de um morador específico
    return db.query(Reserva).filter(Reserva.morador_id == morador_id).all()