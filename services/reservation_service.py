from database.database import get_connection

def get_all_reservations():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM reservations")
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

def delete_reservation(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM reservations WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()