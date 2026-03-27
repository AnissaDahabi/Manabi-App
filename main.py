import sys
from PySide6.QtWidgets import QApplication

from gui.login_window import LoginWindow
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    with open("assets/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    login = LoginWindow(on_success=lambda user: ouvrir_app(app, login, user))
    login.show()

    sys.exit(app.exec())


def ouvrir_app(app, login, user):
    login.close()
    window = MainWindow(user)
    window.show()
    app._main_window = window


if __name__ == "__main__":
    main()