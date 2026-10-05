from typing import List

from fastapi import APIRouter, HTTPException
from src.presentation.api.schemas.relatorio_analitico_schema import GrupoAnaliticoSchema
from src.infrastructure.database.relatorio_repository import RelatorioRepository

router = APIRouter(tags=["Relatórios e Planilhas"])
repo = RelatorioRepository()

@router.get("/projetos/{projeto_id}/resumo-executivo")
def get_resumo_executivo(projeto_id: int):
    try:
    # Passamos o projeto_id para filtrar o banco
      return {"status": "sucesso", "dados": repo.obter_resumo_executivo(projeto_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/{projeto_id}/planejamento")
def get_planejamento_detalhado(projeto_id: int):
    try:
        return {"status": "sucesso", "dados": repo.obter_planejamento_master(projeto_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/{projeto_id}/precificacao")
def get_precificacao(projeto_id: int):
    try:
        return {"status": "sucesso", "dados": repo.obter_precificacao(projeto_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/projetos/{projeto_id}/matriz-calculo")
def get_matriz_calculo(projeto_id: int):
    try:
        # Chama a função que lê a view_relatorio_matriz_fpa
        return {"status": "sucesso", "dados": repo.obter_matriz_calculo(projeto_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/{projeto_id}/relatorio-analitico", response_model=List[GrupoAnaliticoSchema])
def obter_relatorio_analitico(projeto_id: int):
    # Chama o repositório instanciado no seu ecossistema
    return repo.obter_relatorio_analitico_agrupado(projeto_id)
