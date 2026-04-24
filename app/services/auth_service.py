from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario as User
from app.models.status_usuario import StatusUsuario

def register(db: Session, data):
    if not data.nome or not data.email or not data.senha or not data.apartamento:
        raise HTTPException(status_code=400, detail="MISSING_FIELDS")

    if data.senha != data.confirmar_senha:
        raise HTTPException(status_code=400, detail="PASSWORD_MISMATCH")

    if len(data.senha) < 6:
        raise HTTPException(status_code=400, detail="WEAK_PASSWORD")

    user_existente = db.query(User).filter(User.email == data.email).first()

    if user_existente:
        raise HTTPException(status_code=400, detail="EMAIL_EXISTS")

    novo_user = User(
        nome=data.nome,
        email=data.email,
        senha=data.senha,
        apartamento=data.apartamento,
        status=StatusUsuario.pendente
    )

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    return {"msg": "Cadastro enviado para aprovação"}


def login(db: Session, email: str, senha: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="EMAIL_NOT_FOUND")

    # 2. senha incorreta
    if user.senha != senha:
        raise HTTPException(status_code=400, detail="INVALID_PASSWORD")

    # 3. não aprovado
    if user.status != StatusUsuario.aprovado:
        raise HTTPException(status_code=403, detail="USER_NOT_APPROVED")
    
    return {"msg": "Login realizado", "user_id": user.id}