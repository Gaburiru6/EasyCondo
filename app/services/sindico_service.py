from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sindico import Sindico
from app.models.usuario import Usuario
from app.repositories import sindico_repository


def listar_moradores(
    db: Session,
    nome: str | None = None,
    ordenar_por: str = "nome",
    ordem: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    ordenar_por_normalizado = (ordenar_por or "nome").lower()
    ordem_normalizada = (ordem or "asc").lower()

    if ordenar_por_normalizado not in {"nome", "cadastro"}:
        raise HTTPException(status_code=400, detail="Parâmetro 'ordenar_por' inválido.")

    if ordem_normalizada not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Parâmetro 'ordem' inválido.")

    page = max(1, int(page or 1))
    page_size = min(100, max(1, int(page_size or 10)))

    return sindico_repository.listar_moradores(
        db,
        nome=nome,
        ordenar_por=ordenar_por_normalizado,
        ordem=ordem_normalizada,
        page=page,
        page_size=page_size
    )


def buscar_sindico_por_id(
    db: Session,
    user_id: int
):
    return sindico_repository.buscar_sindico_por_id(db, user_id)


def promover(
    db: Session,
    user_id: int
):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    sindico = sindico_repository.promover(db, user_id)
    return {
        "msg": "Usuário promovido a síndico.",
        "id": sindico.id
    }


def rebaixar(
    db: Session,
    user_id: int
):
    sindico = buscar_sindico_por_id(db, user_id)
    if not sindico:
        raise HTTPException(status_code=404, detail="Síndico não encontrado.")

    if total_sindicos(db) <= 1:
        raise HTTPException(status_code=400, detail="Não é possível rebaixar o último síndico.")

    sindico_repository.rebaixar(db, sindico)
    return {"msg": "Síndico rebaixado para morador."}


def total_sindicos(db: Session):
    return sindico_repository.total_sindicos(db)