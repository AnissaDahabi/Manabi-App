from database.database import get_connection


def get_all_reservations():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM reservations")
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_reservations_enrichies():
    """
    Retourne les réservations avec les infos de l'élève, du cours et de la session.
    Colonnes : id, eleve_nom, eleve_prenom, cours_intitule, date_session, heure_debut, heure_fin, date_reservation, statut
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT
            r.id,
            u.nom,
            u.prenom,
            c.intitule,
            s.date_session,
            s.heure_debut,
            s.heure_fin,
            r.date_reservation,
            r.statut
        FROM reservations r
        JOIN users u ON r.eleve_id = u.id
        JOIN sessions s ON r.session_id = s.id
        JOIN cours c ON s.cours_id = c.id
        ORDER BY r.date_reservation DESC
    """)
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_reservations_enrichies_by_prof(prof_id):
    """
    Même requête, filtrée sur les sessions du professeur connecté.
    """
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT
            r.id,
            u.nom,
            u.prenom,
            c.intitule,
            s.date_session,
            s.heure_debut,
            s.heure_fin,
            r.date_reservation,
            r.statut
        FROM reservations r
        JOIN users u ON r.eleve_id = u.id
        JOIN sessions s ON r.session_id = s.id
        JOIN cours c ON s.cours_id = c.id
        WHERE s.prof_id = %s
        ORDER BY r.date_reservation DESC
    """, (prof_id,))
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def get_reservations_by_eleve(eleve_id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM reservations WHERE eleve_id = %s", (eleve_id,))
    resultats = curseur.fetchall()
    connexion.close()
    return resultats


def confirmer_reservation(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("UPDATE reservations SET statut = 'confirmee' WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()


def annuler_reservation(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("UPDATE reservations SET statut = 'annulee' WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()


def delete_reservation(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM reservations WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()