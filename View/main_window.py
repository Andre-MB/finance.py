import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date


class MainWindow(tk.Tk):
    def __init__(self, controller, usuario):
        super().__init__()
        self.controller = controller
        self.usuario = usuario
        self.title("Finance")
        self.geometry("600x450")

        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"

        self.config(bg=bg_color)

        

        tk.Label(
            self,
            text=f"Bem-vindo, {self.usuario['name']}!",
            font=("Arial", 14),
            bg=bg_color,
            fg=fg_color,
        ).pack(pady=20)



        data_atual = date.today()
        mes_atual = data_atual.month



        frame = tk.Frame(bg="#2E2E2E")
        frame.pack(pady=10, padx=10)

        # --- COMBOBOX MÊS ---
        tk.Label(frame, text="Mês:", bg=bg_color, fg="#FFFFFF").grid(row=0, column=0, padx=5)

        self.meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        self.combo_mes = ttk.Combobox(frame, values=self.meses, state="readonly")
        self.combo_mes.set(self.meses[mes_atual - 1])
        self.combo_mes.grid(row=0, column=1, padx=5)

        # --- COMBOBOX ANO ---
        tk.Label(frame, text="Ano:", bg=bg_color, fg="#FFFFFF").grid(row=0, column=2, padx=5)

        self.combo_ano = ttk.Combobox(frame, values=[2024, 2025, 2026], state="readonly")
        self.combo_ano.set("2025")
        self.combo_ano.grid(row=0, column=3, padx=5)

        # LABELS
        self.label_saldo = tk.Label(text="Saldo: R$ 0.00", bg=bg_color, fg="#FFFFFF")
        self.label_saldo.pack(pady=2)

        self.label_receita = tk.Label(text="Receitas: R$ 0.00", bg=bg_color, fg="#FFFFFF")
        self.label_receita.pack(pady=2)

        self.label_despesa = tk.Label(text="Despesas: R$ 0.00", bg=bg_color, fg="#FFFFFF")
        self.label_despesa.pack(pady=2)

        self.label_investido = tk.Label(text="Investido: R$ 0.00", bg=bg_color, fg="#FFFFFF")
        self.label_investido.pack(pady=2)


        self.combo_mes.bind("<<ComboboxSelected>>", self.atualizar_valores)
        self.combo_ano.bind("<<ComboboxSelected>>", self.atualizar_valores)

        

        # ---- LABELS que exibem o valor selecionado ----
        # label_ano = tk.Label( text=f"Ano selecionado: 2025", bg=bg_color, fg="#FFFFFF")
        # label_ano.pack(pady=2)

        # label_mes = tk.Label( text=f"Mês selecionado: {meses[mes_atual - 1]}", bg=bg_color, fg="#FFFFFF")
        # label_mes.pack(pady=2)

        # # ---- FUNÇÕES ----
        # def getcomboboxmes(event):
        #     label_mes.config(text=f"Mês selecionado: {combo_mes.get()}")

        # def getcomboboxano(event):
        #     label_ano.config(text=f"Ano selecionado: {combo_ano.get()}")

        # # Bind
        # combo_mes.bind("<<ComboboxSelected>>", getcomboboxmes)
        # combo_ano.bind("<<ComboboxSelected>>", getcomboboxano)


        self.btn_buscar = tk.Button(
            self,
            text="Ver Transações",
            command=lambda: self.buscar_dados(
                self.meses.index(self.combo_mes.get()) + 1,
                int(self.combo_ano.get())
            ),
            bg="#007BFF",
            fg=fg_color,
            relief="flat",
        )
        self.btn_buscar.pack(pady=5)

        self.btn_adicionar = tk.Button(
            self,
            text="Adicionar Transação",
            command=self.abrir_janela_adicionar,
            bg="#007BFF",
            fg=fg_color,
            relief="flat",
        )
        self.btn_adicionar.pack(pady=5)


        # Frame pra mostrar a quantidade de transacoes tem por categoria
        self.frame_categorias = tk.Frame(self, bg="#2E2E2E")
        self.frame_categorias.pack(pady=10)




        # Atualiza os dados da view quanto carrega a pagina
        self.atualizar_valores(None)

    def buscar_dados(self, mes, ano):
        self.controller.buscar_dados_do_banco(mes,ano)

    def exibir_dados(self, dados):

        janela = tk.Toplevel()
        janela.title("Transações")
        janela.config(bg="#2E2E2E")

        # Estilo para o Treeview (tabela)
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2E2E2E",
            foreground="white",
            fieldbackground="#3E3E3E",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#007BFF")])
        style.configure(
            "Treeview.Heading", background="#3E3E3E", foreground="white", relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#555555")])

        colunas = ("Nome", "Valor", "Categoria", "Pagamento", "Data")
        tree = ttk.Treeview(janela, columns=colunas, show="headings")

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        for row in dados:
            id_transacao = row[0]
            valores_visiveis = row[1:]  
            tree.insert("", tk.END, iid=str(id_transacao), values=valores_visiveis)

        tree.pack(expand=True, fill="both")

        def deletar_transacao():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma transação para deletar.")
                return

            id_transacao = selecionado[0]  # iid = idTransaction

            confirmar = messagebox.askyesno(
                "Confirmar", "Deseja realmente excluir esta transação?"
            )

            if confirmar:
                self.controller.deletar_transacao(id_transacao)
                tree.delete(id_transacao)
                messagebox.showinfo("Sucesso", "Transação excluída!")
                self.atualizar_valores(None)

         # Botão de excluir
        btn_delete = tk.Button(
            janela,
            text="Deletar Transação",
            bg="#C21818",
            fg="white",
            relief="flat",
            command=deletar_transacao,
        )
        btn_delete.pack(pady=5)

    def abrir_janela_adicionar(self):
        # Cria uma nova janela (Toplevel)
        janela_add = tk.Toplevel(self)
        janela_add.title("Nova Transação")
        janela_add.geometry("400x300")
        janela_add.config(bg="#2E2E2E")  # Cor de fundo dark

        # --- Campos de Entrada (Labels e Entrys) ---
        frame = tk.Frame(janela_add, bg="#2E2E2E")
        frame.pack(pady=20, padx=20)

        # Campo Nome
        tk.Label(frame, text="Nome:", bg="#2E2E2E", fg="#FFFFFF").grid(
            row=0, column=0, sticky="w"
        )
        entry_nome = tk.Entry(frame, bg="#3E3E3E", fg="#FFFFFF")
        entry_nome.grid(row=0, column=1, pady=5)

        # Campo Valor
        tk.Label(frame, text="Valor (R$):", bg="#2E2E2E", fg="#FFFFFF").grid(
            row=1, column=0, sticky="w"
        )
        entry_valor = tk.Entry(frame, bg="#3E3E3E", fg="#FFFFFF")
        entry_valor.grid(row=1, column=1, pady=5)

        # Campo Tipo (usando um Combobox)
        tk.Label(frame, text="Tipo:", bg="#2E2E2E", fg="#FFFFFF").grid(
            row=2, column=0, sticky="w"
        )
        # O ideal é buscar esses valores do banco. Vamos usar valores fixos por enquanto.
        tipos_transacao = [
            "Receita",
            "Despesa",
        ]  # Assumindo que estes existem na sua tabela TransactionType
        # Carrega os tipos dinamicamente do banco de dados
        tipos_transacao = self.controller.buscar_tipos()
        combo_tipo = ttk.Combobox(frame, values=tipos_transacao, state="readonly")
        combo_tipo.grid(row=2, column=1, pady=5)

        # Campo Categoria
        tk.Label(frame, text="Categoria:", bg="#2E2E2E", fg="#FFFFFF").grid(
            row=3, column=0, sticky="w"
        )
        # Valores de exemplo. Crie-os na sua tabela TransactionCategory.
        categorias = ["Salário", "Alimentação", "Transporte", "Lazer"]
        # Carrega as categorias dinamicamente do banco de dados
        categorias = self.controller.buscar_categorias()
        combo_categoria = ttk.Combobox(frame, values=categorias, state="readonly")
        combo_categoria.grid(row=3, column=1, pady=5)

        # Campo Método de Pagamento
        tk.Label(frame, text="Pagamento:", bg="#2E2E2E", fg="#FFFFFF").grid(
            row=4, column=0, sticky="w"
        )
        # Carrega os métodos de pagamento dinamicamente do banco de dados
        metodos_pagamento = self.controller.buscar_metodos_pagamento()
        combo_pagamento = ttk.Combobox(
            frame, values=metodos_pagamento, state="readonly"
        )
        combo_pagamento.grid(row=4, column=1, pady=5)

        # --- Botão Salvar ---
        # A função lambda é importante para passar os argumentos para o método salvar
        btn_salvar = tk.Button(
            janela_add,
            text="Salvar",
            command=lambda: self.salvar_transacao(
                janela_add,  # Passa a própria janela para poder fechá-la
                entry_nome.get(),
                entry_valor.get(),
                combo_tipo.get(),
                combo_categoria.get(),
                combo_pagamento.get(),
            ),
        )
        btn_salvar.pack(pady=10)

    # Ainda na classe MainWindow

    def salvar_transacao(
        self, janela_para_fechar, nome, valor, tipo, categoria, metodo_pagamento
    ):
        # Validação simples
        if not nome or not valor or not tipo or not categoria or not metodo_pagamento:
            messagebox.showerror(
                "Erro", "Preencha todos os campos.", parent=janela_para_fechar
            )
            return

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror(
                "Erro", "O valor deve ser um número.", parent=janela_para_fechar
            )
            return

        # Chama o método do controller para fazer a mágica
        self.controller.adicionar_transacao(
            nome, valor_float, tipo, categoria, metodo_pagamento
        )

        # Fecha a janelinha de adicionar
        janela_para_fechar.destroy()

    def atualizar_valores(self, event):
        mes = self.meses.index(self.combo_mes.get()) + 1
        ano = int(self.combo_ano.get())

        resultados = self.controller.buscar_receitas_despesas_investimentos(ano,mes)
        resultados_categoria = self.controller.buscar_quantidade_transacoes_categoria(ano,mes)

        receita = 0.0
        despesa = 0.0
        investimento = 0.0

        if resultados:
            for item in resultados:
                nome = item["name"].lower()
                total = float(item["total"])

                if nome in ["depósito"]:
                    receita += total
                elif nome == "despesa":
                    despesa += total
                elif nome == "investimento":
                    investimento += total

        # Atualizar labels
        self.label_receita.config(text=f"Receitas: R$ {receita:.2f}")
        self.label_despesa.config(text=f"Despesas: R$ {despesa:.2f}")
        self.label_investido.config(text=f"Investido: R$ {investimento:.2f}")

        saldo = receita - despesa
        self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")


        # Parte que printa na tela as quantidades por categoria
        # Limpar categorias antigas
        for widget in self.frame_categorias.winfo_children():
            widget.destroy()

        # Caso não haja categorias
        if not resultados_categoria:
            tk.Label(self.frame_categorias, text="Nenhuma categoria encontrada.",
                    bg="#2E2E2E", fg="white").pack()
            return

        # Criar título
        tk.Label(self.frame_categorias, text="Transações por categoria:",
                bg="#2E2E2E", fg="white", font=("Arial", 10, "bold")).pack()

        # Exibir cada categoria
        for item in resultados_categoria:
            categoria = item["name"]
            total = item["total"]

            tk.Label(
                self.frame_categorias,
                text=f"{categoria}: {total}",
                bg="#2E2E2E",
                fg="white",
                anchor="w"
            ).pack(fill="x")




        