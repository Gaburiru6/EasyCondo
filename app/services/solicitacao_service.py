from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.status_usuario import StatusUsuario
from app.models.usuario import Usuario as User


def listar(db: Session):
    return db.query(User).filter(User.status == StatusUsuario.pendente).all()


def aprovar(db: Session, id: int):
    user = db.get(User, id)

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if user.status != StatusUsuario.pendente:
        raise HTTPException(400, "Usuário já processado")

    user.status = StatusUsuario.aprovado
    db.commit()

    return {"msg": "Usuário aprovado"}


def negar(db: Session, id: int):
    user = db.get(User, id)

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if user.status != StatusUsuario.pendente:
        raise HTTPException(400, "Usuário já processado")

    user.status = StatusUsuario.negado
    db.commit()

    return {"msg": "Usuário negado"}