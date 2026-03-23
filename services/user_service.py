from database.database import get_connection

def get_all_users():
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM users")
    resultats = curseur.fetchall()
    connexion.close()
    return resultats

def delete_user(id):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM users WHERE id = %s", (id,))
    connexion.commit()
    connexion.close()

def create_user(user):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO users(nom, prenom, email, password, role) VALUES(%s, %s, %s, %s, %s);", (user.nom, user.prenom, user.email, user.password, user.role,))
    connexion.commit()
    connexion.close()

def update_user(user):
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("UPDATE users SET nom = %s, prenom = %s, email = %s, password = %s, role = %s WHERE id = %s", (user.nom, user.prenom, user.email, user.password, user.role, user.id,))
    connexion.commit()
    connexion.close()