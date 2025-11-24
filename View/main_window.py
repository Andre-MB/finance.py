import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainWindow(ttk.Toplevel):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent)
        self.controller = controller
        self.usuario = usuario
        self.title("Finance")
        self.parent = parent
        self.geometry("1200x800")

        self.protocol("WM_DELETE_WINDOW", self.fechar_app)

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Label(
            header_frame,
            text=f"Bem-vindo, {self.usuario['name']}!",
            font=("Arial", 14),
        ).pack(side="left")

        btn_logout = ttk.Button(
            header_frame,
            text="Sair",
            command=self.logout,
            bootstyle="danger-outline",
        )
        btn_logout.pack(side="right")

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        main_frame.grid_columnconfigure(0, weight=45)
        main_frame.grid_columnconfigure(1, weight=55)
        main_frame.grid_rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        data_atual = date.today()
        mes_atual = data_atual.month

        frame_data = ttk.Frame(self.left_frame)
        frame_data.pack(pady=10)

        ttk.Label(frame_data, text="Mês:").grid(row=0, column=0, padx=5)

        self.meses = [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]
        self.combo_mes = ttk.Combobox(frame_data, values=self.meses, state="readonly")
        self.combo_mes.set(self.meses[mes_atual - 1])
        self.combo_mes.grid(row=0, column=1, padx=5)

        ttk.Label(frame_data, text="Ano:").grid(row=0, column=2, padx=5)

        self.combo_ano = ttk.Combobox(
            frame_data, values=[2024, 2025, 2026], state="readonly"
        )
        self.combo_ano.set("2025")
        self.combo_ano.grid(row=0, column=3, padx=5)

        self.label_saldo = ttk.Label(
            self.left_frame,
            text="Saldo: R$ 0.00",
            font=("Arial", 12, "bold"),
        )
        self.label_saldo.pack(pady=10, anchor="w")

        self.label_receita = ttk.Label(
            self.left_frame,
            text="Receitas: R$ 0.00",
            bootstyle="success",
            font=("Arial", 10),
        )
        self.label_receita.pack(pady=2, anchor="w")

        self.label_despesa = ttk.Label(
            self.left_frame,
            text="Despesas: R$ 0.00",
            bootstyle="danger",
            font=("Arial", 10),
        )
        self.label_despesa.pack(pady=2, anchor="w")

        self.label_investido = ttk.Label(
            self.left_frame,
            text="Investido: R$ 0.00",
            bootstyle="info",
            font=("Arial", 10),
        )
        self.label_investido.pack(pady=2, anchor="w")

        self.combo_mes.bind("<<ComboboxSelected>>", self.atualizar_valores)
        self.combo_ano.bind("<<ComboboxSelected>>", self.atualizar_valores)

        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(pady=10)

        self.btn_buscar = ttk.Button(
            button_frame,
            text="Ver Transações",
            command=self.buscar_dados,
        )
        self.btn_buscar.pack(side="left", padx=5)

        self.btn_adicionar = ttk.Button(
            button_frame,
            text="Adicionar Transação",
            command=self.abrir_janela_adicionar,
        )
        self.btn_adicionar.pack(side="left", padx=5)

        self.progress_bars_frame = ttk.Frame(self.left_frame)
        self.progress_bars_frame.pack(pady=(20, 0), fill="x")

        self.atualizar_valores(None)

    def fechar_app(self):
        self.parent.destroy()

    def logout(self):
        self.controller.logout()

    def buscar_dados(self):
        mes = self.meses.index(self.combo_mes.get()) + 1
        ano = int(self.combo_ano.get())
        self.controller.buscar_dados_do_banco(mes, ano)

    def exibir_dados(self, dados):
        janela = ttk.Toplevel(self)
        janela.title("Transações e Análise de Gastos")
        janela.geometry("800x600")

        mes = self.meses.index(self.combo_mes.get()) + 1
        ano = int(self.combo_ano.get())

        resumo_completo = self.controller.buscar_resumo_financeiro_completo(ano, mes)
        receita = resumo_completo["receita"]
        despesa = resumo_completo["despesa"]
        investimento = resumo_completo["investimento"]

        # Calcula a sobra líquida conforme solicitado
        saldo_restante = receita - despesa - investimento

        frame_resumo = ttk.Frame(janela)
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

        frame_tabela = ttk.Frame(janela)
        frame_tabela.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        colunas_visiveis = ("Nome", "Valor", "Categoria", "Pagamento", "Data")

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)

        tree = ttk.Treeview(frame_tabela, columns=colunas_visiveis, show="headings")

        for col in colunas_visiveis:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for row in dados:
            tree.insert("", tk.END, iid=row[0], values=row[1:])

        tree.pack(expand=True, fill="both")

        def deletar_transacao():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma transação para deletar.")
                return

            id_transacao = selecionado[0]

            confirmar = messagebox.askyesno(
                "Confirmar", "Deseja realmente excluir esta transação?"
            )

            if confirmar:
                self.controller.deletar_transacao(id_transacao)
                tree.delete(selecionado[0])
                messagebox.showinfo("Sucesso", "Transação excluída!")
                self.atualizar_valores(None)

        btn_edit = ttk.Button(
            frame_tabela,
            text="Editar Transação",
            bootstyle="warning",
            command=lambda: self.abrir_janela_editar(tree),
        )
        btn_edit.pack(side="left", padx=10, pady=10)

        btn_delete = ttk.Button(
            frame_tabela,
            text="Deletar Transação",
            bootstyle="danger-outline",
            command=deletar_transacao,
        )
        btn_delete.pack(side="left", padx=10, pady=10)

    def _deletar_transacao_selecionada(self, tree):
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma transação para deletar.")
            return

    def abrir_janela_adicionar(self):
        janela_add = ttk.Toplevel(self)
        janela_add.title("Nova Transação")
        janela_add.geometry("400x350")

        frame = ttk.Frame(janela_add)
        frame.pack(pady=20, padx=20)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        entry_nome = ttk.Entry(frame)
        entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Valor (R$):").grid(row=1, column=0, sticky="w")
        entry_valor = ttk.Entry(frame)
        entry_valor.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky="w")
        tipos_transacao = [
            "Receita",
            "Despesa",
            "Investimento",
        ]
        tipos_transacao = self.controller.buscar_tipos()
        combo_tipo = ttk.Combobox(frame, values=tipos_transacao, state="readonly")
        combo_tipo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Categoria:").grid(row=3, column=0, sticky="w")
        categorias = self.controller.buscar_categorias()
        combo_categoria = ttk.Combobox(frame, values=categorias, state="readonly")
        combo_categoria.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Pagamento:").grid(row=4, column=0, sticky="w")
        metodos_pagamento = self.controller.buscar_metodos_pagamento()
        combo_pagamento = ttk.Combobox(
            frame, values=metodos_pagamento, state="readonly"
        )
        combo_pagamento.grid(row=4, column=1, pady=5)

        def on_tipo_selected(event):
            tipo_selecionado = combo_tipo.get()
            if tipo_selecionado == "Investimento":
                combo_categoria.set("Outros")

                combo_categoria.config(state="disabled")
            else:
                combo_categoria.config(state="readonly")
                if tipo_selecionado == "Despesa":
                    combo_categoria.set("")

        combo_tipo.bind("<<ComboboxSelected>>", on_tipo_selected)

        btn_salvar = ttk.Button(
            janela_add,
            text="Salvar",
            command=lambda: self.salvar_transacao(
                janela_add,
                entry_nome.get(),
                entry_valor.get(),
                combo_tipo.get(),
                combo_categoria.get(),
                combo_pagamento.get(),
            ),
            bootstyle="success",
        )
        btn_salvar.pack(pady=10)

    def salvar_transacao(
        self, janela_para_fechar, nome, valor, tipo, categoria, metodo_pagamento
    ):
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

        self.controller.adicionar_transacao(
            nome, valor_float, tipo, categoria, metodo_pagamento
        )

        janela_para_fechar.destroy()

    def abrir_janela_editar(self, tree):
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma transação para editar.")
            return

        id_transacao = selecionado[0]

        dados_transacao = self.controller.buscar_transacao_por_id(id_transacao)
        if not dados_transacao:
            messagebox.showerror(
                "Erro", "Não foi possível carregar os dados da transação."
            )
            return

        (
            nome_atual,
            valor_atual,
            tipo_atual,
            categoria_atual,
            pagamento_atual,
        ) = dados_transacao

        janela_edit = ttk.Toplevel(self)
        janela_edit.title("Editar Transação")
        janela_edit.geometry("400x300")

        frame = ttk.Frame(janela_edit)
        frame.pack(pady=20, padx=20)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        entry_nome = ttk.Entry(frame)
        entry_nome.insert(0, nome_atual)
        entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Valor (R$):").grid(row=1, column=0, sticky="w")
        entry_valor = ttk.Entry(frame)
        entry_valor.insert(0, f"{valor_atual:.2f}")
        entry_valor.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky="w")
        tipos_transacao = self.controller.buscar_tipos()
        combo_tipo = ttk.Combobox(frame, values=tipos_transacao, state="readonly")
        combo_tipo.set(tipo_atual)
        combo_tipo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Categoria:").grid(row=3, column=0, sticky="w")
        categorias = self.controller.buscar_categorias()
        combo_categoria = ttk.Combobox(frame, values=categorias, state="readonly")
        combo_categoria.set(categoria_atual)
        combo_categoria.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Pagamento:").grid(row=4, column=0, sticky="w")
        metodos_pagamento = self.controller.buscar_metodos_pagamento()
        combo_pagamento = ttk.Combobox(
            frame, values=metodos_pagamento, state="readonly"
        )
        combo_pagamento.set(pagamento_atual)
        combo_pagamento.grid(row=4, column=1, pady=5)

        btn_salvar = ttk.Button(
            janela_edit,
            text="Salvar Alterações",
            command=lambda: self.salvar_edicao(
                janela_edit,
                id_transacao,
                entry_nome.get(),
                entry_valor.get(),
                combo_tipo.get(),
                combo_categoria.get(),
                combo_pagamento.get(),
            ),
            bootstyle="success",
        )
        btn_salvar.pack(pady=10)

    def salvar_edicao(
        self,
        janela_para_fechar,
        id_transacao,
        nome,
        valor,
        tipo,
        categoria,
        metodo_pagamento,
    ):
        valor_float = float(valor)
        self.controller.atualizar_transacao(
            id_transacao, nome, valor_float, tipo, categoria, metodo_pagamento
        )
        janela_para_fechar.destroy()

    def atualizar_valores(self, event):
        mes = self.meses.index(self.combo_mes.get()) + 1
        ano = int(self.combo_ano.get())

        resumo_completo = self.controller.buscar_resumo_financeiro_completo(ano, mes)

        receita = resumo_completo["receita"]
        despesa = resumo_completo["despesa"]
        investimento = resumo_completo["investimento"]
        gastos_por_categoria = resumo_completo["gastos_por_categoria"]
        investimentos_por_categoria = resumo_completo["investimentos_por_categoria"]

        self.label_receita.config(text=f"Receitas: R$ {receita:.2f}")
        self.label_despesa.config(text=f"Despesas: R$ {despesa:.2f}")
        self.label_investido.config(text=f"Investido: R$ {investimento:.2f}")

        saldo = receita - despesa - investimento
        self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")

        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.progress_bars_frame.winfo_children():
            widget.destroy()

        labels_grafico = []
        valores_grafico = []
        cores_grafico = []

        if receita > 0:
            sobra = receita - despesa - investimento

            if despesa > 0:
                labels_grafico.append("Despesas")
                valores_grafico.append(despesa)
                cores_grafico.append("#F44336")

            if investimento > 0:
                labels_grafico.append("Investimentos")
                valores_grafico.append(investimento)
                cores_grafico.append("#2196F3")  # Azul

            if sobra > 0:
                labels_grafico.append("Sobra")
                valores_grafico.append(sobra)
                cores_grafico.append("#4CAF50")

            style = ttk.Style()
            bg_color = style.lookup("TFrame", "background")
            fig = Figure(figsize=(4, 3.5), dpi=100, facecolor=bg_color)
            ax = fig.add_subplot(111)

            wedges, texts, autotexts = ax.pie(
                valores_grafico,
                autopct="%1.1f%%",
                startangle=140,
                colors=cores_grafico,
                textprops=dict(color="w"),
            )

            for autotext in autotexts:
                autotext.set_color("black")

            ax.legend(
                wedges,
                labels_grafico,
                title="Fluxo Financeiro",
                title_fontsize="small",
                loc="lower center",
                bbox_to_anchor=(0.5, -0.3),
                ncol=len(labels_grafico),
                prop={"size": 8},
            )
            ax.axis("equal")
            fig.suptitle(
                f"Distribuição da Receita (R$ {receita:.2f})",
                color="white",
                fontsize=12,
            )
            fig.tight_layout(
                pad=2.0
            )  # Ajusta o layout para garantir que a legenda não seja cortada

            # Cria o canvas do Tkinter para exibir o gráfico
            canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(
                self.right_frame,
                text="Nenhum dado financeiro para exibir no gráfico.",
                font=("Arial", 12),
            ).pack(expand=True)

        frame_gastos_categoria = ttk.Frame(self.progress_bars_frame)
        frame_gastos_categoria.pack(pady=(0, 20), fill="x")

        ttk.Label(
            frame_gastos_categoria,
            text="Gastos por Categoria (em relação à Receita)",
            font=("Arial", 12, "bold"),
        ).pack()

        if gastos_por_categoria and receita > 0:
            for categoria, gasto_total in sorted(
                gastos_por_categoria, key=lambda item: item[1], reverse=True
            ):
                percentual = (gasto_total / receita) * 100

                frame_linha = ttk.Frame(frame_gastos_categoria)
                frame_linha.pack(fill="x", pady=2)

                label_texto = f"{categoria}: R$ {gasto_total:.2f} ({percentual:.1f}%)"
                ttk.Label(frame_linha, text=label_texto, anchor="w").pack(
                    side="top", fill="x"
                )

                progress = ttk.Progressbar(
                    frame_linha,
                    orient="horizontal",
                    mode="determinate",
                    bootstyle="danger",
                )
                progress["value"] = percentual
                progress.pack(side="bottom", fill="x")
        else:
            ttk.Label(
                frame_gastos_categoria,
                text="Sem despesas para analisar.",
            ).pack()

        ttk.Label(
            frame_gastos_categoria,
            text="Investimentos (em relação à Receita)",
            font=("Arial", 12, "bold"),
        ).pack(pady=(20, 0))

        if investimentos_por_categoria and receita > 0:
            for categoria, investimento_total in sorted(
                investimentos_por_categoria, key=lambda item: item[1], reverse=True
            ):
                percentual = (investimento_total / receita) * 100

                frame_linha = ttk.Frame(frame_gastos_categoria)
                frame_linha.pack(fill="x", pady=2)

                label_texto = (
                    f"{categoria}: R$ {investimento_total:.2f} ({percentual:.1f}%)"
                )
                ttk.Label(frame_linha, text=label_texto, anchor="w").pack(
                    side="top", fill="x"
                )

                progress = ttk.Progressbar(
                    frame_linha,
                    orient="horizontal",
                    mode="determinate",
                    bootstyle="info",
                )
                progress["value"] = percentual
                progress.pack(side="bottom", fill="x")
        else:
            ttk.Label(
                frame_gastos_categoria,
                text="Sem investimentos para analisar.",
            ).pack()
