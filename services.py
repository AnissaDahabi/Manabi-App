from gestion_bdd import afficher_mots, ajouter_mot, supprimer_mot, modifier_mot

def traiter_choix(choix,curseur,connexion):
    if choix == "1":
        afficher_mots(curseur, connexion)
    elif choix == "2":
        ajouter_mot(curseur, connexion)
    elif choix == "3":
        supprimer_mot(curseur, connexion)
    elif choix == "4":
        modifier_mot(curseur, connexion)
    elif choix == "0":
        print("Au revoir !")
        return False
    else:
        print("Choix invalide, veuillez réessayer.")
    return True