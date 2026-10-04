from typing import List, Dict
from src.infrastructure.database.connection import DBConnection

class TecnologiaRepository:
    def __init__(self):
        self.db = DBConnection()

    def listar_todas(self) -> List[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, produtividade_desenvolvimento,produtividade_manutencao FROM tecnologias ORDER BY nome ASC")
        linhas = cursor.fetchall()
        conexao.close()
        return [dict(l) for l in linhas]
