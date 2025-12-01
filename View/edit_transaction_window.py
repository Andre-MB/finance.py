from tkinter import messagebox
import ttkbootstrap as ttk


class EditTransactionWindow(ttk.Toplevel):
    def __init__(self, parent, controller, id_transacao, callback_on_close):
        super().__init__(parent)
        self.controller = controller
        self.id_transacao = id_transacao
        self.callback_on_close = callback_on_close

        self.title("Editar Transação")
        self.geometry("400x350")

        dados_transacao = self.controller.buscar_transacao_por_id(self.id_transacao)
        if not dados_transacao:
            messagebox.showerror(
                "Erro", "Não foi possível carregar os dados da transação.", parent=self
            )
            self.destroy()
            return

        (nome_atual, valor_atual, tipo_atual, categoria_atual, pagamento_atual) = (
            dados_transacao
        )

        frame = ttk.Frame(self)
        frame.pack(pady=20, padx=20)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.insert(0, nome_atual)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Valor (R$):").grid(row=1, column=0, sticky="w")
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.insert(0, f"{valor_atual:.2f}")
        self.entry_valor.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky="w")
        tipos_transacao = self.controller.buscar_tipos()
        self.combo_tipo = ttk.Combobox(frame, values=tipos_transacao, state="readonly")
        self.combo_tipo.set(tipo_atual)
        self.combo_tipo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Categoria:").grid(row=3, column=0, sticky="w")
        categorias = self.controller.buscar_categorias()
        self.combo_categoria = ttk.Combobox(frame, values=categorias, state="readonly")
        self.combo_categoria.set(categoria_atual)
        self.combo_categoria.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Pagamento:").grid(row=4, column=0, sticky="w")
        metodos_pagamento = self.controller.buscar_metodos_pagamento()
        self.combo_pagamento = ttk.Combobox(
            frame, values=metodos_pagamento, state="readonly"
        )
        self.combo_pagamento.set(pagamento_atual)
        self.combo_pagamento.grid(row=4, column=1, pady=5)

        btn_salvar = ttk.Button(
            self, text="Salvar Alterações", command=self.salvar, bootstyle="success"
        )
        btn_salvar.pack(pady=10)

    def salvar(self):
        nome = self.entry_nome.get()
        valor = self.entry_valor.get()
        tipo = self.combo_tipo.get()
        categoria = self.combo_categoria.get()
        metodo_pagamento = self.combo_pagamento.get()

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número.", parent=self)
            return

        success = self.controller.atualizar_transacao(
            self.id_transacao, nome, valor_float, tipo, categoria, metodo_pagamento
        )

        if success:
            self.on_close()

    def on_close(self):
        self.callback_on_close()
        self.destroy()
