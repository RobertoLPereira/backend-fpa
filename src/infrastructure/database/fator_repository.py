from typing import Optional, Dict
from src.infrastructure.database.connection import DBConnection

class FatorRepository:
    def __init__(self):
        self.db = DBConnection()

    def buscar_por_projeto(self, projeto_id: int) -> Optional[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM fatores_influencia WHERE projeto_id = ?", (projeto_id,))
        linha = cursor.fetchone()
        conexao.close()
        return dict(linha) if linha else None

    def atualizar(self, projeto_id: int, dados: dict) -> bool:
        if not dados: return False
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
            query = f"UPDATE fatores_influencia SET {campos} WHERE projeto_id = :projeto_id"
            dados["projeto_id"] = projeto_id
            cursor.execute(query, dados)
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()
    def listar_notas_detalhadas(self, projeto_id: int) -> list:        
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        query = """
            SELECT c.nome, COALESCE(p.nota, 0) as nota
            FROM características_influencia c
            LEFT JOIN projeto_notas_influencia p ON p.caracteristica_id = c.id AND p.projeto_id = ?
            ORDER BY c.id ASC
        """
        cursor.execute(query, (projeto_id,))
        linhas = cursor.fetchall()
        conexao.close()
        return [dict(l) for l in linhas]
        