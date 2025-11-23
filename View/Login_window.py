import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk


class LoginWindow(ttk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Finance")
        self.geometry("400x300")

        # Título
        ttk.Label(
            self,
            text="Finance Login",
            font=("Arial", 16, "bold"),
            bootstyle="default",
        ).pack(pady=10)

        # Frame central para organizar os campos
        frame = ttk.Frame(self, bootstyle="default")
        frame.pack(pady=20)

        ttk.Label(frame, text="Email:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Senha:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_senha = ttk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        # Botão de Login
        ttk.Button(
            self,
            text="Login",
            command=self.login,
            bootstyle="primary-outline",  # Estilo do botão
        ).pack(pady=10)

        # Botão para ir para a tela de cadastro
        btn_ir_cadastro = ttk.Button(
            self,
            text="Ainda não tem uma conta? Cadastre-se",
            command=self.ir_para_cadastro,
            bootstyle="link",  # Estilo de link
            cursor="hand2",
        )
        btn_ir_cadastro.pack(pady=5)

    def login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        self.controller.login(email, senha)

    def ir_para_cadastro(self):
        self.controller.abrir_janela_cadastro()
