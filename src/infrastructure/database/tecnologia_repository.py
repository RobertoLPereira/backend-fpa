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
    
    def criar(self, dados: dict) -> int:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        query = """
            INSERT INTO tecnologias (nome, produtividade_desenvolvimento, produtividade_manutencao)
            VALUES (?, ?, ?)
        """
        try:
            cursor.execute(query, (dados["nome"], dados["produtividade_desenvolvimento"], dados["produtividade_manutencao"]))
            conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def atualizar(self, id_tec: int, dados: dict) -> bool:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        query = """
            UPDATE tecnologias 
            SET nome = ?, produtividade_desenvolvimento = ?, produtividade_manutencao = ?
            WHERE id = ?
        """
        try:
            cursor.execute(query, (dados["nome"], dados["produtividade_desenvolvimento"], dados["produtividade_manutencao"], id_tec))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def deletar(self, id_tec: int) -> bool:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM tecnologias WHERE id = ?", (id_tec,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            return False
        finally:
            conexao.close()

