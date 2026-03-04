import sqlite3
from vue import afficher_menu
from services import traiter_choix
from gestion_bdd import initialiser_bdd

# main.py
initialiser_bdd()
connexion = sqlite3.connect("manabi.db")
curseur = connexion.cursor()

# boucle principale
while True:
    afficher_menu()
    choix = input("Entrez votre choix: ")
    if not traiter_choix(choix, curseur, connexion):
        break
connexion.commit()
connexion.close()