from tkinter import messagebox
import ttkbootstrap as ttk


class AddTransactionWindow(ttk.Toplevel):
    def __init__(self, parent, controller, callback_on_close):
        super().__init__(parent)
        self.controller = controller
        self.callback_on_close = callback_on_close

        self.title("Nova Transação")
        self.geometry("400x350")

        frame = ttk.Frame(self)
        frame.pack(pady=20, padx=20)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Valor (R$):").grid(row=1, column=0, sticky="w")
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky="w")
        tipos_transacao = self.controller.buscar_tipos()
        self.combo_tipo = ttk.Combobox(frame, values=tipos_transacao, state="readonly")
        self.combo_tipo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Categoria:").grid(row=3, column=0, sticky="w")
        categorias = self.controller.buscar_categorias()
        self.combo_categoria = ttk.Combobox(frame, values=categorias, state="readonly")
        self.combo_categoria.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Pagamento:").grid(row=4, column=0, sticky="w")
        metodos_pagamento = self.controller.buscar_metodos_pagamento()
        self.combo_pagamento = ttk.Combobox(
            frame, values=metodos_pagamento, state="readonly"
        )
        self.combo_pagamento.grid(row=4, column=1, pady=5)

        self.combo_tipo.bind("<<ComboboxSelected>>", self.on_tipo_selected)

        btn_salvar = ttk.Button(
            self, text="Salvar", command=self.salvar, bootstyle="success"
        )
        btn_salvar.pack(pady=10)

    def on_tipo_selected(self, event):
        tipo_selecionado = self.combo_tipo.get()
        if tipo_selecionado == "Investimento":
            self.combo_categoria.set("Outros")
            self.combo_categoria.config(state="disabled")
        else:
            self.combo_categoria.config(state="readonly")
            if tipo_selecionado == "Despesa":
                self.combo_categoria.set("")

    def salvar(self):
        nome = self.entry_nome.get()
        valor = self.entry_valor.get()
        tipo = self.combo_tipo.get()
        categoria = self.combo_categoria.get()
        metodo_pagamento = self.combo_pagamento.get()

        if not all([nome, valor, tipo, categoria, metodo_pagamento]):
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=self)
            return

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número.", parent=self)
            return

        success = self.controller.adicionar_transacao(
            nome, valor_float, tipo, categoria, metodo_pagamento
        )

        if success:
            self.on_close()

    def on_close(self):
        self.callback_on_close()
        self.destroy()
