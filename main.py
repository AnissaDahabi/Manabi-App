import sqlite3
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from vue import afficher_menu
from services import traiter_choix
from gestion_bdd import initialiser_bdd

# main.py
initialiser_bdd()
connexion = sqlite3.connect("manabi.db")
curseur = connexion.cursor()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

# boucle principale
while True:
    afficher_menu()
    choix = input("Entrez votre choix: ")
    if not traiter_choix(choix, curseur, connexion):
        break
connexion.commit()
connexion.close()