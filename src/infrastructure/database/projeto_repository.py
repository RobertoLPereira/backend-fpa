from typing import List, Dict, Optional
from infrastructure.database.connection import DBConnection

class ProjetoRepository:
    def __init__(self):
        self.db = DBConnection()

    def criar(self, dados: dict) -> int:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            query_projeto = """
                INSERT INTO projetos (nome_projeto, gerente_projeto, responsavel, data_elaboracao, numero_projeto, tecnologia_id, tipo_atividade, valor_ponto_funcao)
                VALUES (:nome_projeto, :gerente_projeto, :responsavel, :data_elaboracao, :numero_projeto, :tecnologia_id, :tipo_atividade, :valor_ponto_funcao)
            """
            cursor.execute(query_projeto, dados)
            projeto_id = cursor.lastrowid

            query_fatores = "INSERT INTO fatores_influencia (projeto_id) VALUES (?)"
            cursor.execute(query_fatores, (projeto_id,))
            
            conexao.commit()
            return projeto_id
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def listar_todos(self) -> List[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM projetos")
        linhas = cursor.fetchall()
        conexao.close()
        return [dict(l) for l in linhas]

    def buscar_por_id(self, projeto_id: int) -> Optional[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM projetos WHERE id = ?", (projeto_id,))
        linha = cursor.fetchone()
        conexao.close()
        return dict(linha) if linha else None

    def atualizar(self, projeto_id: int, dados: dict) -> bool:
        if not dados: return False
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
            query = f"UPDATE projetos SET {campos} WHERE id = :projeto_id"
            dados["projeto_id"] = projeto_id
            cursor.execute(query, dados)
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def deletar(self, projeto_id: int) -> bool:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("DELETE FROM projetos WHERE id = ?", (projeto_id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()
            