import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self, controller, usuario):
        super().__init__()
        self.controller = controller
        self.usuario = usuario
        self.title("Finance")
        self.geometry("400x250")

        # Cores do Dark Mode
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"

        # Configurar a cor de fundo da janela principal
        self.config(bg=bg_color)

        self.label = tk.Label(
            self, text="Finance", bg=bg_color, fg=fg_color, font=("Arial", 16, "bold")
        )
        self.label.pack(pady=10)

        tk.Label(
            self,
            text=f"Bem-vindo, {self.usuario['name']}!",
            font=("Arial", 14),
            bg=bg_color,
            fg=fg_color,
        ).pack(pady=20)

        self.btn_buscar = tk.Button(
            self,
            text="Ver Transações",
            command=self.buscar_dados,
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

    def buscar_dados(self):
        self.controller.buscar_dados_do_banco()

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
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill="both")

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
