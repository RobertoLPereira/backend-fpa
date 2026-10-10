from fastapi import APIRouter, HTTPException, status
from infrastructure.services.backup_service import BackupService
from infrastructure.database.database_initializer import DatabaseInitializer # 💡 NOVO
from typing import List
 
router = APIRouter(tags=["Administração e Segurança"])
backup_service = BackupService()

@router.get("/sistema/backups", response_model=List[str])
def listar_backups_disponiveis():
    """Retorna a lista de todos os arquivos de backup (.db) disponíveis para restauração."""
    try:
        return backup_service.listar_backups()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar arquivos de segurança: {str(e)}"
        )
    
@router.post("/sistema/backup", status_code=status.HTTP_201_CREATED)
def disparar_backup_manual():
    """Gera um ponto de restauração (Backup) do banco de dados na pasta local."""
    try:
        caminho_arquivo = backup_service.realizar_backup()
        return {
            "status": "sucesso",
            "mensagem": "Backup realizado com sucesso!",
            "arquivo_gerado": caminho_arquivo
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao gerar cópia de segurança: {str(e)}"
        )
@router.post("/sistema/restaurar", status_code=status.HTTP_200_OK)
def disparar_restauracao_manual(nome_arquivo_backup: str):
    """
    Substitui os dados atuais pelo backup selecionado.
    🛡️ Realiza um backup preventivo automático do estado atual antes da operação.
    """
    try:
        # Executa a restauração e captura o caminho do backup preventivo gerado
        arquivo_preventivo = backup_service.restaurar_backup(nome_arquivo_backup)
        return {
            "status": "sucesso",
            "mensagem": f"Banco de dados restaurado com sucesso para o ponto: {nome_arquivo_backup}!",
            "seguranca_automatica": f"Um backup preventivo do estado anterior foi salvo em: {arquivo_preventivo}"
        }
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha crítica ao restaurar o banco de dados: {str(e)}"
        )
@router.post("/sistema/inicializar-banco", status_code=status.HTTP_200_OK)
def forçar_inicializacao_banco():
    """Força a verificação e criação do esquema de tabelas e dados default se o banco sumir."""
    initializer = DatabaseInitializer()
    criado = initializer.inicializar_banco()
    if criado:
        return {"status": "sucesso", "mensagem": "Um novo banco de dados limpo foi gerado e configurado!"}
    return {"status": "sucesso", "mensagem": "O banco de dados já existe e está operacional. Nenhuma alteração foi necessária."}
    