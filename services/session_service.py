from database.database import get_connection

def get_all_sessions():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM sessions")
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
    curseur.execute("INSERT INTO sessions(cours_id, prof_id, date_session, heure_debut, heure_fin) VALUES(%s, %s, %s, %s, %s);", (session.cours_id, session.prof_id, session.date_session, session.heure_debut, session.heure_fin,))
    connexion.commit()
    connexion.close()

def update_session(session):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("UPDATE sessions SET cours_id = %s, prof_id = %s, date_session = %s, heure_debut = %s, heure_fin = %s WHERE id = %s", (session.cours_id, session.prof_id, session.date_session, session.heure_debut, session.heure_fin, session.id,))
    connexion.commit()
    connexion.close()