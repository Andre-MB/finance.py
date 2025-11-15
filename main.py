from Controller.main_controller import MainController
from Controller.user_controller import MainUserController


if __name__ == "__main__":
    usuario = {"idUser": "b6688b8a-1912-4e42-827e-c367bc467e6f", "name": "Andre", "email": "andre@gmail.com"}
    app = MainController(usuario)

    app.iniciar_app()