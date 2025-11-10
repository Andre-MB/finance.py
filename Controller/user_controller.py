import os
from tkinter import messagebox
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet
from Controller.main_controller import MainController
from Model.database import Database
from View.Register_window import RegisterWindow
from View.Login_window import LoginWindow
from View.main_window import MainWindow

# === Carregar chave de criptografia ===
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

        # self.view = RegisterWindow(self)
        self.view = LoginWindow(self)

    def iniciar_app(self):
        self.view.mainloop()

    # === Função para cadastrar usuário ===
    def cadastrar_usuario(self, name, email, senha, cpf):
        senha_cripto = fernet.encrypt(senha.encode()).decode()

        query = '''
        INSERT INTO "Users" ("name", "email", "senha", "cpf")
        VALUES (%s, %s, %s, %s)
        '''

        try:
            self.db.execute_query(query, (name, email, senha_cripto, cpf))
            print("✅ Usuário cadastrado com sucesso!")
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except Exception as e:
            print("❌ Erro ao cadastrar usuário:", e)
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")



    # === Função de login ===
    def login(self, email, senha):
        query = '''SELECT "idUser", "name", "email", "senha" FROM "Users" WHERE "email" = %s'''
        user_data = self.db.fetch_one(query, (email,))

        if not user_data:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return
        
        idUser, name, email, senha_cripto = user_data
        senha_armazenada = fernet.decrypt(senha_cripto.encode()).decode()

        # senha_armazenada_cripto = user_data[0]
        # senha_armazenada = fernet.decrypt(senha_armazenada_cripto.encode()).decode()

        if senha == senha_armazenada:
            messagebox.showinfo("Sucesso",  f"Bem-vindo, {name}!")

            usuario = {
            "idUser": idUser,
            "name": name,
            "email": email
            }

            self.view.destroy()       

            main_controller = MainController(usuario)
            main_controller.iniciar_app()

            # MainWindow(self, usuario).mainloop() 
        else:
            messagebox.showerror("Erro", "Senha incorreta.")
            

