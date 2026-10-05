from pydantic import BaseModel, Field
from typing import Optional

class BaseFuncaoFPA(BaseModel):
    projeto_id: int
    descricao: str = Field(..., min_length=2)
    tipo_funcao_id: int = Field(..., description="ID correspondente na tabela tipos_funcao_fpa")
    arquivos_referenciados: int = Field(0, ge=0)
    itens_dados: int = Field(0, ge=0)

class CriarFuncaoSchema(BaseFuncaoFPA):
    pass

class FuncaoSchema(BaseFuncaoFPA):
    id: int
    complexidade: Optional[str] = None
