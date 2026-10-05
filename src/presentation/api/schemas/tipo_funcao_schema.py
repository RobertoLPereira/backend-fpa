from typing import Optional

from pydantic import BaseModel, Field

class TipoFuncaoBase(BaseModel):
    id: int = Field(..., description="Id" )
    sigla: str = Field(..., max_length=3, description="Sigla oficial (Ex: ALI, EE)")
    nome_extenso: str = Field(..., max_length=30, description="Nome extenso do tipo funcional")
    categoria: str = Field(..., max_length=12, description="Categoria'")

class TipoFuncaoCriar(TipoFuncaoBase):
    pass

class AtualizarTipoFuncaoSchema(BaseModel):
    sigla: Optional[str] = None
    nome_extenso: Optional[str] = None
    categoria: Optional[str] = None    

class TipoFuncaoResposta(TipoFuncaoBase):
    id: int

    class Config:
        from_attributes = True

