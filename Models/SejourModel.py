from Models.Connexion_base import *

class SejourModel():
    def __init__(self, id, patient, service, lit, adm, sortie):
        self.id_sejour = id
        self.id_patient = patient
        self.id_service = service
        self.id_lit = lit
        self.date_admission = adm
        self.date_sortie = sortie

    def get_id_sejour(self):
        return self.id_sejour
    def set_id_sejour(self, sejour):
        self.id_sejour = sejour

    def get_id_patient(self):
        return self.id_patient
    def set_id_patient(self, patient):
        self.id_patient = patient

    def get_id_service(self):
        return self.id_service
    def set_id_service(self, serv):
        self.id_service = serv

    def get_id_lit(self):
        return self.id_lit
    def set_id_lit(self, lit):
        self.id_lit = lit

    def get_admission(self):
        return self.date_admission
    def set_admission(self, adm):
        self.date_admission = adm
    
    def get_sortie(self):
        return self.date_sortie
    def set_sortie(self, sortie):
        self.date_sortie = sortie


    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Sejour VALUES(NULL, %s, %s, %s, %s, %s)"
            valeurs = (self.id_patient, self.id_service, self.id_lit, self.date_admission, self.date_sortie)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except:
            print("Erreur lors de l'ajout de sejour")
        finally:
            curseur.close()
            ma_connexion.close()