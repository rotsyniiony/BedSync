from Models.Connexion_base import *
class AlerteModel():
    def __init__(self,id_alerte, id_service, type_alerte, description, date_alerte, regle):
        self.id_alerte = id_alerte
        self.id_service = id_service
        self.type_alerte = type_alerte
        self.description = description
        self.date_alerte = date_alerte
        self.regle = regle

    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO alertes VALUES(NULL, %s,  %s, %s, %s, %s)"
            valeurs = (self.service, self.type_alerte, self.description, self.date_alerte, self.regle)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'alerte : {e}")
        finally:
            curseur.close()
            ma_connexion.close()