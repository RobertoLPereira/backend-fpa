from typing import List, Dict, Optional
from infrastructure.database.connection import DBConnection

class FuncaoRepository:
    def __init__(self):
        self.db = DBConnection()

    def criar(self, dados: dict) -> int:
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        try:
            # 💡 RESOLUÇÃO DINÂMICA: Substituímos o valor estático por uma Subquery 
            # que busca a sigla diretamente da tabela 'tipos_funcao_fpa' usando o ID.
            query = """
                INSERT INTO funcoes_fpa (
                    projeto_id, 
                    descricao, 
                    tipo_funcao, 
                    arquivos_referenciados, 
                    itens_dados
                )
                VALUES (
                    :projeto_id, 
                    :descricao, 
                    (SELECT sigla FROM tipos_funcao_fpa WHERE id = :tipo_funcao_id), 
                    :arquivos_referenciados, 
                    :itens_dados
                )
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
        """
        Atualiza uma função componente convertendo o ID do Swagger 
        na String física exigida pela CHECK CONSTRAINT do DDL.
        """
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        
        # 💡 TRADUÇÃO CIRÚRGICA: Mapeia o ID vindo do Swagger para a string do DDL
        tipo_id = dados.get("tipo_funcao_id", 1)
        mapa_siglas = {1: "ALI", 2: "AIE", 3: "EE", 4: "SE", 5: "CE"}
        sigla_fpa = mapa_siglas.get(tipo_id, "ALI")

        query = """
            UPDATE funcoes_fpa 
            SET descricao = ?, 
                tipo_funcao = ?, 
                arquivos_referenciados = ?, 
                itens_dados = ?
            WHERE id = ?
        """
        try:
            cursor.execute(query, (
                dados["descricao"],
                sigla_fpa, # 💡 Grava 'ALI', 'EE', etc., respeitando seu CHECK do SQLite
                int(dados["arquivos_referenciados"]),
                int(dados["itens_dados"]),
                funcao_id
            ))
            conexao.commit()
            
            # Retorna True se o banco gravou e alterou a linha com sucesso
            return cursor.rowcount > 0
        except Exception as e:
            conexao.rollback()
            print(f"❌ [SQLite] Erro crítico no PUT /api/funcoes: {str(e)}")
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
            