from typing import List, Dict
from src.infrastructure.database.connection import DBConnection

class RelatorioRepository:
    def __init__(self):
        self.db = DBConnection()
    
    def _executar_consulta(self, query: str, parametros: tuple = ()) -> List[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, parametros)
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]
        finally:
            conexao.close()

    def obter_resumo_executivo(self, projeto_id: int) -> List[Dict]:
        # Filtra os indicadores vinculando o ID do projeto na View
        query = """SELECT * FROM view_relatorio_fpa_final WHERE "Projeto" = (SELECT nome_projeto FROM projetos WHERE id = ?)"""
        return self._executar_consulta(query, (projeto_id,))

    def obter_planejamento_master(self, projeto_id: int) -> List[Dict]:
        query = """
            SELECT * FROM view_planejamento_master 
            WHERE "Projeto" = (SELECT nome_projeto FROM projetos WHERE id = ?)
        """
        return self._executar_consulta(query, (projeto_id,))

    def obter_precificacao(self, projeto_id: int) -> List[Dict]:
        # 💡 FILTRA FILÉ: Puxa os KPIs financeiros unicamente do projeto selecionado
        query = """
            SELECT * FROM view_precificacao_projeto 
            WHERE "Projeto" = (SELECT nome_projeto FROM projetos WHERE id = ?)
        """
        return self._executar_consulta(query, (projeto_id,))

    def obter_matriz_calculo(self, projeto_id: int) -> List[Dict]:
        # 💡 ORDENAÇÃO IMPECÁVEL: Lê a sua view_relatorio_matriz_fpa filtrando pelo ID do projeto ativo
        query = """
            SELECT * FROM view_relatorio_matriz_fpa 
            WHERE "Projeto" = (SELECT nome_projeto FROM projetos WHERE id = ?)
        """
        return self._executar_consulta(query, (projeto_id,))