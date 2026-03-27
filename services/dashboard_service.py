from database.database import get_connection


def get_stats_admin():
    connexion = get_connection()
    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM users WHERE role = 'eleve'")
    nb_eleves = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM users WHERE role = 'professeur'")
    nb_profs = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM cours")
    nb_cours = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM sessions")
    nb_sessions = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM reservations WHERE statut = 'en attente'")
    nb_attente = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM reservations WHERE statut = 'confirmée'")
    nb_confirmees = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM reservations WHERE statut = 'annulée'")
    nb_annulees = curseur.fetchone()[0]

    connexion.close()

    return {
        'eleves': nb_eleves,
        'professeurs': nb_profs,
        'cours': nb_cours,
        'sessions': nb_sessions,
        'attente': nb_attente,
        'confirmees': nb_confirmees,
        'annulees': nb_annulees,
    }


def get_stats_professeur(prof_id):
    connexion = get_connection()
    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM cours WHERE prof_id = %s", (prof_id,))
    nb_cours = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM sessions WHERE prof_id = %s", (prof_id,))
    nb_sessions = curseur.fetchone()[0]

    curseur.execute("""
        SELECT COUNT(*) FROM reservations r
        JOIN sessions s ON r.session_id = s.id
        WHERE s.prof_id = %s AND r.statut = 'en_attente'
    """, (prof_id,))
    nb_attente = curseur.fetchone()[0]

    curseur.execute("""
        SELECT COUNT(*) FROM reservations r
        JOIN sessions s ON r.session_id = s.id
        WHERE s.prof_id = %s AND r.statut = 'confirmee'
    """, (prof_id,))
    nb_confirmees = curseur.fetchone()[0]

    curseur.execute("""
        SELECT COUNT(*) FROM reservations r
        JOIN sessions s ON r.session_id = s.id
        WHERE s.prof_id = %s AND r.statut = 'annulee'
    """, (prof_id,))
    nb_annulees = curseur.fetchone()[0]

    connexion.close()

    return {
        'cours': nb_cours,
        'sessions': nb_sessions,
        'attente': nb_attente,
        'confirmees': nb_confirmees,
        'annulees': nb_annulees,
    }