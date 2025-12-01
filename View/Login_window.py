import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk


class LoginWindow(ttk.Toplevel):
    def __init__(self, controller, parent):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.title("Finance")
        self.geometry("400x300")

        self.protocol("WM_DELETE_WINDOW", self.fechar_app)

        ttk.Label(
            self,
            text="Finance Login",
            font=("Arial", 16, "bold"),
            bootstyle="default",
        ).pack(pady=10)

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

        ttk.Button(
            self,
            text="Login",
            command=self.login,
            bootstyle="primary-outline",
        ).pack(pady=10)

        btn_ir_cadastro = ttk.Button(
            self,
            text="Ainda não tem uma conta? Cadastre-se",
            command=self.ir_para_cadastro,
            bootstyle="link",
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

    def fechar_app(self):
        self.parent.destroy()
