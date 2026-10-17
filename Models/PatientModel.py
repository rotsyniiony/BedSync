from Models.Connexion_base import *

class PatientModel():
    def __init__(self, id, code, date):
        self.id_patient = id
        self.code_patient = code
        self.date_fiche = code

    def get_id_patient(self):
        return self.id_patient
    def set_id_patient(self, id):
        self.id_patient = id

    def get_code_patient(self):
        return self.code_patient
    def set_code_patient(self, code):
        self.code_patient = code

    def get_date_fiche(self):
        return self.date_fiche
    def set_date_fiche(self, date):
        self.date_fiche = date
    
    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Patient VALUES(NULL, %s, %s)"
            valeurs = (self.code_patient, self.date_fiche)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de patient: {e}")
        finally:
            curseur.close()
            ma_connexion.close()