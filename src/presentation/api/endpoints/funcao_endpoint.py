from fastapi import APIRouter, HTTPException, status
from src.presentation.api.schemas.funcao_schema import CriarFuncaoSchema, AtualizarFuncaoSchema, FuncaoSchema
from src.infrastructure.database.funcao_repository import FuncaoRepository
import sqlite3
from typing import List

router = APIRouter(tags=["Funções Componentes (FPA)"])
repo = FuncaoRepository()

@router.post("/funcoes", response_model=dict, status_code=201)
def cadastrar_funcao(funcao: CriarFuncaoSchema):
    try:
        novo_id = repo.criar(funcao.model_dump())
        return {"status": "sucesso", "mensagem": "Função cadastrada com sucesso e complexidade calculada!", "funcaofpa_id": novo_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade. Verifique se o projeto_id existe.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/{projeto_id}/funcoes", response_model=List[FuncaoSchema])
def listar_funcoes_do_projeto(projeto_id: int):
    return repo.listar_por_projeto(projeto_id)

@router.put("/funcoes/{funcao_id}")
def atualizar_funcao(funcao_id: int, dados_atualizacao: AtualizarFuncaoSchema):
    dados = {k: v for k, v in dados_atualizacao.model_dump().items() if v is not None}
    if not repo.buscar_por_id(funcao_id):
        raise HTTPException(status_code=404, detail="Função não encontrada.")
    if repo.atualizar(funcao_id, dados):
        return {"status": "sucesso", "mensagem": "Função atualizada com sucesso!"}
    raise HTTPException(status_code=400, detail="Nenhuma alteração realizada.")

@router.delete("/funcoes/{funcao_id}")
def deletar_funcao(funcao_id: int):
    if not repo.buscar_por_id(funcao_id):
        raise HTTPException(status_code=404, detail="Função não encontrada.")
    if repo.deletar(funcao_id):
        return {"status": "sucesso", "mensagem": "Função removida com sucesso!"}
    raise HTTPException(status_code=500, detail="Erro ao remover função.")