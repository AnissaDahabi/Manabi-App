from database.database import get_connection
from models.cours import Cours


def get_all_cours():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM cours")
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_cours_enrichis():
    """
    Retourne tous les cours avec le nom complet du professeur.
    Colonnes : id, intitule, niveau, prof_id, description, prof_nom, prof_prenom
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT c.id, c.intitule, c.niveau, c.prof_id, c.description,
               u.nom, u.prenom
        FROM cours c
        JOIN users u ON c.prof_id = u.id
        ORDER BY c.intitule
    """)
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_cours_enrichis_by_prof(prof_id):
    """
    Même requête, filtrée sur un professeur donné.
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT c.id, c.intitule, c.niveau, c.prof_id, c.description,
               u.nom, u.prenom
        FROM cours c
        JOIN users u ON c.prof_id = u.id
        WHERE c.prof_id = %s
        ORDER BY c.intitule
    """, (prof_id,))
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_cours_by_id(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM cours WHERE id = %s", (id,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat


def delete_cours(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM cours WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()


def create_cours(cours):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO cours(intitule, niveau, prof_id, description) VALUES(%s, %s, %s, %s);",
        (cours.intitule, cours.niveau, cours.prof_id, cours.description,)
    )
    connexion.commit()
    connexion.close()


def update_cours(cours):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE cours SET intitule = %s, niveau = %s, prof_id = %s, description = %s WHERE id = %s",
        (cours.intitule, cours.niveau, cours.prof_id, cours.description, cours.id,)
    )
    connexion.commit()
    connexion.close()