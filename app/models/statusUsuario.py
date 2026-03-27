from enum import Enum

class StatusUsuario(str, Enum):
    pendente = 'pendente'
    aprovado = 'aprovado'
    negado = 'negado'