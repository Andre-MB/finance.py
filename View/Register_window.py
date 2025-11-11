import tkinter as tk
from tkinter import messagebox


class RegisterWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Finance")
        self.geometry("600x500")

        # Título
        tk.Label(self, text="Finance", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame central para organizar os campos
        frame = tk.Frame(self)
        frame.pack(pady=20)

        # Campos de entrada
        tk.Label(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Senha:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="CPF:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_cpf = tk.Entry(frame)
        self.entry_cpf.grid(row=3, column=1, padx=5, pady=5)

        # Botão de cadastro
        tk.Button(self, text="Cadastrar", command=self.cadastrar).pack(pady=10)

    def cadastrar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        cpf = self.entry_cpf.get()

        if not nome or not email or not senha or not cpf:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        self.controller.cadastrar_usuario(nome, email, senha, cpf)
