from fastapi import APIRouter, HTTPException
from src.infrastructure.database.relatorio_repository import RelatorioRepository

router = APIRouter(tags=["Relatórios e Planilhas"])
repo = RelatorioRepository()

@router.get("/projetos/resumo-executivo")
def get_resumo_executivo():
    try:
        return {"status": "sucesso", "dados": repo.obter_resumo_executivo()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/planejamento")
def get_planejamento_detalhado():
    try:
        return {"status": "sucesso", "dados": repo.obter_planejamento_master()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/precificacao")
def get_precificacao():
    try:
        return {"status": "sucesso", "dados": repo.obter_precificacao()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))