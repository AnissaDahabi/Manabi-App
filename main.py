import sys
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

def load_stylesheet(app):
    try:
        with open("assets/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Erreur : Le fichier style.qss est introuvable.")
    except Exception as e:
        print(f"Erreur lors du chargement du style : {e}")

def main():
    app = QApplication(sys.argv)
    load_stylesheet(app)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()