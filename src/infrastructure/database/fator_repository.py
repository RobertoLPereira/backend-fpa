from typing import Optional, Dict, List
from src.infrastructure.database.connection import DBConnection

class FatorRepository:
    def __init__(self):
        self.db = DBConnection()

    def listar_notas_detalhadas(self, projeto_id: int) -> List[Dict]:
        """Retorna os nomes das características e as notas associadas de um projeto específico."""
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        
        # 💡 Usamos apelidos simples (fator_id e nome_fator) para evitar caracteres especiais
        query = """
            SELECT c.id, c.nome, COALESCE(p.nota, 0)
            FROM características_influencia c
            LEFT JOIN projeto_notas_influencia p ON p.caracteristica_id = c.id AND p.projeto_id = ?
            ORDER BY c.id ASC
        """
        try:
            cursor.execute(query, (projeto_id,))
            linhas = cursor.fetchall()
            
            # 💡 MAPEA MANUAMENTE POR POSIÇÃO FÍSICA: Elimina qualquer chance de retornar None
            resultado = []
            for linha in linhas:
                resultado.append({
                    "caracteristica_id": int(linha[0]),
                    "nome": str(linha[1]),
                    "nota": int(linha[2])
                })
            return resultado
        except Exception as e:
            raise e
        finally:
            conexao.close()

    def atualizar_notas_lote(self, projeto_id: int, lista_notas: list) -> bool:
        """Atualiza em lote (Batch) as notas das características de um projeto específico."""
        conexao = self.db.obter_conexao()
        cursor = conexao.cursor()
        
        # 💡 CORREÇÃO CRÍTICA: Mudado para '?' na ordem exata da tupla para destravar o executemany
        query = """
            UPDATE projeto_notas_influencia 
            SET nota = ? 
            WHERE projeto_id = ? AND caracteristica_id = ?
        """
        try:
            # 💡 FORMATO DE TUPLA: O executemany exige (valor1, valor2, valor3) casado com os '?'
            dados_lote = []
            for item in lista_notas:
                dados_lote.append((
                    int(item["nota"]),              # 1º ponto de interrogação: SET nota = ?
                    int(projeto_id),               # 2º ponto de interrogação: WHERE projeto_id = ?
                    int(item["caracteristica_id"])   # 3º ponto de interrogação: AND caracteristica_id = ?
                ))
            
            # Executa a gravação física em lote de forma nativa e real no arquivo do banco
            print(query,dados_lote);
            cursor.executemany(query, dados_lote)
            conexao.commit()
            
            print(f"🛡️ [SQLite] Lote de {len(dados_lote)} notas processado e gravado com sucesso!")
            return True
        except Exception as e:
            conexao.rollback()
            print(f"❌ [SQLite] Erro ao gravar lote no banco: {str(e)}")
            raise e
        finally:
            conexao.close()
