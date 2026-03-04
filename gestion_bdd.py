
mots = [
    {
        "kanji" : "漢字",
        "lecture" : "かんじ",
        "traduction" : "caractères chinois utilisés en japonais",
        "exemple" : "日本語の漢字は難しいです。",
        "traduction_exemple" : "Les kanjis japonais sont difficiles.",
        "niveau" : "N5"
    },
    {
        "kanji" : "猫",
        "lecture" : "ねこ",
        "traduction" : "chat",
        "exemple" : "私は猫が好きです。",
        "traduction_exemple" : "J'aime les chats.",
        "niveau" : "N5"
    },
{
        "kanji" : "test",
        "lecture" : "test",
        "traduction" : "test",
        "exemple" : "私は猫が好きです。",
        "traduction_exemple" : "J'aime les chats.",
        "niveau" : "N5"
    }
]

def afficher_mots():
    if not mots:
        print("La base de données est vide pour l'instant.")
    else:
        print("Voici les mots de la base de données :")
        for mot in mots:
            print(mot)

def ajouter_mot():
    input_kanji = input("Entrez le kanji à ajouter:")
    input_lecture = input("Entrez la lecture du kanji:")
    input_traduction = input("Entrez la traduction du kanii:")
    input_exemple = input("Entrez une phrase d'exemple:")
    input_tradexemple = input("Entrez la traduction de la phrase d'exemple:")
    input_niveau = input("Entrez le niveau JLPT du kanji:")

    nouveau_mot = {
        "kanji" : input_kanji,
        "lecture" : input_lecture,
        "traduction" : input_traduction,
        "exemple" : input_exemple,
        "traduction_exemple" : input_tradexemple,
        "niveau" : input_niveau
    }

    mots.append(nouveau_mot)

    print(f"Le kanji {input_kanji} a bien été ajouté à la base de données!")


def supprimer_mot():
    if not mots:
        print("La base de données est vide, aucun mot à supprimer.")
        return

    for i, mot in enumerate(mots, start = 1):
        print(f"{i}. {mot['kanji']} ({mot['lecture']} - {mot['traduction']})")

    num = int(input("Entrez le numéro du mot à supprimer: "))
    if 1 <= num <= len(mots):
        mot_supprime = mots.pop(num - 1)
        print(f"Le mot {mot_supprime['kanji']} a été supprimé")


def modifier_mot():
    if not mots:
        print("La base de données est vide, aucun mot à modifier.")
        return

    for i, mot in enumerate(mots, start = 1):
        print(f"{i}. {mot['kanji']} ({mot['lecture']} - {mot['traduction']})")


    num = int(input("Entrez le numéro du mot à modifier: "))
    if 1 <= num <= len(mots):
        mot_choisi = mots[num - 1]

        while True:
            for j,  cle in enumerate(mot_choisi.keys(), start = 1):
                print(f"{j}. {cle} : {mot_choisi[cle]}")

            liste_cles = list(mot_choisi.keys())

            choix = int(input("Choisissez la valeur à modifier: "))

            if 1 <= choix <= len(liste_cles):
                cle_a_editer = liste_cles[choix - 1]
                nouvelle_valeur = input("Nouvelle valeur: ")
                mot_choisi[cle_a_editer] = nouvelle_valeur
                print("Valeur modifiée avec succès!")
            else:
                print("Choix invalide.")

            continuer = input("Modifier une autre valeur? (o/n): ")
            if continuer.lower() == "n":
                break
