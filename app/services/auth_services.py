from sqlalchemy.orm import Session
from app.models.user import User


def register(db: Session, data):
    user_existente = db.query(User).filter(User.email == data.email).first()

    if user_existente:
        raise Exception("Email já cadastrado")

    novo_user = User(
        nome=data.nome,
        email=data.email,
        senha=data.senha,
        status="PENDENTE" 
    )

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    return {"msg": "Cadastro enviado para aprovação"}


def login(db: Session, email: str, senha: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or user.senha != senha:
        raise Exception("Credenciais inválidas")

    if user.status != "APROVADO":
        raise Exception("Usuário ainda não aprovado")

    return {"msg": "Login realizado", "user_id": user.id}