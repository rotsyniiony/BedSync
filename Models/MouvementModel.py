from Models.Connexion_base import *

class MouvementModel():
    def __init__(self, id_mouvement, id_sejour, id_lit, type_mouvement, date_mouvement):
        self.id_mouvement = id_mouvement
        self.id_sejour = id_sejour
        self.id_lit = id_lit
        self.type_mouvement = type_mouvement
        self.date_mouvement = date_mouvement

    def get_id_mouvement(self):
        return self._id_mouvement
    def set_id_mouvement(self, id):
        self._id_mouvement = id

    def get_id_sejour(self):
        return self._id_sejour
    def set_id_sejour(self, sejour):
        self._id_sejour = sejour

    def get_id_lit(self):
        return self._id_lit
    def set_id_lit(self, lit):
        self._id_lit  = lit

    def get_type_mouvement(self):
        return self._type_mouvement
    def set_type_mouvement(self, type):
        self._type_mouvement = type

    def get_date_mouvement(self):
        return self._date_mouvement
    def set_date_mouvement(self, date):
        self._date_mouvement = date


    id_mouvement = property(get_id_mouvement, set_id_mouvement)
    id_sejour = property(get_id_sejour, set_id_sejour)
    id_lit = property(get_id_lit, set_id_lit)
    type_mouvement = property(get_type_mouvement, set_type_mouvement)
    date_mouvement = property(get_date_mouvement, set_date_mouvement)


    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Mouvement VALUES(NULL, %s,  %s, %s, %s)"
            valeurs = (self.id_sejour, self.id_lit, self.type_mouvement, self.date_mouvement)
            print(f"{self.id_lit}")
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de mouvement : {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM Mouvement"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des mouvements: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE Mouvement SET id_sejour = %s, id_lit = %s, date_mouvement = %s WHERE id_mouvement = %s"
            valeurs = (self.id_sejour, self.id_lit, self.date_mouvement, self.id_mouvement)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de modification: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
    def delete(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "DELETE FROM Mouvement WHERE id_mouvement = %s"
            valeur = (self.id_mouvement,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

        