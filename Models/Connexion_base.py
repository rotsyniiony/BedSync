import mysql.connector as my

class Connexion_base:
    ma_connexion = None
    def get_connexion(cls):
        if(Connexion_base.ma_connexion == None):
            try:
                Connexion_base.ma_connexion = my.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="BedSync"
                )
            except my.Error:
                print("Erreur de connexion à la base de données")
        else:
            return Connexion_base.ma_connexion
    get_connexion = classmethod(get_connexion)