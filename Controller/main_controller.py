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
        self.usuario = usuario
        self.view = MainWindow(self, usuario)

    def iniciar_app(self):
        self.view.mainloop()

    def buscar_dados_do_banco(self, mes, ano):
        # Busca as transações do usuário logado, incluindo categoria e método de pagamento
        id_usuario = self.usuario["idUser"]
        query = """
            SELECT 
                t."idTransaction",
                t.name, 
                t.amount, 
                tc.name AS category_name, 
                tpm.name AS payment_method_name,
                to_char(t.date, 'DD/MM/YYYY')
            FROM "Transaction" t
            JOIN "TransactionCategory" tc ON t."idCategory" = tc."idCategory"
            JOIN "TransactionPaymentMethod" tpm ON t."idPaymentMethod" = tpm."idPaymentMethod"
            WHERE 
                t."idUser" = %s
                AND EXTRACT(YEAR FROM t."date") = %s
                AND EXTRACT(MONTH FROM t."date") = %s
            ORDER BY t.date DESC;
        """
        dados = self.db.fetch_all(query, (id_usuario,ano,mes))
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
    
    def buscar_receitas_despesas_investimentos(self,year,month):
        id_usuario = self.usuario["idUser"]
        query = """
            SELECT 
                tc."name",
                COALESCE(SUM(t.amount), 0) AS total
            FROM (
                VALUES
                    ('305f4a9a-d977-48db-9f54-8284eead7105'::uuid),
                    ('38ec343a-1565-4b07-9200-0bf581fa4812'::uuid),
                    ('e66c6a9e-028d-460a-9d01-4019c283a0f7'::uuid)
            ) AS c(id)
            LEFT JOIN "TransactionType" tc ON tc."idType" = c.id
            LEFT JOIN "Transaction" t 
                ON t."idType" = c.id
                AND t."idUser" = %s::uuid
                AND EXTRACT(YEAR FROM t."date") = %s
                AND EXTRACT(MONTH FROM t."date") = %s
            GROUP BY c.id, tc.name
            ORDER BY c.id
        """
        resultados = self.db.fetch_all(query, (id_usuario,year,month))
        return [{"name": item[0], "total": float(item[1])} for item in resultados]
    
    def buscar_quantidade_transacoes_categoria(self,year,month):
        id_usuario = self.usuario["idUser"]
        query = """
            SELECT 
                tc.name AS category_name,
                COUNT(*) AS total_transacoes
            FROM "Transaction" t
            JOIN "TransactionCategory" tc 
                ON t."idCategory" = tc."idCategory"
            WHERE 
                t."idUser" = %s
                AND EXTRACT(YEAR FROM t."date") = %s
                AND EXTRACT(MONTH FROM t."date") = %s
            GROUP BY tc.name
            ORDER BY total_transacoes DESC;
        """
        resultados = self.db.fetch_all(query, (id_usuario,year,month))
        return [{"name": item[0], "total": item[1]} for item in resultados]






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
            self.view.atualizar_valores(None)
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não foi possível adicionar a transação.\nErro: {e}"
            )


    def deletar_transacao(self, id_transacao):
        query = 'DELETE FROM "Transaction" WHERE "idTransaction" = %s'
        self.db.execute_query(query, (id_transacao,))
