from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import solicitacao_service
from app.api.deps import get_db

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações"])


@router.get("/")
def listar(db: Session = Depends(get_db)):
    return solicitacao_service.listar(db)


@router.put("/{id}/aprovar")
def aprovar(id: int, db: Session = Depends(get_db)):
    return solicitacao_service.aprovar(db, id)


@router.put("/{id}/negar")
def negar(id: int, db: Session = Depends(get_db)):
    return solicitacao_service.negar(db, id)