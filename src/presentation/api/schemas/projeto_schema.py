from pydantic import BaseModel, Field
from typing import Optional

class BaseProjeto(BaseModel):
    nome_projeto: str = Field(..., min_length=3)
    gerente_projeto: Optional[str] = None
    responsavel: Optional[str] = None
    data_elaboracao: Optional[str] = None
    numero_projeto: Optional[str] = "S/N"
    tecnologia_id: int
    tipo_atividade: str = "Desenvolvimento"
    valor_ponto_funcao: float = 89.44

class CriarProjetoSchema(BaseProjeto):
    pass

class AtualizarProjetoSchema(BaseModel):
    nome_projeto: Optional[str] = None
    gerente_projeto: Optional[str] = None
    responsavel: Optional[str] = None
    data_elaboracao: Optional[str] = None
    numero_projeto: Optional[str] = None
    tecnologia_id: Optional[int] = None
    tipo_atividade: Optional[str] = None
    valor_ponto_funcao: Optional[float] = None

class ProjetoSchema(BaseProjeto):
    id: int
    class Config:
        from_attributes = True
