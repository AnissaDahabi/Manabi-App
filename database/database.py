import pymysql

def get_connection():
    connexion = pymysql.connect(
        host='172.26.131.113',
        database='manabi_db',
        user='user',
        password='user',
        port=3306
    )
    return connexion