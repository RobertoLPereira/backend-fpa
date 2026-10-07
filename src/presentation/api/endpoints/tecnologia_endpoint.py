import sqlite3

from fastapi import APIRouter, HTTPException,status
from src.presentation.api.schemas.tecnologia_schema import TecnologiaSchema
from src.infrastructure.database.tecnologia_repository import TecnologiaRepository

from typing import List

router = APIRouter(tags=["Tecnologias (Fatores de Produtividade)"])
repo = TecnologiaRepository()

@router.get("/tecnologias", response_model=List[dict])
def listar_tecnologias():
    try:
        return repo.listar_todas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tecnologias", status_code=201)
def cadastrar_tecnologia(payload: TecnologiaSchema):
    try:
        novo_id = repo.criar(payload.model_dump())
        return {"status": "sucesso", "mensagem": "Tecnologia registrada!", "id": novo_id}
    except sqlite3.IntegrityError:
        # 💡 CAPTURA DE INTEGRIDADE: Identifica nome duplicado e barra de forma elegante
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Esta tecnologia/linguagem já está cadastrada no ecossistema."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tecnologias/{tecnologia_id}")
def atualizar_tecnologia(tecnologia_id: int, payload: TecnologiaSchema):
    if repo.atualizar(tecnologia_id, payload.model_dump()):
        return {"status": "sucesso", "mensagem": "Tecnologia atualizada com sucesso!"}
    raise HTTPException(status_code=404, detail="Tecnologia não encontrada.")

@router.delete("/tecnologias/{tecnologia_id}")
def deletar_tecnologia(tecnologia_id: int):
    if repo.deletar(tecnologia_id):
        return {"status": "sucesso", "mensagem": "Tecnologia removida do sistema."}
    raise HTTPException(status_code=400, detail="Não é possível remover: existem projetos vinculados a esta tecnologia.")