from Controller.main_controller import MainController
from Controller.user_controller import MainUserController
import ttkbootstrap as ttk


if __name__ == "__main__":
    # O código abaixo serve para pular a tela de login durante o desenvolvimento.
    # Descomente este bloco e comente a linha 'app = MainUserController()' para usar.
    usuario = {
        "idUser": "e9351531-2244-4b11-a3c0-1e0f1e745939",
        "name": "Filipe",
        "email": "filipe@gmail.com",
    }
    app = MainController(usuario)

    # Inicia o fluxo normal da aplicação pela tela de login.
    # app = MainUserController()
    app.iniciar_app()
