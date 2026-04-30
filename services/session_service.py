from database.database import get_connection
from models.session import Session


def get_all_sessions():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM sessions")
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_sessions_enrichies():
    """
    Retourne toutes les sessions avec le nom du cours et du professeur.
    Colonnes : id, cours_id, prof_id, date_session, heure_debut, heure_fin,
               cours_intitule, prof_nom, prof_prenom
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT s.id, s.cours_id, s.prof_id, s.date_session, s.heure_debut, s.heure_fin,
               c.intitule, u.nom, u.prenom
        FROM sessions s
        JOIN cours c ON s.cours_id = c.id
        JOIN users u ON s.prof_id = u.id
        ORDER BY s.date_session DESC, s.heure_debut
    """)
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_sessions_enrichies_by_prof(prof_id):
    """
    Même requête, filtrée sur un professeur donné.
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT s.id, s.cours_id, s.prof_id, s.date_session, s.heure_debut, s.heure_fin,
               c.intitule, u.nom, u.prenom
        FROM sessions s
        JOIN cours c ON s.cours_id = c.id
        JOIN users u ON s.prof_id = u.id
        WHERE s.prof_id = %s
        ORDER BY s.date_session DESC, s.heure_debut
    """, (prof_id,))
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_sessions_by_cours(cours_id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM sessions WHERE cours_id = %s", (cours_id,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat


def delete_session(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sessions WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()


def create_session(session):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO sessions(cours_id, prof_id, date_session, heure_debut, heure_fin) VALUES(%s, %s, %s, %s, %s);",
        (session.cours_id, session.prof_id, session.date_session, session.heure_debut, session.heure_fin,)
    )
    connexion.commit()
    connexion.close()


def update_session(session):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sessions SET cours_id = %s, prof_id = %s, date_session = %s, heure_debut = %s, heure_fin = %s WHERE id = %s",
        (session.cours_id, session.prof_id, session.date_session, session.heure_debut, session.heure_fin, session.id,)
    )
    connexion.commit()
    connexion.close()