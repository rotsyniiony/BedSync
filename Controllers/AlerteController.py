from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from Models.AlerteModel import *

class AlerteController:
    @classmethod
    def read_all_now(cls):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM alerte WHERE description != %s"
            valeur = ("RESOLUE", )
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            raise ValueError(f"Erreur de lecture des lits occupes: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod 
    def create(cls,id_service, type_alerte, description, date_alerte, regle):
        alert = AlerteModel(0, id_service, type_alerte, description, date_alerte, regle)
        alert.create()

    @classmethod
    def resoudre(cls, id):
        alert = AlerteModel(id, 0, "", "", "", 0)
        alert.resoudre()

    






