from fastapi import APIRouter, HTTPException
from src.presentation.api.schemas.fator_schema import FatoresInfluenciaSchema, AtualizarFatoresSchema
from src.infrastructure.database.fator_repository import FatorRepository
from src.infrastructure.database.projeto_repository import ProjetoRepository

router = APIRouter(tags=["Fatores de Influência (Notas 0 a 5)"])
repo_fator = FatorRepository()
repo_projeto = ProjetoRepository()

@router.get("/projetos/{projeto_id}/fatores", response_model=FatoresInfluenciaSchema)
def obter_fatores_do_projeto(projeto_id: int):
    if not repo_projeto.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return repo_fator.buscar_por_projeto(projeto_id)

@router.put("/projetos/{projeto_id}/fatores")
def atualizar_fatores_do_projeto(projeto_id: int, dados_atualizacao: AtualizarFatoresSchema):
    dados = {k: v for k, v in dados_atualizacao.model_dump().items() if v is not None}
    if not repo_projeto.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    if repo_fator.atualizar(projeto_id, dados):
        return {"status": "sucesso", "mensagem": "Notas atualizadas e relatórios recalculados!"}
    raise HTTPException(status_code=400, detail="Nenhuma alteração realizada.")