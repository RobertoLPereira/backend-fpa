from fastapi import APIRouter, HTTPException
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
