from typing import List, Dict, Optional
from src.infrastructure.database.connection import DBConnection

class FuncaoRepository:
    def __init__(self):
        self.db = DBConnection()

    def criar(self, dados: dict) -> int:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            query = """
                INSERT INTO funcoes_fpa (projeto_id, descricao, tipo_funcao, arquivos_referenciados, itens_dados)
                VALUES (:projeto_id, :descricao, :tipo_funcao, :arquivos_referenciados, :itens_dados)
            """
            cursor.execute(query, dados)
            conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def listar_por_projeto(self, projeto_id: int) -> List[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM funcoes_fpa WHERE projeto_id = ?", (projeto_id,))
        linhas = cursor.fetchall()
        conexao.close()
        return [dict(l) for l in linhas]

    def buscar_por_id(self, funcao_id: int) -> Optional[Dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM funcoes_fpa WHERE id = ?", (funcao_id,))
        linha = cursor.fetchone()
        conexao.close()
        return dict(linha) if linha else None

    def atualizar(self, funcao_id: int, dados: dict) -> bool:
        if not dados: return False
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
            query = f"UPDATE funcoes_fpa SET {campos} WHERE id = :funcom_id"
            dados["funcom_id"] = funcao_id
            cursor.execute(query, dados)
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def deletar(self, funcao_id: int) -> bool:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM funcoes_fpa WHERE id = ?", (funcao_id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()