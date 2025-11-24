import os
from dotenv import load_dotenv
from Model.database import Database
from View.main_window import MainWindow
from tkinter import messagebox

load_dotenv()


class MainController:
    def __init__(self, user_controller, root, usuario):
        self.user_controller = user_controller
        db_password = os.getenv("DB_PASSWORD")
        self.db = Database(
            host="ep-soft-feather-a4ymlnb0-pooler.us-east-1.aws.neon.tech",
            database="neondb",
            user="neondb_owner",
            password=db_password,
        )
        self.db.connect()
        self.root = root
        self.usuario = usuario
        self.view = MainWindow(self.root, self, usuario)

    def iniciar_app(self):
        pass

    def logout(self):
        if self.view:
            self.view.destroy()
        self.user_controller.reiniciar_para_login()

    def buscar_dados_do_banco(self, mes, ano):
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
        dados = self.db.fetch_all(query, (id_usuario, ano, mes))
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

    def buscar_quantidade_transacoes_categoria(self, year, month):
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
        resultados = self.db.fetch_all(query, (id_usuario, year, month))
        return (
            [{"name": item[0], "total": item[1]} for item in resultados]
            if resultados
            else []
        )

    def adicionar_transacao(
        self, nome, valor, tipo_nome, categoria_nome, pagamento_nome
    ):
        from datetime import date  # Importa a classe date

        id_usuario = self.usuario["idUser"]
        data_hoje = date.today()  # Pega a data de hoje

        try:
            query_tipo = 'SELECT "idType" FROM "TransactionType" WHERE "name" = %s'
            resultado_tipo = self.db.fetch_one(query_tipo, (tipo_nome,))
            if not resultado_tipo:
                raise ValueError(f"Tipo '{tipo_nome}' não encontrado.")
            id_tipo = resultado_tipo[0]

            query_categoria = (
                'SELECT "idCategory" FROM "TransactionCategory" WHERE "name" = %s'
            )
            resultado_categoria = self.db.fetch_one(query_categoria, (categoria_nome,))
            if not resultado_categoria:
                raise ValueError(f"Categoria '{categoria_nome}' não encontrada.")
            id_categoria = resultado_categoria[0]

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
        self.view.atualizar_valores(None)

    def buscar_transacao_por_id(self, id_transacao):
        query = """
            SELECT 
                t.name, 
                t.amount, 
                tt.name AS type_name,
                tc.name AS category_name, 
                tpm.name AS payment_method_name
            FROM "Transaction" t
            JOIN "TransactionType" tt ON t."idType" = tt."idType"
            JOIN "TransactionCategory" tc ON t."idCategory" = tc."idCategory"
            JOIN "TransactionPaymentMethod" tpm ON t."idPaymentMethod" = tpm."idPaymentMethod"
            WHERE t."idTransaction" = %s;
        """
        return self.db.fetch_one(query, (id_transacao,))

    def atualizar_transacao(
        self, id_transacao, nome, valor, tipo_nome, categoria_nome, pagamento_nome
    ):
        try:
            query_tipo = 'SELECT "idType" FROM "TransactionType" WHERE "name" = %s'
            id_tipo = self.db.fetch_one(query_tipo, (tipo_nome,))[0]

            query_categoria = (
                'SELECT "idCategory" FROM "TransactionCategory" WHERE "name" = %s'
            )
            id_categoria = self.db.fetch_one(query_categoria, (categoria_nome,))[0]

            query_pagamento = 'SELECT "idPaymentMethod" FROM "TransactionPaymentMethod" WHERE "name" = %s'
            id_pagamento = self.db.fetch_one(query_pagamento, (pagamento_nome,))[0]

        except (TypeError, IndexError) as e:
            messagebox.showerror(
                "Erro de Dados",
                f"Não foi possível encontrar os IDs para os nomes fornecidos. Erro: {e}",
            )
            return False

        query = """
        UPDATE "Transaction" SET
            "name" = %s, 
            "amount" = %s, 
            "idType" = %s, 
            "idCategory" = %s, 
            "idPaymentMethod" = %s
        WHERE "idTransaction" = %s
        """
        params = (nome, valor, id_tipo, id_categoria, id_pagamento, id_transacao)

        try:
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Transação atualizada com sucesso!")
            self.view.atualizar_valores(None)
            return True
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não foi possível atualizar a transação.\nErro: {e}"
            )
            return False

    def buscar_resumo_financeiro_completo(self, year, month):
        id_usuario = self.usuario["idUser"]
        query = """
        WITH transacoes_mes AS (
            SELECT t.amount, tt.name AS tipo, tc.name AS categoria
            FROM "Transaction" t
            JOIN "TransactionType" tt ON t."idType" = tt."idType"
            JOIN "TransactionCategory" tc ON t."idCategory" = tc."idCategory"
            WHERE t."idUser" = %s
              AND EXTRACT(YEAR FROM t.date) = %s
              AND EXTRACT(MONTH FROM t.date) = %s
        )
        SELECT 
            tipo, 
            categoria, 
            SUM(amount) as total
        FROM transacoes_mes
        GROUP BY tipo, categoria;
        """
        resultados_db = self.db.fetch_all(query, (id_usuario, year, month))

        resumo = {
            "receita": 0.0,
            "despesa": 0.0,
            "investimento": 0.0,
            "gastos_por_categoria": [],
            "investimentos_por_categoria": [],
        }

        if not resultados_db:
            return resumo

        for tipo, categoria, total in resultados_db:
            total_float = float(total)
            if tipo == "Depósito":
                resumo["receita"] += total_float
            elif tipo == "Despesa":
                resumo["despesa"] += total_float
                resumo["gastos_por_categoria"].append((categoria, total_float))
            elif tipo == "Investimento":
                resumo["investimento"] += total_float
                resumo["investimentos_por_categoria"].append((categoria, total_float))

        return resumo
