from enum import Enum

class StatusReserva(str, Enum):
    confirmada = 'confirmada'
    pendentePagamento = 'pendentePagamento'
    cancelada = 'cancelada'