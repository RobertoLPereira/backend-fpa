from pydantic import BaseModel, Field
from typing import List, Optional

class ItemNotaInfluenciaSchema(BaseModel):
    caracteristica_id: int = Field(..., description="ID da característica no catálogo")
    nome: Optional[str] = Field(None, description="Nome retornado apenas na leitura")
    nota: int = Field(..., ge=0, le=5, description="Nota de influência variando estritamente de 0 a 5")

class AtualizarNotasProjetoSchema(BaseModel):
    notas: List[ItemNotaInfluenciaSchema] = Field(..., description="Lista de características e suas respectivas novas notas")
    
class FatoresInfluenciaSchema(BaseModel):
    projeto_id: int
    comunicacao_dados: int = Field(0, ge=0, le=5)
    processamento_distribuido: int = Field(0, ge=0, le=5)
    performance: int = Field(0, ge=0, le=5)
    utilizacao_equipamento: int = Field(0, ge=0, le=5)
    volume_transacoes: int = Field(0, ge=0, le=5)
    entrada_dados_online: int = Field(0, ge=0, le=5)
    eficiencia_usuario_final: int = Field(0, ge=0, le=5)
    atualizacao_online: int = Field(0, ge=0, le=5)
    processamento_complexo: int = Field(0, ge=0, le=5)
    reutilizacao_codigo: int = Field(0, ge=0, le=5)
    facilidade_implantacao: int = Field(0, ge=0, le=5)
    facilidade_operacional: int = Field(0, ge=0, le=5)
    multiplos_locais: int = Field(0, ge=0, le=5)
    facilidade_mudancas: int = Field(0, ge=0, le=5)
    class Config:
        from_attributes = True

class AtualizarFatoresSchema(BaseModel):
    comunicacao_dados: Optional[int] = Field(None, ge=0, le=5)
    processamento_distribuido: Optional[int] = Field(None, ge=0, le=5)
    performance: Optional[int] = Field(None, ge=0, le=5)
    utilizacao_equipamento: Optional[int] = Field(None, ge=0, le=5)
    volume_transacoes: Optional[int] = Field(None, ge=0, le=5)
    entrada_dados_online: Optional[int] = Field(None, ge=0, le=5)
    eficiencia_usuario_final: Optional[int] = Field(None, ge=0, le=5)
    atualizacao_online: Optional[int] = Field(None, ge=0, le=5)
    processamento_complexo: Optional[int] = Field(None, ge=0, le=5)
    reutilizacao_codigo: Optional[int] = Field(None, ge=0, le=5)
    facilidade_implantacao: Optional[int] = Field(None, ge=0, le=5)
    facilidade_operacional: Optional[int] = Field(None, ge=0, le=5)
    multiplos_locais: Optional[int] = Field(None, ge=0, le=5)
    facilidade_mudancas: Optional[int] = Field(None, ge=0, le=5)
