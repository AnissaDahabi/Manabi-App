import mysql.connector
from database.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def get_connection():
    connexion = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connexion