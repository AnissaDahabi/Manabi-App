import sqlite3

def initialiser_bdd():
    connexion = sqlite3.connect("manabi.db")
    curseur = connexion.cursor()

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS mots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji TEXT,
        lecture TEXT,
        traduction TEXT,
        exemple TEXT,
        traduction_exemple TEXT,
        niveau TEXT,
        prochaine_revision DATETIME,
        intervalle INTEGER,
        repetitions INTEGER
    )
    """)

    connexion.commit()
    connexion.close()
    print("Base de données initialisée avec succès !")


def afficher_mots(curseur, connexion):
    curseur.execute("SELECT * FROM mots")
    mots = curseur.fetchall()

    for mot in mots:
        print(f"{mot[0]}. {mot[1]} ({mot[2]} - {mot[3]})")
        print(f"   Exemple : {mot[4]}")
        print(f"   Traduction : {mot[5]}")
        print(f"   Niveau : {mot[6]}")
        print(f"   Prochaine révision : {mot[7]}")
        print(f"   Intervalle : {mot[8]} minutes, Répétitions : {mot[9]}")
        print("-" * 40)


def ajouter_mot(curseur, connexion):
    kanji = input("Entrez le kanji à ajouter:")
    lecture = input("Entrez la lecture du kanji:")
    traduction = input("Entrez la traduction du kanii:")
    exemple = input("Entrez une phrase d'exemple:")
    traduction_exemple = input("Entrez la traduction de la phrase d'exemple:")
    niveau = input("Entrez le niveau JLPT du kanji:")

    curseur.execute("""
            INSERT INTO mots
            (kanji, lecture, traduction, exemple, traduction_exemple, niveau, prochaine_revision, intervalle, repetitions)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)
        """, (kanji, lecture, traduction, exemple, traduction_exemple, niveau, 0, 0))

    connexion.commit()
    print(f"Le mot {kanji} a bien été ajouté à la base de données!")


def supprimer_mot(curseur, connexion):
    curseur.execute("SELECT * FROM mots")
    mots = curseur.fetchall()

    if not mots:
        print("La base de données est vide !")
        return

    for mot in mots:
        print(f"{mot[0]}. {mot[1]} ({mot[2]} - {mot[3]})")

    mot_id = int(input("Entrez l'id du mot à supprimer: "))

    curseur.execute("DELETE FROM mots WHERE id = ?", (mot_id,))
    connexion.commit()
    print("Mot supprimé avec succès!")


def modifier_mot(curseur, connexion):
    curseur.execute("SELECT * FROM mots")
    mots = curseur.fetchall()

    if not mots:
        print("La base de données est vide !")
        return

    for mot in mots:
        print(f"{mot[0]}. {mot[1]} ({mot[2]} - {mot[3]})")

    mot_id = int(input("Entrez l'id du mot à modifier: "))

    curseur.execute("SELECT * FROM mots WHERE id = ?", (mot_id,))
    mot = curseur.fetchone()

    colonnes = ["id", "kanji", "lecture", "traduction", "exemple", "traduction_exemple", "niveau"]

    while  True:
        for i, col in enumerate(colonnes[1:7], start=1):
            print(f"{i}. {col} : {mot[i]}")

        choix_col = int(input("Entrez le numéro du champ à modifier: "))
        if 1 <= choix_col <= len(colonnes) - 1:
            cle_a_editer = colonnes[choix_col]
            nouvelle_valeur = input(f"Nouvelle valeur pour {cle_a_editer} : ")

            curseur.execute(f"UPDATE mots SET {cle_a_editer} = ? WHERE id = ?", (nouvelle_valeur, mot_id))
            connexion.commit()
            curseur.execute("SELECT * FROM mots WHERE id = ?", (mot_id,))
            mot = curseur.fetchone()

            print(f"{cle_a_editer} modifié avec succès!")
        else:
            print("Choix invalide.")

        continuer = input("Voulez-vous modifier un autre champ? (o/n): ")
        if continuer.lower() != "o":
            break


def lancer_quiz():
    pass
