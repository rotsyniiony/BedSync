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
        return self._id_sejour
    def set_id_sejour(self, sejour):
        self._id_sejour = sejour

    def get_id_patient(self):
        return self._id_patient
    def set_id_patient(self, patient):
        self._id_patient = patient

    def get_id_service(self):
        return self._id_service
    def set_id_service(self, serv):
        self._id_service = serv

    def get_id_lit(self):
        return self._id_lit
    def set_id_lit(self, lit):
        self._id_lit = lit

    def get_admission(self):
        return self._date_admission
    def set_admission(self, adm):
        self._date_admission = adm
    
    def get_sortie(self):
        return self._date_sortie
    def set_sortie(self, sortie):
        self._date_sortie = sortie

    id_sejour = property(get_id_sejour, set_id_sejour)
    id_patient = property(get_id_patient, set_id_patient)
    id_service = property(get_id_service, set_id_service)
    id_lit = property(get_id_lit, set_id_lit)
    date_admission = property(get_admission, set_admission)
    date_sortie = property(get_sortie, set_sortie)


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