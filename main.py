from gestion_bdd import afficher_mots
from gestion_bdd import ajouter_mot
from gestion_bdd import supprimer_mot
from gestion_bdd import modifier_mot

# main.py

# boucle principale
while True:
    print("\n --- Menu ---")
    print("1. Afficher les mots")
    print("2. Ajouter un mot")
    print("3. Supprimer un mot")
    print("4. Modifier un mot")
    print("0. Quitter")
    choix = input("Entrez votre choix : ")

    if choix == "1":
        afficher_mots()
    elif choix == "2":
        ajouter_mot()
    elif choix == "3":
        supprimer_mot()
    elif choix == "4":
        modifier_mot()
    elif choix == "0":
        print("Au revoir !")
        break
    else:
        print("Choix invalide, veuillez réessayer.")


# afficher menu

# 1 -> ajouter_mot()

# 2 -> supprimer_mot()

# 3 -> modifier_mot()

# 4 -> afficher_mots()

# 0 -> quitter