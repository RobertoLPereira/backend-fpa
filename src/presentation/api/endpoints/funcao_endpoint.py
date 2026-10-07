from fastapi import APIRouter, HTTPException, status
# 💡 CORREÇÃO CIRÚRGICA: Removido o 'AtualizarFuncaoSchema' que gerava o erro de importação
from src.presentation.api.schemas.funcao_schema import CriarFuncaoSchema, FuncaoSchema
from src.infrastructure.database.funcao_repository import FuncaoRepository
from typing import List

router = APIRouter(tags=["Funções Componentes (FPA)"])
repo = FuncaoRepository()

@router.post("/funcoes", status_code=201)
def cadastrar_funcao(funcao: CriarFuncaoSchema):
    try:
        novo_id = repo.criar(funcao.model_dump())
        return {"status": "sucesso", "mensagem": "Componente funcional registrado!", "id": novo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos/{projeto_id}/funcoes", response_model=List[dict])
def listar_funcoes_do_projeto(projeto_id: int):
    return repo.listar_por_projeto(projeto_id)

@router.delete("/funcoes/{funcao_id}")
def deletar_funcao(funcao_id: int):
    if repo.deletar(funcao_id):
        return {"status": "sucesso", "mensagem": "Componente removido do escopo!"}
    raise HTTPException(status_code=404, detail="Componente não encontrado.")

@router.put("/funcoes/{funcao_id}")
def atualizar_funcao(funcao_id: int, funcao: CriarFuncaoSchema):
    try:
        if repo.atualizar(funcao_id, funcao.model_dump()):
            return {"status": "sucesso", "mensagem": "Componente funcional atualizado!"}
        raise HTTPException(status_code=404, detail="Componente não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
