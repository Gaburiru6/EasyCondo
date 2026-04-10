from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario as User
from app.models.status_usuario import StatusUsuario

def register(db: Session, data):
    user_existente = db.query(User).filter(User.email == data.email).first()

    if user_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_user = User(
        nome=data.nome,
        email=data.email,
        senha=data.senha,
        status=StatusUsuario.pendente 
    )

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    return {"msg": "Cadastro enviado para aprovação"}


def login(db: Session, email: str, senha: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or user.senha != senha:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    if user.status != StatusUsuario.aprovado:
        raise HTTPException(status_code=403, detail="Usuário não aprovado")

    return {"msg": "Login realizado", "user_id": user.id}