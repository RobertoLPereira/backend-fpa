from fastapi import APIRouter, HTTPException, status

from src.presentation.api.schemas.tipo_funcao_schema import TipoFuncaoCriar, TipoFuncaoResposta,AtualizarTipoFuncaoSchema
# Injetar os imports corretos das suas classes do sistema
from src.infrastructure.database.tipo_funcao_repository import TipoFuncaoFpaRepository
router = APIRouter(tags=["Tipos de Função FPA"])
repo = TipoFuncaoFpaRepository()

@router.get("/tipofuncaofpa", response_model=list[TipoFuncaoResposta])
def listar_tipos():
    return repo.obter_todos()

@router.post("/tipofuncaofpa", response_model=int, status_code=status.HTTP_201_CREATED)
def criar_tipo(payload: TipoFuncaoCriar):
    try:
        return repo.criar(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de integridade ou constraint: {str(e)}")

@router.put("/{tipo_id}/tipofuncaofpa", response_model=bool)
def atualizar_tipo(tipo_id: int, dados: AtualizarTipoFuncaoSchema):
    sucesso = repo.atualizar(tipo_id, dados.model_dump())
    if not sucesso:
        raise HTTPException(status_code=404, detail="Tipo funcional não localizado.")
    return sucesso

@router.delete("/{tipo_id}/tipofuncaofpa", response_model=bool)
def deletar_tipo(tipo_id: int):
    try:
        sucesso = repo.deletar(tipo_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Tipo funcional não localizado.")
        return sucesso
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incapaz de remover: Existem referências em sub-tabelas.")
