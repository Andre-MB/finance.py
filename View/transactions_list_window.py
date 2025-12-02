import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk


class TransactionsListWindow(ttk.Toplevel):
    def __init__(self, parent, controller, dados, callback_on_close):
        super().__init__(parent)
        self.controller = controller
        self.main_window = parent  # Salva a referência da janela principal
        self.callback_on_close = callback_on_close

        self.title("Transações e Análise de Gastos")
        self.geometry("800x600")

        # Atualiza a view principal quando esta janela é fechada
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Resumo financeiro no topo
        mes = parent.meses.index(parent.combo_mes.get()) + 1
        ano = int(parent.combo_ano.get())

        resumo_completo = self.controller.buscar_resumo_financeiro_completo(ano, mes)
        receita = resumo_completo["receita"]
        despesa = resumo_completo["despesa"]
        investimento = resumo_completo["investimento"]
        saldo_restante = receita - despesa - investimento

        frame_resumo = ttk.Frame(self)
        frame_resumo.pack(pady=10, padx=10, fill="x")

        ttk.Label(
            frame_resumo,
            text=f"Total Receitas: R$ {receita:.2f}",
            bootstyle="success",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            frame_resumo,
            text=f"Total Despesas: R$ {despesa:.2f}",
            bootstyle="danger",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            frame_resumo,
            text=f"Total Investido: R$ {investimento:.2f}",
            bootstyle="info",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")

        cor_sobra = "success" if saldo_restante >= 0 else "danger"
        ttk.Label(
            frame_resumo,
            text=f"Saldo Restante: R$ {saldo_restante:.2f}",
            bootstyle=cor_sobra,
            font=("Arial", 14, "bold"),
        ).pack(anchor="w")

        # Tabela de transações
        frame_tabela = ttk.Frame(self)
        frame_tabela.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        colunas_visiveis = ("Nome", "Valor", "Categoria", "Pagamento", "Data")
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)

        self.tree = ttk.Treeview(
            frame_tabela, columns=colunas_visiveis, show="headings"
        )

        for col in colunas_visiveis:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        for row in dados:
            self.tree.insert("", tk.END, iid=row[0], values=row[1:])

        self.tree.pack(expand=True, fill="both")

        # Botões de ação
        btn_edit = ttk.Button(
            frame_tabela,
            text="Editar Transação",
            bootstyle="warning",
            command=self.abrir_janela_editar,
        )
        btn_edit.pack(side="left", padx=10, pady=10)

        btn_delete = ttk.Button(
            frame_tabela,
            text="Deletar Transação",
            bootstyle="danger-outline",
            command=self.deletar_transacao,
        )
        btn_delete.pack(side="left", padx=10, pady=10)

    def deletar_transacao(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning(
                "Aviso", "Selecione uma transação para deletar.", parent=self
            )
            return

        id_transacao = selecionado[0]
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir esta transação?", parent=self
        ):
            self.controller.deletar_transacao(id_transacao)
            self.tree.delete(selecionado[0])
            messagebox.showinfo("Sucesso", "Transação excluída!", parent=self)
            self.on_close()  # Fecha e atualiza a main window

    def abrir_janela_editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning(
                "Aviso", "Selecione uma transação para editar.", parent=self
            )
            return
        id_transacao = selecionado[0]
        # Chama o método da MainWindow para abrir a janela de edição
        self.main_window.abrir_janela_editar(id_transacao)
        self.on_close()

    def on_close(self):
        self.callback_on_close()
        self.destroy()
