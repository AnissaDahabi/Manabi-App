from database.database import get_connection


def verifier_connexion(email, password):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "SELECT id, nom, prenom, email, role FROM users WHERE email = %s AND password = %s AND role IN ('admin', 'professeur')",
        (email, password)
    )
    resultat = curseur.fetchone()
    connexion.close()
    return resultat