from typing import List, Dict
from src.infrastructure.database.connection import DBConnection

class TipoFuncaoFpaRepository:
    def __init__(self):
        self.db = DBConnection()

    def obter_todos(self) -> list[dict]:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            # 💡 Mapeado exatamente com as colunas físicas do banco
            cursor.execute("SELECT id, sigla, nome_extenso, categoria FROM tipos_funcao_fpa ORDER BY id")
            colunas = [col[0] for col in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        finally:
            conexao.close()

    def criar(self, dados: dict) -> int:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            query = """
                INSERT INTO tipos_funcao_fpa (sigla, nome_extenso, categoria)
                VALUES (:sigla, :nome_extenso, :categoria)
            """
            cursor.execute(query, dados)
            conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()
    
    def atualizar(self, id: int, dados: dict) -> bool:
            if not dados: return False
            conexao = self.db.obter_conexao()
            cursor = conexao.cursor()
            try:
                campos = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
                query = f"UPDATE tipos_funcao_fpa SET {campos} WHERE id = :id"
                dados["id"] = id
                cursor.execute(query, dados)
                conexao.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conexao.rollback()
                raise e
            finally:
                conexao.close()
        
    def deletar(self, tipo_id: int) -> bool:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM tipos_funcao_fpa WHERE id = ?", (tipo_id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()
