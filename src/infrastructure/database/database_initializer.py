import os
import sqlite3
from src.infrastructure.database.connection import DBConnection

class DatabaseInitializer:
    def __init__(self):
        self.db = DBConnection()

    def inicializar_banco(self) -> bool:
        """Verifica se o banco existe. Se não, cria toda a estrutura e dados iniciais."""
        db_path = self.db.db_path
        
        # Se o banco já existe, não faz nada para não apagar os dados existentes
        if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
            return False

        print(f"⚙️ Banco de dados '{db_path}' não encontrado ou vazio. Iniciando criação do zero...")
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        try:
            # 1. Ativar chaves estrangeiras
            cursor.execute("PRAGMA foreign_keys = ON;")

            # 2. Criar Tabelas Base
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnologias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                produtividade REAL NOT NULL
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_projeto TEXT NOT NULL,
                gerente_projeto TEXT,
                responsavel TEXT,
                data_elaboracao TEXT,
                numero_projeto TEXT,
                tecnologia_id INTEGER,
                tipo_atividade TEXT CHECK (tipo_atividade IN ('Desenvolvimento', 'Manutenção')),
                valor_ponto_funcao REAL NOT NULL DEFAULT 89.44,
                ajuste_adicional REAL DEFAULT 0.65,
                FOREIGN KEY (tecnologia_id) REFERENCES tecnologias (id)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_funcao_fpa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sigla TEXT NOT NULL UNIQUE,
                nome_extenso TEXT NOT NULL,
                categoria TEXT NOT NULL CHECK (categoria IN ('Dados', 'Transação'))
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcoes_fpa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projeto_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                tipo_funcao_id INTEGER NOT NULL,
                arquivos_referenciados INTEGER DEFAULT 0,
                itens_dados INTEGER DEFAULT 0,
                complexidade TEXT DEFAULT 'Simples',
                FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
                FOREIGN KEY (tipo_funcao_id) REFERENCES tipos_funcao_fpa(id) ON DELETE CASCADE
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS características_influencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS projeto_notas_influencia (
                projeto_id INTEGER NOT NULL,
                caracteristica_id INTEGER NOT NULL,
                nota INTEGER DEFAULT 0 CHECK (nota BETWEEN 0 AND 5),
                PRIMARY KEY (projeto_id, caracteristica_id),
                FOREIGN KEY (projeto_id) REFERENCES projetos (id) ON DELETE CASCADE,
                FOREIGN KEY (caracteristica_id) REFERENCES características_influencia (id) ON DELETE CASCADE
            );
            """)

            # 3. Criar a Trigger de Inicialização Automática de Notas
            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_inicializar_notas_projeto
            AFTER INSERT ON projetos
            FOR EACH ROW
            BEGIN
                INSERT INTO projeto_notas_influencia (projeto_id, caracteristica_id, nota)
                SELECT NEW.id, id, 0 FROM características_influencia;
            END;
            """)

            # 4. Inserir Dados Default (Carga Inicial Obrigatória)
            tecnologias_padrao = [('JAVA', 10.0), ('PYTHON', 8.0), ('FLUTTER', 7.0), ('ANGULAR', 9.0)]
            cursor.executemany("INSERT OR IGNORE INTO tecnologias (nome, produtividade) VALUES (?, ?);", tecnologias_padrao)

            fatores_padrao = [
                ('Comunicação de Dados',), ('Processamento Distribuído',), ('Performance',),
                ('Utilização do Equipamento',), ('Volume de Transações',), ('Entrada de Dados "On-Line"',),
                ('Eficiência do Usuário Final',), ('Atualização "On-Line"',), ('Processamento Complexo',),
                ('Reutilização de Código',), ('Facilidade de Implantação',), ('Facilidade Operacional',),
                ('Múltiplos Locais',), ('Facilidade de Mudanças',)
            ]
            cursor.executemany("INSERT OR IGNORE INTO características_influencia (nome) VALUES (?);", fatores_padrao)

            tipos_padrao = [
                ('ALI', 'Arquivo Lógico Interno', 'Dados'),
                ('AIE', 'Arquivo de Interface Externa', 'Dados'),
                ('EE', 'Entrada Externa', 'Transação'),
                ('SE', 'Saída Externa', 'Transação'),
                ('CE', 'Consulta Externa', 'Transação')
            ]
            cursor.executemany("INSERT OR IGNORE INTO tipos_funcao_fpa (sigla, nome_extenso, categoria) VALUES (?, ?, ?);", tipos_padrao)

            # 5. Criar as Views Matemáticas Essenciais
            cursor.execute("""
            CREATE VIEW IF NOT EXISTS view_relatorio_matriz_fpa AS
            WITH matriz_estatica AS (
                SELECT 'ALI' AS tipo_funcao, 'Simples' AS complexidade, 7 AS peso_unitario, 1 AS ordem_tipo, 'Arq. Interno (ALI)' AS tipo_funcao_nome UNION ALL
                SELECT 'ALI', 'Média', 10, 1, 'Arq. Interno (ALI)' UNION ALL
                SELECT 'ALI', 'Complexa', 15, 1, 'Arq. Interno (ALI)' UNION ALL
                SELECT 'EE', 'Simples', 3, 3, 'Entrada Externa (EE)' UNION ALL
                SELECT 'EE', 'Média', 4, 3, 'Entrada Externa (EE)' UNION ALL
                SELECT 'EE', 'Complexa', 6, 3, 'Entrada Externa (EE)' UNION ALL
                SELECT 'SE', 'Simples', 4, 4, 'Saída Externa (SE)' UNION ALL
                SELECT 'SE', 'Média', 5, 4, 'Saída Externa (SE)' UNION ALL
                SELECT 'SE', 'Complexa', 7, 4, 'Saída Externa (SE)' UNION ALL
                SELECT 'CE', 'Simples', 3, 5, 'Consulta Externa (CE)' UNION ALL
                SELECT 'CE', 'Média', 4, 5, 'Consulta Externa (CE)' UNION ALL
                SELECT 'CE', 'Complexa', 6, 5, 'Consulta Externa (CE)'
            ),
            contagem_real AS (
                SELECT f.projeto_id, t.sigla AS tipo_funcao, f.complexidade, COUNT(*) AS qtd
                FROM funcoes_fpa f
                JOIN tipos_funcao_fpa t ON f.tipo_funcao_id = t.id
                GROUP BY f.projeto_id, t.sigla, f.complexidade
            ),
            matriz_por_projeto AS (
                SELECT p.id AS projeto_id, p.nome_projeto, m.tipo_funcao, m.complexidade, m.peso_unitario, m.ordem_tipo, m.tipo_funcao_nome
                FROM projetos p
                CROSS JOIN matriz_estatica m
            )
            SELECT mp.nome_projeto AS "Projeto", mp.tipo_funcao_nome AS "Tipo de Função", mp.complexidade AS "Complexidade",
                   COALESCE(cr.qtd, 0) AS "Quantidade", mp.peso_unitario || '.0' AS "Peso", (COALESCE(cr.qtd, 0) * mp.peso_unitario) AS "Total Complexidade"
            FROM matriz_por_projeto mp
            LEFT JOIN contagem_real cr ON mp.projeto_id = cr.projeto_id AND mp.tipo_funcao = cr.tipo_funcao AND mp.complexidade = cr.complexidade;
            """)

            cursor.execute("""
            CREATE VIEW IF NOT EXISTS view_relatorio_fpa_final AS
            WITH resumo_pontos AS (
                SELECT p.id AS projeto_id, SUM(m."Total Complexidade") AS total_pf_nao_ajustado
                FROM view_relatorio_matriz_fpa m
                JOIN projetos p ON m."Projeto" = p.nome_projeto
                GROUP BY p.id
            ),
            calculo_ni AS (
                SELECT projeto_id, SUM(nota) AS nivel_influencia_ni
                FROM projeto_notas_influencia
                GROUP BY projeto_id
            )
            SELECT p.nome_projeto AS "Projeto", p.gerente_projeto AS "Gerente Responsável",
                   COALESCE(r.total_pf_nao_ajustado, 0) AS "Pontos de Função Não Ajustados",
                   COALESCE(n.nivel_influencia_ni, 0) AS "Nível de Influência (NI)",
                   ROUND((COALESCE(n.nivel_influencia_ni, 0) * 0.01) + p.ajuste_adicional, 2) AS "Fator de Ajuste Calculado",
                   ROUND(COALESCE(r.total_pf_nao_ajustado, 0) * ROUND((COALESCE(n.nivel_influencia_ni, 0) * 0.01) + p.ajuste_adicional, 2), 2) AS "Pontos de Função Ajustados (FPA)",
                   p.valor_ponto_funcao AS "Valor por PF (R$)",
                   ROUND((COALESCE(r.total_pf_nao_ajustado, 0) * ROUND((COALESCE(n.nivel_influencia_ni, 0) * 0.01) + p.ajuste_adicional, 2)) * p.valor_ponto_funcao, 2) AS "Valor Total do Projeto (R$)"
            FROM projetos p
            LEFT JOIN resumo_pontos r ON p.id = r.projeto_id
            LEFT JOIN calculo_ni n ON p.id = n.projeto_id;
            """)
            cursor.execute("""
            DROP VIEW IF EXISTS view_planejamento_master;

            CREATE VIEW view_planejamento_master AS
            WITH esforco_por_funcao AS (
                -- 💡 Calcula as horas de cada função baseando-se no Peso vs Produtividade da tecnologia do projeto
                SELECT 
                    f.projeto_id,
                    p.nome_projeto AS "Projeto",
                    t_fpa.nome_extenso AS "Grupo Funcional",
                    f.descricao AS "Componente",
                    -- Puxa o peso estático de acordo com o tipo e complexidade real
                    CASE 
                        WHEN t_fpa.sigla = 'ALI' AND f.complexidade = 'Simples' THEN 7
                        WHEN t_fpa.sigla = 'ALI' AND f.complexidade = 'Média' THEN 10
                        WHEN t_fpa.sigla = 'ALI' AND f.complexidade = 'Complexa' THEN 15
                        WHEN t_fpa.sigla = 'AIE' AND f.complexidade = 'Simples' THEN 5
                        WHEN t_fpa.sigla = 'AIE' AND f.complexidade = 'Média' THEN 7
                        WHEN t_fpa.sigla = 'AIE' AND f.complexidade = 'Complexa' THEN 10
                        WHEN t_fpa.sigla = 'EE'  AND f.complexidade = 'Simples' THEN 3
                        WHEN t_fpa.sigla = 'EE'  AND f.complexidade = 'Média' THEN 4
                        WHEN t_fpa.sigla = 'EE'  AND f.complexidade = 'Complexa' THEN 6
                        WHEN t_fpa.sigla = 'SE'  AND f.complexidade = 'Simples' THEN 4
                        WHEN t_fpa.sigla = 'SE'  AND f.complexidade = 'Média' THEN 5
                        WHEN t_fpa.sigla = 'SE'  AND f.complexidade = 'Complexa' THEN 7
                        WHEN t_fpa.sigla = 'CE'  AND f.complexidade = 'Simples' THEN 3
                        WHEN t_fpa.sigla = 'CE'  AND f.complexidade = 'Média' THEN 4
                        WHEN t_fpa.sigla = 'CE'  AND f.complexidade = 'Complexa' THEN 6
                        ELSE 0
                    END AS peso_calculado,
                    tec.produtividade
                FROM funcoes_fpa f
                JOIN projetos p ON f.projeto_id = p.id
                JOIN tipos_funcao_fpa t_fpa ON f.tipo_funcao_id = t_fpa.id
                JOIN tecnologias tec ON p.tecnologia_id = tec.id
            ),
            matriz_horas AS (
                SELECT 
                    projeto_id,
                    "Projeto",
                    "Grupo Funcional",
                    "Componente",
                    -- Total de Horas da Linha = Peso x Produtividade (Ex: 10 * 8.2 = 82 horas)
                    ROUND(peso_calculado * produtividade, 1) AS total_horas
                FROM esforco_por_funcao
            )
            SELECT 
                projeto_id,
                "Projeto",
                "Grupo Funcional",
                "Componente",
                ROUND(total_horas * 0.20, 1) AS "Levantamento",
                ROUND(total_horas * 0.20, 1) AS "Especificação",
                ROUND(total_horas * 0.50, 1) AS "Desenvolvimento",
                ROUND(total_horas * 0.10, 1) AS "Homologação",
                total_horas AS "Subtotal Horas"
            FROM matriz_horas;""")

            conexao.commit()
            print("🚀 Estrutura de tabelas, triggers, views e dados default estabelecida com sucesso!")
            return True
        except Exception as e:
            conexao.rollback()
            print(f"❌ Erro crítico ao inicializar o banco: {str(e)}")
            raise e
        finally:
            conexao.close()
