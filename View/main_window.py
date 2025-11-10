import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, controller, usuario):
        super().__init__()
        self.controller = controller
        self.usuario = usuario
        self.title("Finance")
        self.geometry("400x300")
        
        self.label = tk.Label(self, text="Finance")
        self.label.pack(pady=10)

        tk.Label(self, text=f"Bem-vindo, {self.usuario['name']}!", font=("Arial", 14)).pack(pady=20)

        self.btn_buscar = tk.Button(self, text="Transações", command=self.buscar_dados)
        self.btn_buscar.pack(pady=5)

    def buscar_dados(self):
        self.controller.buscar_dados_do_banco()

    def exibir_dados(self, dados):

        janela = tk.Toplevel()
        janela.title("Transações")

        colunas = ("Nome", "Valor", "Data")
        tree = ttk.Treeview(janela, columns=colunas, show="headings")

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for row in dados:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill="both")
            
