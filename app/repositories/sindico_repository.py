from sqlalchemy.orm import Session

from app.models.sindico import Sindico
from app.models.usuario import Usuario


def listar_moradores(
    db: Session,
    nome: str | None = None,
    ordenar_por: str = "nome",
    ordem: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    query = (
        db.query(Usuario, Sindico.id.label("sindico_id"))
        .outerjoin(Sindico, Sindico.id == Usuario.id)
    )

    if nome:
        query = query.filter(Usuario.nome.ilike(f"%{nome}%"))

    coluna_ordenacao = Usuario.nome if ordenar_por == "nome" else Usuario.id
    query = query.order_by(coluna_ordenacao.desc() if ordem == "desc" else coluna_ordenacao.asc())

    total = query.count()
    offset = (page - 1) * page_size
    registros = query.offset(offset).limit(page_size).all()

    items = []
    for usuario, sindico_id in registros:
        items.append(
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "apartamento": usuario.apartamento,
                "status": usuario.status.value if hasattr(usuario.status, "value") else str(usuario.status),
                "is_sindico": sindico_id is not None,
                # O modelo atual não possui data de cadastro; usamos a ordem de criação (id).
                "ordem_cadastro": usuario.id
            }
        )

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0
    }


def buscar_sindico_por_id(
    db: Session,
    user_id: int
):
    return (
        db.query(Sindico)
        .filter(Sindico.id == user_id)
        .first()
    )


def promover(
    db: Session,
    user_id: int
):
    sindico_existente = buscar_sindico_por_id(db, user_id)
    if sindico_existente:
        return sindico_existente

    novo_sindico = Sindico(
        id=user_id
    )

    db.add(novo_sindico)
    db.commit()

    return novo_sindico


def rebaixar(
    db: Session,
    sindico: Sindico
):

    db.delete(sindico)
    db.commit()

    return True


def total_sindicos(db: Session):

    return db.query(Sindico).count()