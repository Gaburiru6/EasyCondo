from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.area import Area
from app.schemas.area import AreaCreate


def listar_area(db: Session):
    return db.query(Area).all()


def criar_area(db: Session, area_data: AreaCreate):

    area_existente = (
        db.query(Area)
        .filter(
            Area.nome == area_data.nome,
            Area.ativo == True
        )
        .first()
    )

    if area_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma área ativa com esse nome."
        )

    nova_area = Area(**area_data.model_dump())

    db.add(nova_area)
    db.commit()
    db.refresh(nova_area)

    return nova_area


def eliminar_area(db: Session, area_id: int):
    area = db.query(Area).filter(Area.id == area_id).first()

    if area:
        db.delete(area)
        db.commit()
        return True

    return False


def atualizar_area(db: Session, area_id: int, area_data: AreaCreate):

    area = db.query(Area).filter(
        Area.id == area_id
    ).first()

    if not area:
        return None


    area_existente = (
        db.query(Area)
        .filter(
            Area.nome == area_data.nome,
            Area.ativo == True,
            Area.id != area_id
        )
        .first()
    )

    if area_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma área ativa com esse nome."
        )


    for key, value in area_data.model_dump().items():
        setattr(area, key, value)

    db.commit()
    db.refresh(area)

    return area


def alternar_status_area(db: Session, area_id: int):

    area = db.query(Area).filter(
        Area.id == area_id
    ).first()

    if area:
        area.ativo = not area.ativo

        db.commit()
        db.refresh(area)

    return area