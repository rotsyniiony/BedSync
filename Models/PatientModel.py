from Models.Connexion_base import *

class PatientModel():
    def __init__(self, id, code, date):
        self.id_patient = id
        self.code_patient = code
        self.date_fiche = date

    def get_id_patient(self):
        return self._id_patient
    def set_id_patient(self, id):
        self._id_patient = id

    def get_code_patient(self):
        return self._code_patient
    def set_code_patient(self, code):
        self._code_patient = code

    def get_date_fiche(self):
        return self._date_fiche
    def set_date_fiche(self, date):
        self._date_fiche = date

    id_patient = property(get_id_patient, set_id_patient)
    code_patient = property(get_code_patient, set_code_patient)
    date_fiche = property(get_date_fiche, set_date_fiche)
    
    
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

    def read_all(self):
        liste_patients = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM patient"
            curseur.execute(req)
            liste_patients = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des patients: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste_patients

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE patient SET code_patient = %s, date_fiche = %s WHERE id_patient = %s"
            valeurs = (self.code_patient, self.date_fiche, self.id_patient)
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
            req = "DELETE FROM patient WHERE id_patient = %s"
            valeur = (self.id_patient,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

