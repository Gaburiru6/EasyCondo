from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.solicitacao_service import listar, aprovar, negar
from app.api.deps import get_db
from typing import List
from app.schemas.user import UserResponse

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações"])


@router.get("/", response_model=List[UserResponse])
def listar(db: Session = Depends(get_db)):
    return listar(db)

@router.put("/{id}/aprovar")
def aprovar(id: int, db: Session = Depends(get_db)):
    return aprovar(db, id)

@router.put("/{id}/negar")
def negar(id: int, db: Session = Depends(get_db)):
    return negar(db, id)