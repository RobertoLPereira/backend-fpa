import os
import sys

# 1. Configuração dinâmica de caminhos (Funciona no Windows do PC e no Linux da Nuvem)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 2. Importações universais limpas (Sem o prefixo )
from infrastructure.database.database_initializer import DatabaseInitializer
from presentation.api.endpoints.backup_endpoint import router as backups_router
from presentation.api.endpoints.fator_endpoint import router as fatores_router
from presentation.api.endpoints.funcao_endpoint import router as funcoes_router
from presentation.api.endpoints.projeto_endpoint import router as projetos_router
from presentation.api.endpoints.relatorio_endpoint import router as relatorios_router
from presentation.api.endpoints.tecnologia_endpoint import router as tecnologias_router
from presentation.api.endpoints.tipo_funcao_endpoint import (
    router as tipo_funcao_fpa_router,
)

# 3. Inicialização do FastAPI
app = FastAPI(
    title="API de Análise de Pontos de Função (FPA)",
    description="Backend completo, modular e robusto orquestrando as 11 abas da planilha FPA",
    version="1.4.0",
)


# 4. Inicialização segura do banco protegida no evento de startup
@app.on_event("startup")
def inicializar_aplicacao():
    initializer = DatabaseInitializer()
    initializer.inicializar_banco()


# 5. Configuração global do CORS para o Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Registro das Rotas Oficiais da API
app.include_router(relatorios_router, prefix="/api")
app.include_router(projetos_router, prefix="/api")
app.include_router(funcoes_router, prefix="/api")
app.include_router(fatores_router, prefix="/api")
app.include_router(backups_router, prefix="/api")
app.include_router(tecnologias_router, prefix="/api")
app.include_router(tipo_funcao_fpa_router, prefix="/api")


# 7. Rota Raiz de Teste
@app.get("/")
def raiz():
    return {
        "status": "online",
        "mensagem": "Backend FPA robusto e modularizado reestabelecido com sucesso!",
    }
