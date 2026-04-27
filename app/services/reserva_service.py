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

def atualizar_reserva(db: Session, reserva_id: int, reserva_data: ReservaCreate):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        # Atualiza apenas os campos que o morador pode editar
        reserva.area_id = reserva_data.area_id
        reserva.data_reserva = reserva_data.data_reserva
        reserva.horario_inicio = reserva_data.horario_inicio
        reserva.horario_fim = reserva_data.horario_fim
        db.commit()
        db.refresh(reserva)
    return reserva