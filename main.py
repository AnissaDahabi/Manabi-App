from gestion_bdd import afficher_mots

# main.py

# boucle principale
while True:
    print("\n --- Menu ---")
    print("1. Afficher les mots")
    print("0. Quitter")
    choix = input("Entrez votre choix : ")

    if choix == "1":
        afficher_mots()
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