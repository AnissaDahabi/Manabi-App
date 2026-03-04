
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




def supprimer_mot():
    pass



def editer_mot():
    pass


