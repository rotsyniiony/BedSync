import mysql.connector as my

class Connexion_base:
    ma_connexion = None
    @classmethod
    def get_connexion(cls):
        try:
            Connexion_base.ma_connexion = my.connect(
                host="localhost",
                user="root",
                password="",
                database="BedSync"
            )
            return Connexion_base.ma_connexion
        except my.Error as m:
            print(f"Erreur de connexion à la base de données: {m}")
