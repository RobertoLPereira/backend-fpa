from pydantic import BaseModel
from typing import List

class ItemAnaliticoSchema(BaseModel):
    descricao: str
    registros_arquivos: int  # Mapeia f.arquivos_referenciados
    itens_dados: int        # Mapeia f.itens_dados
    complexidade: str
    pontos_funcao: int

class GrupoAnaliticoSchema(BaseModel):
    sigla: str
    nome_extenso: str
    categoria: str
    itens: List[ItemAnaliticoSchema]
