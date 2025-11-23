import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk


class RegisterWindow(ttk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Finance")
        self.geometry("600x500")

        # Título
        ttk.Label(self, text="Cadastro de Usuário", font=("Arial", 16, "bold")).pack(
            pady=10
        )

        # Frame central para organizar os campos
        frame = ttk.Frame(self)
        frame.pack(pady=20)

        # Campos de entrada
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Senha:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_senha = ttk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_cpf = ttk.Entry(frame)
        self.entry_cpf.grid(row=3, column=1, padx=5, pady=5)

        # Botão de cadastro
        ttk.Button(
            self, text="Cadastrar", command=self.cadastrar, bootstyle="success"
        ).pack(pady=10)

        # Botão para voltar para a tela de login
        btn_voltar_login = ttk.Button(
            self,
            text="Já tem uma conta? Faça o login",
            command=self.voltar_para_login,
            bootstyle="link",
            cursor="hand2",
        )
        btn_voltar_login.pack(pady=5)

    def cadastrar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        cpf = self.entry_cpf.get()

        if not nome or not email or not senha or not cpf:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        self.controller.cadastrar_usuario(nome, email, senha, cpf)

    def voltar_para_login(self):
        self.controller.abrir_janela_login()
