import sqlite3

class DBConnection:
    def __init__(self, db_path: str = "fpa.db"):
        self.db_path = db_path

    def obter_conexao(self):
        conexao = sqlite3.connect(self.db_path)
        conexao.row_factory = sqlite3.Row
        return conexao
