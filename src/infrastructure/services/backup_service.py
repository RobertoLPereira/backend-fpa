import os
import sqlite3
from datetime import datetime
 
class BackupService:
    def __init__(self, db_path: str = "fpa.db", backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir

    def realizar_backup(self) -> str:
        """Gera uma cópia física segura e compacta do fpa.db com carimbo de data/hora."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Banco de dados de origem '{self.db_path}' não foi encontrado.")

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        carimbo_tempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_backup = f"backup_fpa_{carimbo_tempo}.db"
        caminho_final = os.path.join(self.backup_dir, nome_backup)

        con_origem = sqlite3.connect(self.db_path)
        con_destino = sqlite3.connect(caminho_final)
        
        try:
            with con_destino:
                con_origem.backup(con_destino)
            return caminho_final
        finally:
            con_destino.close()
            con_origem.close()

    def restaurar_backup(self, nome_arquivo_backup: str) -> str:
        """
        Substitui o fpa.db atual pelo backup selecionado.
        Garante um backup preventivo automático do estado atual antes de sobrescrever.
        """
        caminho_backup = os.path.join(self.backup_dir, nome_arquivo_backup)

        # 1. Valida se o arquivo de backup de origem realmente existe
        if not os.path.exists(caminho_backup):
            raise FileNotFoundError(f"O arquivo de backup '{nome_arquivo_backup}' não foi encontrado na pasta '{self.backup_dir}'.")

        # 2. 🛡️ SEGURANÇA MÁXIMA: Faz o backup preventivo automático do estado atual
        carimbo_tempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_backup_preventivo = f"backup_preventivo_antes_de_restaurar_{carimbo_tempo}.db"
        caminho_preventivo = os.path.join(self.backup_dir, nome_backup_preventivo)

        con_atual_bkp = sqlite3.connect(self.db_path)
        con_preventivo = sqlite3.connect(caminho_preventivo)
        try:
            with con_preventivo:
                con_atual_bkp.backup(con_preventivo)
        finally:
            con_preventivo.close()
            con_atual_bkp.close()

        # 3. Executa a restauração (sobrescreve o fpa.db atual com o backup escolhido)
        con_backup = sqlite3.connect(caminho_backup)
        con_atual = sqlite3.connect(self.db_path)
        try:
            with con_atual:
                con_backup.backup(con_atual)
            return caminho_preventivo
        except Exception as e:
            raise e
        finally:
            con_atual.close()
            con_backup.close()
    
    def listar_backups(self) -> list:
        """Retorna uma lista com os nomes de todos os arquivos de backup disponíveis, ordenados do mais recente para o mais antigo."""
        if not os.path.exists(self.backup_dir):
            return []
            
        # Lista todos os arquivos da pasta que terminam com .db
        arquivos = [f for f in os.listdir(self.backup_dir) if f.endswith('.db')]
        
        # Ordena os arquivos para que o backup mais recente apareça primeiro na lista
        arquivos.sort(reverse=True)
        return arquivos
