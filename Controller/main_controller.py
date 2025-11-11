import os
from dotenv import load_dotenv
from Model.database import Database
from View.main_window import MainWindow
from tkinter import messagebox

load_dotenv()


class MainController:
    def __init__(self, usuario):
        db_password = os.getenv("DB_PASSWORD")
        self.db = Database(
            host="ep-soft-feather-a4ymlnb0-pooler.us-east-1.aws.neon.tech",
            database="neondb",
            user="neondb_owner",
            password=db_password,
        )
        self.db.connect()
        self.view = MainWindow(self, usuario)
        self.usuario = usuario

    def iniciar_app(self):
        self.view.mainloop()

    def buscar_dados_do_banco(self):
        # Busca as transações do usuário logado, incluindo categoria e método de pagamento
        id_usuario = self.usuario["idUser"]
        query = """
            SELECT 
                t.name, 
                t.amount, 
                tc.name AS category_name, 
                tpm.name AS payment_method_name,
                t.date
            FROM "Transaction" t
            JOIN "TransactionCategory" tc ON t."idCategory" = tc."idCategory"
            JOIN "TransactionPaymentMethod" tpm ON t."idPaymentMethod" = tpm."idPaymentMethod"
            WHERE t."idUser" = %s
            ORDER BY t.date DESC;
        """
        dados = self.db.fetch_all(query, (id_usuario,))
        self.view.exibir_dados(dados)

    def buscar_tipos(self):
        query = 'SELECT "name" FROM "TransactionType" ORDER BY "name"'
        resultados = self.db.fetch_all(query)
        return [item[0] for item in resultados] if resultados else []

    def buscar_categorias(self):
        query = 'SELECT "name" FROM "TransactionCategory" ORDER BY "name"'
        resultados = self.db.fetch_all(query)
        return [item[0] for item in resultados] if resultados else []

    def buscar_metodos_pagamento(self):
        query = 'SELECT "name" FROM "TransactionPaymentMethod" ORDER BY "name"'
        resultados = self.db.fetch_all(query)
        return [item[0] for item in resultados] if resultados else []

    # Dentro da classe MainController

    # ... (depois do método buscar_dados_do_banco)

    def adicionar_transacao(
        self, nome, valor, tipo_nome, categoria_nome, pagamento_nome
    ):
        from datetime import date  # Importa a classe date

        id_usuario = self.usuario["idUser"]
        data_hoje = date.today()  # Pega a data de hoje

        try:
            # --- BUSCAR O ID DO TIPO ---
            query_tipo = 'SELECT "idType" FROM "TransactionType" WHERE "name" = %s'
            resultado_tipo = self.db.fetch_one(query_tipo, (tipo_nome,))
            if not resultado_tipo:
                raise ValueError(f"Tipo '{tipo_nome}' não encontrado.")
            id_tipo = resultado_tipo[0]

            # --- BUSCAR O ID DA CATEGORIA ---
            query_categoria = (
                'SELECT "idCategory" FROM "TransactionCategory" WHERE "name" = %s'
            )
            resultado_categoria = self.db.fetch_one(query_categoria, (categoria_nome,))
            if not resultado_categoria:
                raise ValueError(f"Categoria '{categoria_nome}' não encontrada.")
            id_categoria = resultado_categoria[0]

            # --- BUSCAR O ID DO MÉTODO DE PAGAMENTO ---
            query_pagamento = 'SELECT "idPaymentMethod" FROM "TransactionPaymentMethod" WHERE "name" = %s'
            resultado_pagamento = self.db.fetch_one(query_pagamento, (pagamento_nome,))
            if not resultado_pagamento:
                raise ValueError(
                    f"Método de Pagamento '{pagamento_nome}' não encontrado."
                )
            id_pagamento = resultado_pagamento[0]

        except ValueError as e:
            messagebox.showerror("Erro de Dados", str(e))
            return

        query = """
        INSERT INTO "Transaction" 
        ("name", "amount", "date", "idUser", "idType", "idCategory", "idPaymentMethod")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            nome,
            valor,
            data_hoje,
            id_usuario,
            id_tipo,
            id_categoria,
            id_pagamento,
        )

        try:
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não foi possível adicionar a transação.\nErro: {e}"
            )
