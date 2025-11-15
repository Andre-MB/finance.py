import tkinter as tk
from tkinter import messagebox


class LoginWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Finance")
        self.geometry("400x300")

        # Cores do Dark Mode
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"
        entry_bg = "#3E3E3E"

        # Configurar a cor de fundo da janela principal
        self.config(bg=bg_color)

        # Título
        tk.Label(
            self,
            text="Finance Login",
            font=("Arial", 16, "bold"),
            bg=bg_color,
            fg=fg_color,
        ).pack(pady=10)

        # Frame central para organizar os campos
        frame = tk.Frame(self, bg=bg_color)
        frame.pack(pady=20)

        tk.Label(frame, text="Email:", bg=bg_color, fg=fg_color).grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_email = tk.Entry(
            frame, bg=entry_bg, fg=fg_color, insertbackground=fg_color
        )
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Senha:", bg=bg_color, fg=fg_color).grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_senha = tk.Entry(
            frame, show="*", bg=entry_bg, fg=fg_color, insertbackground=fg_color
        )
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        # Botão de Login
        tk.Button(
            self,
            text="Login",
            command=self.login,
            bg="#007BFF",
            fg=fg_color,
            relief="flat",
        ).pack(pady=10)

        # Botão para ir para a tela de cadastro
        btn_ir_cadastro = tk.Button(
            self,
            text="Ainda não tem uma conta? Cadastre-se",
            command=self.ir_para_cadastro,
            bg=bg_color,
            fg="#007BFF",
            relief="flat",
            bd=0,
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
