import os
from tkinter import messagebox
import ttkbootstrap as ttk
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet
from Utils.cpf_validation import validar_cpf
from Controller.main_controller import MainController
from Model.database import Database
from View.Register_window import RegisterWindow
from View.Login_window import LoginWindow
from View.main_window import MainWindow

# Carrega a chave de criptografia do .env
load_dotenv()
chave = os.getenv("FERNET_KEY")

if not chave:
    chave = Fernet.generate_key().decode()
    set_key(".env", "FERNET_KEY", chave)
    print("🔐 Nova chave criada e salva no arquivo .env")

fernet = Fernet(chave.encode())


class MainUserController:
    def __init__(self):
        db_password = os.getenv("DB_PASSWORD")
        self.db = Database(
            host="ep-soft-feather-a4ymlnb0-pooler.us-east-1.aws.neon.tech",
            database="neondb",
            user="neondb_owner",
            password=db_password,
        )
        self.db.connect()

        self.root = ttk.Window(themename="darkly")
        self.root.withdraw()
        self.current_window = None

    def iniciar_app(self):
        self.abrir_janela_login()
        self.root.mainloop()

    # Cadastra um novo usuário no banco
    def cadastrar_usuario(self, name, email, senha, cpf):
        if not validar_cpf(cpf):
            messagebox.showerror("Erro de Validação", "O CPF informado é inválido.")
            return

        senha_cripto = fernet.encrypt(senha.encode()).decode()

        query = """
        INSERT INTO "Users" ("name", "email", "senha", "cpf")
        VALUES (%s, %s, %s, %s)
        """

        try:
            self.db.execute_query(query, (name, email, senha_cripto, cpf))
            print("✅ Usuário cadastrado com sucesso!")
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.abrir_janela_login()
        except Exception as e:
            print("❌ Erro ao cadastrar usuário:", e)
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    def abrir_janela_cadastro(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = RegisterWindow(self, self.root)

    def abrir_janela_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginWindow(self, self.root)

    # Valida o login do usuário
    def login(self, email, senha):
        query = """SELECT "idUser", "name", "email", "senha" FROM "Users" WHERE "email" = %s"""
        user_data = self.db.fetch_one(query, (email,))

        if not user_data:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        idUser, name, email, senha_cripto = user_data
        senha_armazenada = fernet.decrypt(senha_cripto.encode()).decode()

        if senha == senha_armazenada:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {name}!")

            usuario = {"idUser": idUser, "name": name, "email": email}

            if self.current_window:
                self.current_window.destroy()

            main_controller = MainController(self, self.root, usuario)
            main_controller.iniciar_app()

        else:
            messagebox.showerror("Erro", "Senha incorreta.")

    def reiniciar_para_login(self):
        self.abrir_janela_login()
