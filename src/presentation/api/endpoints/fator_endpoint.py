from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from src.infrastructure.database.fator_repository import FatorRepository
from src.infrastructure.database.projeto_repository import ProjetoRepository
from typing import List, Optional

router = APIRouter(tags=["Fatores de Influência (Notas 0 a 5)"])
repo_fator = FatorRepository()
repo_projeto = ProjetoRepository()

# 💡 CORREÇÃO CIRÚRGICA: Alterado de String para str (minúsculo padrão Python)
class ItemNotaInfluenciaSchema(BaseModel):
    caracteristica_id: int
    nome: Optional[str] = None
    nota: int = Field(..., ge=0, le=5)

class AtualizarNotasProjetoSchema(BaseModel):
    notas: List[ItemNotaInfluenciaSchema]

@router.get("/projetos/{projeto_id}/fatores-detalhado", response_model=List[ItemNotaInfluenciaSchema])
def obter_fatores_detalhadados_relatorio(projeto_id: int):
    """Retorna os fatores e notas estruturados para o Flutter."""
    if not repo_projeto.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return repo_fator.listar_notas_detalhadas(projeto_id)

@router.put("/projetos/{projeto_id}/fatores", status_code=status.HTTP_200_OK)
def atualizar_fatores_do_projeto(projeto_id: int, payload: AtualizarNotasProjetoSchema):
    """Atualiza as notas em lote e recalcula as views de precificação e relatório."""
    if not repo_projeto.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    
    dados_atualizacao = [item.model_dump() for item in payload.notas]
    if repo_fator.atualizar_notas_lote(projeto_id, dados_atualizacao):
        return {"status": "sucesso", "mensagem": "Notas atualizadas e relatórios recalculados!"}
    raise HTTPException(status_code=400, detail="Nenhuma alteração realizada.")
