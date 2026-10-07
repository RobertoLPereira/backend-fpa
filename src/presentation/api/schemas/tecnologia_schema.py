from pydantic import BaseModel, Field

class TecnologiaSchema(BaseModel):
    id: int = Field(0, description="0 para novos cadastros, ou o ID existente para edição")
    nome: str = Field(..., min_length=1, max_length=100, pattern=r"^\s*\S.*$") 
    produtividade_desenvolvimento: float = Field(..., gt=0, description="Taxa de esforço para novos projetos")
    produtividade_manutencao: float = Field(..., gt=0, description="Taxa de esforço para sustentação")
