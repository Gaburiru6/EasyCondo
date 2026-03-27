from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.session import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    taxa = Column(Float)
    possui_taxa = Column(Boolean)
    antecedencia_minima_horas = Column(Integer)
    limite_semanal = Column(Integer)
    limite_mensal = Column(Integer)
    tempo_maximo_desistencia_horas = Column(Integer)