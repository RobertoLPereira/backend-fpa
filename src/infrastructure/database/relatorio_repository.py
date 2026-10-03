from typing import List, Dict
from src.infrastructure.database.connection import DBConnection

class RelatorioRepository:
    def __init__(self):
        self.db = DBConnection()

    def _executar_consulta(self, query: str) -> List[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(query)
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]
        finally:
            conexao.close()

    def obter_resumo_executivo(self) -> List[Dict]:
        return self._executar_consulta("SELECT Indicador FROM view_resumo_executivo_fpa")

    def obter_planejamento_master(self) -> List[Dict]:
        return self._executar_consulta("SELECT * FROM view_planejamento_master")

    def obter_precificacao(self) -> List[Dict]:
        return self._executar_consulta("SELECT * FROM view_precificacao_projeto")
