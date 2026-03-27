from pydantic import BaseModel

class Usuario(BaseModel):
    id:float
    nome: str
    email: str
    senha: str