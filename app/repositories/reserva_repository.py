from sqlalchemy.orm import Session

from app.models.reserva import Reserva
from app.models.status_reserva import StatusReserva
from app.models.area import Area
from app.models.usuario import Usuario


def criar(
    db: Session,
    reserva: Reserva
):

    db.add(reserva)
    db.commit()
    db.refresh(reserva)

    return reserva


def listar_por_morador(
    db: Session,
    morador_id: int
):
    return (
        db.query(Reserva)
        .filter(Reserva.morador_id == morador_id)
        .all()
    )


def buscar_por_id(
    db: Session,
    reserva_id: int
):
    return (
        db.query(Reserva)
        .filter(Reserva.id == reserva_id)
        .first()
    )


def listar_conflitantes_por_area_data(
    db: Session,
    area_id: int,
    data_reserva,
    reserva_id: int | None = None
):
    query = (
        db.query(Reserva)
        .filter(Reserva.area_id == area_id)
        .filter(Reserva.data_reserva == data_reserva)
        .filter(Reserva.status != StatusReserva.cancelada)
    )

    if reserva_id is not None:
        query = query.filter(Reserva.id != reserva_id)

    return query.all()


def listar_todas_ativas(
    db: Session
):
    return (
        db.query(Reserva)
        .filter(Reserva.status != StatusReserva.cancelada)
        .order_by(Reserva.data_reserva.asc(), Reserva.horario_inicio.asc())
        .all()
    )


def listar_todas_ativas_com_nomes(
    db: Session
):
    registros = (
        db.query(Reserva, Area.nome.label("area_nome"), Usuario.nome.label("morador_nome"))
        .join(Area, Area.id == Reserva.area_id)
        .join(Usuario, Usuario.id == Reserva.morador_id)
        .filter(Reserva.status != StatusReserva.cancelada)
        .order_by(Reserva.data_reserva.asc(), Reserva.horario_inicio.asc())
        .all()
    )

    return [
        {
            "id": reserva.id,
            "area_id": reserva.area_id,
            "morador_id": reserva.morador_id,
            "data_reserva": reserva.data_reserva,
            "horario_inicio": reserva.horario_inicio,
            "horario_fim": reserva.horario_fim,
            "valor_pago": reserva.valor_pago,
            "status": reserva.status,
            "area_nome": area_nome,
            "morador_nome": morador_nome
        }
        for reserva, area_nome, morador_nome in registros
    ]


def salvar(
    db: Session,
    reserva: Reserva
):

    db.commit()
    db.refresh(reserva)

    return reserva