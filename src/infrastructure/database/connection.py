import os
import sqlite3
from pathlib import Path


class DBConnection:

    def __init__(self, db_name: str = "fpa.db"):
        # 1. Descobre a pasta onde este arquivo connection.py está salvo
        BASE_DIR = Path(__file__).resolve().parent

        # 2. Une a pasta do projeto ao nome do banco de dados de forma absoluta
        self.db_path = os.path.join(BASE_DIR, db_name)

    def obter_conexao(self):
        conexao = sqlite3.connect(self.db_path)
        conexao.row_factory = sqlite3.Row
        return conexao
