import sys
import os
# Adiciona o diretório atual ao path para evitar erros de ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from src.presentation.api.endpoints.relatorio_endpoint import router as relatorios_router
from src.infrastructure.database.database_initializer import DatabaseInitializer
from src.presentation.api.endpoints.projeto_endpoint import router as projetos_router
from src.presentation.api.endpoints.funcao_endpoint import router as funcoes_router
from src.presentation.api.endpoints.fator_endpoint import router as fatores_router
from src.presentation.api.endpoints.backup_endpoint import router as backups_router
from src.presentation.api.endpoints.tecnologia_endpoint import router as tecnologias_router # 💡 ADICIONE
from src.presentation.api.endpoints.tipo_funcao_endpoint import router as tipo_funcao_fpa_router

initializer = DatabaseInitializer()
initializer.inicializar_banco()

app = FastAPI(
    title="API de Análise de Pontos de Função (FPA)",
    description="Backend completo, modular e robusto orquestrando as 11 abas da planilha FPA",
    version="1.4.0"
)

# Registra todos os módulos de rotas sob o prefixo correto
app.include_router(relatorios_router, prefix="/api")
app.include_router(projetos_router, prefix="/api")
app.include_router(funcoes_router, prefix="/api")
app.include_router(fatores_router, prefix="/api")
app.include_router(backups_router, prefix="/api")
app.include_router(tecnologias_router, prefix="/api")
app.include_router(tipo_funcao_fpa_router, prefix="/api")

@app.get("/")
def raiz():
    return {"status": "online", "mensagem": "Backend FPA robusto e modularizado reestabelecido com sucesso!"}
