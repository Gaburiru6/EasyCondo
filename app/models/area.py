from pydantic import BaseModel

class Area(BaseModel):
    id: int
    nome: str
    descricao: str
    taxa: float
    possuiTaxa: bool
    antecedenciaMinimaHoras: int
    limiteSemanal: int
    limiteMensal: int
    tempoMaximoDesistenciaHoras: int