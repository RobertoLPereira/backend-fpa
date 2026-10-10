from typing import List, Dict
from infrastructure.database.connection import DBConnection

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

    def obter_relatorio_analitico_agrupado(self, projeto_id: int) -> list:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            # 1. Busca todos os tipos funcionais dinamicamente da tabela de tipos
            cursor.execute("SELECT sigla, nome_extenso, categoria FROM tipos_funcao_fpa ORDER BY categoria DESC, id")
            tipos = cursor.fetchall()
            
            relatorio_completo = []
            
            # 2. Para cada tipo, busca as funções cadastradas calculando os pesos na query
            for sigla, nome_extenso, categoria in tipos:
                query_funcoes = """
                    SELECT 
                        f.descricao, 
                        f.arquivos_referenciados, 
                        f.itens_dados, 
                        f.complexidade,
                        CASE 
                            WHEN f.tipo_funcao IN ('ALI') THEN
                                CASE 
                                    WHEN f.complexidade = 'Simples' THEN 7
                                    WHEN f.complexidade = 'Média' THEN 10
                                    ELSE 15
                                END
                            WHEN f.tipo_funcao IN ('AIE') THEN
                                CASE 
                                    WHEN f.complexidade = 'Simples' THEN 5
                                    WHEN f.complexidade = 'Média' THEN 7
                                    ELSE 10
                                END
                            WHEN f.tipo_funcao IN ('EE', 'CE') THEN
                                CASE 
                                    WHEN f.complexidade = 'Simples' THEN 3
                                    WHEN f.complexidade = 'Média' THEN 4
                                    ELSE 6
                                END
                            WHEN f.tipo_funcao IN ('SE') THEN
                                CASE 
                                    WHEN f.complexidade = 'Simples' THEN 4
                                    WHEN f.complexidade = 'Média' THEN 5
                                    ELSE 7
                                END
                            ELSE 0
                        END AS pontos_funcao
                    FROM funcoes_fpa f
                    WHERE f.projeto_id = ? AND f.tipo_funcao = ?
                    ORDER BY f.id
                """
                cursor.execute(query_funcoes, (projeto_id, sigla))
                linhas = cursor.fetchall()
                
                itens = []
                for r in linhas:
                    itens.append({
                        "descricao": r[0],
                        "registros_arquivos": r[1],
                        "itens_dados": r[2],
                        "complexidade": r[3] if r[3] else "Simples",
                        "pontos_funcao": r[4]
                    })
                    
                # Só adicionamos o bloco ao relatório se ele possuir itens cadastrados
                relatorio_completo.append({
                    "sigla": sigla,
                    "nome_extenso": nome_extenso,
                    "categoria": categoria,
                    "itens": itens
                })
                
            return relatorio_completo
        finally:
            conexao.close()
