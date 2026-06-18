from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_sindico
from app.services import sindico_service

router = APIRouter(
    prefix="/sindicos",
    tags=["Sindicos"]
)


@router.get("/moradores")
def listar(
    nome: str = None,
    ordenar_por: str = "nome",
    ordem: str = "asc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    _sindico_id: int = Depends(require_sindico)
):
    return sindico_service.listar_moradores(
        db,
        nome,
        ordenar_por,
        ordem,
        page,
        page_size
    )


@router.post("/promover/{id}")
def promover(
    id: int,
    db: Session = Depends(get_db),
    _sindico_id: int = Depends(require_sindico)
):
    return sindico_service.promover(
        db,
        id
    )


@router.delete("/rebaixar/{id}")
def rebaixar(
    id: int,
    db: Session = Depends(get_db),
    _sindico_id: int = Depends(require_sindico)
):
    return sindico_service.rebaixar(
        db,
        id
    )