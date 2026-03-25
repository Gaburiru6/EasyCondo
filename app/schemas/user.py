from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str
    status: str

    class Config:
        from_attributes = True  # necessário pro SQLAlchemy