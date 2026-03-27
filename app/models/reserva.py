from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from statusReserva import StatusReserva

class Reserva(BaseModel):
    id: int
    area: str
    morador: str
    dataReserva: date
    dataCancelamento: Optional[date] = None
    horarioInicio: time
    horarioFim: time
    status: StatusReserva
    valorPago: float