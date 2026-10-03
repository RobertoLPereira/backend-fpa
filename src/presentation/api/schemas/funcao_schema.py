from pydantic import BaseModel, Field
from typing import Optional, Literal

class BaseFuncaoFPA(BaseModel):
    projeto_id: int
    descricao: str = Field(..., min_length=2)
    tipo_funcao: Literal['EE', 'SE', 'CE', 'ALI', 'AIE']
    arquivos_referenciados: int = Field(0, ge=0)
    itens_dados: int = Field(0, ge=0)

class CriarFuncaoSchema(BaseFuncaoFPA):
    pass

class AtualizarFuncaoSchema(BaseModel):
    descricao: Optional[str] = None
    tipo_funcao: Optional[Literal['EE', 'SE', 'CE', 'ALI', 'AIE']] = None
    arquivos_referenciados: Optional[int] = None
    itens_dados: Optional[int] = None

class FuncaoSchema(BaseFuncaoFPA):
    id: int
    complexidade: Optional[str] = None
    class Config:
        from_attributes = True
