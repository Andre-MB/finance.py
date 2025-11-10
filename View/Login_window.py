import tkinter as tk
from tkinter import messagebox

class LoginWindow(tk.Tk):
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

        tk.Label(frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Senha:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        # Botão de cadastro
        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if  not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        
        self.controller.login(email, senha)
