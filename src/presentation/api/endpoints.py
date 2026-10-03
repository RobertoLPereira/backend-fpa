from fastapi import APIRouter, HTTPException
from src.infrastructure.database.repositories import RelatorioRepository

router = APIRouter()
repo = RelatorioRepository(db_path="fpa.db") # Aponta para o seu arquivo de banco de dados

@router.get("/projetos/resumo-executivo")
def get_resumo_executivo():
    """Rota que retorna as 4 linhas do card comercial idêntico ao print."""
    try:
        dados = repo.obter_resumo_executivo()
        return {"status": "sucesso", "dados": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler banco: {str(e)}")

@router.get("/projetos/planejamento")
def get_planejamento_detalhado():
    """Rota que entrega a matriz completa de horas dividida por fases e blocos."""
    try:
        dados = repo.obter_planejamento_master()
        return {"status": "sucesso", "dados": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler banco: {str(e)}")

@router.get("/projetos/precificacao")
def get_precificacao():
    """Rota que entrega o valor financeiro total calculado do projeto."""
    try:
        dados = repo.obter_precificacao()
        return {"status": "sucesso", "dados": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler banco: {str(e)}")
