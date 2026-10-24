from Models.Connexion_base import *

class SejourModel():
    def __init__(self, id, patient, service, lit, stat, adm, sortie=None):
        self.id_sejour = id
        self.id_patient = patient
        self.id_service = service
        self.id_lit = lit
        self.date_admission = adm
        self.date_sortie = sortie
        self.statut_sejour = stat

    

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
            chaine_req = "INSERT INTO sejour VALUES(NULL, %s, %s, %s, %s, %s, %s)"
            valeurs = (self.id_patient, self.id_service, self.id_lit, self.date_admission, self.date_sortie, self.statut_sejour)
            curseur.execute(chaine_req, valeurs)

            id_sejour = curseur.lastrowid
            chaine_req = "INSERT INTO mouvement VALUES(NULL, %s,  %s, %s, %s)"
            valeurs = (id_sejour, self.id_lit, "ADMISSION" , self.date_admission)
            curseur.execute(chaine_req, valeurs)

            req = "UPDATE lit SET etat_lit = %s WHERE id_lit = %s"
            valeurs = ("OCCUPE", self.id_lit)
            curseur.execute(req, valeurs)

            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de sejour: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM sejour"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des sejours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE sejour SET id_patient = %s,  id_service = %s, id_lit = %s, date_admission = %s, date_sortie = %s WHERE id_sejour = %s"
            valeurs = (self.id_patient, self.id_service, self.id_lit, self.date_admission, self.date_sortie, self.id_sejour)
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
            req = "DELETE FROM sejour WHERE id_sejour = %s"
            valeur = (self.id_sejour,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()


    @classmethod
    def patient_encours(cls, id_patient):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM sejour WHERE id_patient = %s AND statut_sejour = %s"
            valeur = (id_patient, "EN COURS")
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            print(f"Erreur de lecture des sejours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    
    