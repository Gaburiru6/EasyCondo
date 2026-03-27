from typing import Optional
from datetime import date
from usuario import Usuario
from statusUsuario import StatusUsuario

class Morador(Usuario):
    dataAprovacao: Optional[date] = None
    status: StatusUsuario