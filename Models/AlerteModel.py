from Models.Connexion_base import *
from datetime import *
class AlerteModel():
    def __init__(self,id_alerte, id_service, type_alerte, description, date_alerte, regle, date_resolution=None, statut_alerte="NON_RESOLUE"):
        self.id_alerte = id_alerte
        self.id_service = id_service
        self.type_alerte = type_alerte
        self.description = description
        self.date_alerte = date_alerte
        self.date_resolution = date_resolution
        self.regle = regle
        self.statut_alerte = statut_alerte


    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO alertes VALUES(NULL, %s,  %s, %s, %s,%s, %s, %s)"
            valeurs = (self.id_service, self.type_alerte, self.description, self.date_alerte,self.date_resolution,self.regle, self.statut_alerte)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'alerte : {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def resoudre(cls, id):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE Alerte SET date_resolution = %s, statut_alerte = %s WHERE id_alerte = %s"
            valeurs = (datetime.today(),"RESOLUE", id)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de résolution: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def alerte_active(cls, id_service, type_alerte):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = """
                SELECT id_alerte
                FROM Alertes
                WHERE id_service = %s
                AND type_alerte = %s
                AND statut = %s
                LIMIT 1
            """
            valeurs = (id_service, type_alerte, "NON_RESOLUE")
            curseur.execute(req, valeurs)
            alerte = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de résolution: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return alerte


    