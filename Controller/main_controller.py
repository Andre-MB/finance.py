import os
from dotenv import load_dotenv
from Model.database import Database
from View.main_window import MainWindow

load_dotenv()

class MainController:
    def __init__(self, usuario):
        db_password = os.getenv("DB_PASSWORD")
        self.db = Database(host="ep-soft-feather-a4ymlnb0-pooler.us-east-1.aws.neon.tech", database="neondb", user="neondb_owner", password=db_password)
        self.db.connect()
        self.view = MainWindow(self,usuario)

    def iniciar_app(self):
        self.view.mainloop()

    def buscar_dados_do_banco(self):
        # Exemplo de interação: buscar todos os usuários de uma tabela
        query = 'SELECT "name", "amount", "date" FROM "Transaction";'
        dados = self.db.fetch_all(query)
        self.view.exibir_dados(dados)