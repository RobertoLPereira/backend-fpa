from fastapi import APIRouter, HTTPException
from src.presentation.api.schemas.projeto_schema import CriarProjetoSchema, AtualizarProjetoSchema, ProjetoSchema
from src.infrastructure.database.projeto_repository import ProjetoRepository
from typing import List

router = APIRouter(tags=["Projetos"])
repo = ProjetoRepository()

@router.post("/projetos", response_model=dict, status_code=201)
def criar_novo_projeto(projeto: CriarProjetoSchema):
    try:
        novo_id = repo.criar(projeto.model_dump())
        return {"status": "sucesso", "mensagem": "Projeto cadastrado com sucesso!", "projeto_id": novo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projetos", response_model=List[ProjetoSchema])
def listar_projetos():
    return repo.listar_todos()

@router.get("/projetos/{projeto_id}", response_model=ProjetoSchema)
def obter_projeto_por_id(projeto_id: int):
    projeto = repo.buscar_por_id(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return projeto

@router.put("/projetos/{projeto_id}")
def atualizar_projeto(projeto_id: int, dados_atualizacao: AtualizarProjetoSchema):
    dados = {k: v for k, v in dados_atualizacao.model_dump().items() if v is not None}
    if not repo.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    if repo.atualizar(projeto_id, dados):
        return {"status": "sucesso", "mensagem": "Projeto atualizado com sucesso!"}
    raise HTTPException(status_code=400, detail="Nenhuma alteração realizada.")

@router.delete("/projetos/{projeto_id}")
def deletar_projeto(projeto_id: int):
    if not repo.buscar_por_id(projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    if repo.deletar(projeto_id):
        return {"status": "sucesso", "mensagem": "Projeto excluído com sucesso!"}
    raise HTTPException(status_code=500, detail="Erro ao excluir projeto.")