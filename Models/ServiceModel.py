from Models.Connexion_base import *

class ServiceModel():
    def __init__(self, id, nom, cat, des, seui, satut):
        self.id_service = id
        self.nom_service = nom
        self.categorie_service = cat
        self.desc_service = des
        self.seuil_occupation = seui
        self.statut = satut


    def get_id_service(self):
        return self._id_service
    def set_id_service(self, id):
        self._id_service = id

    def get_nom_service(self):
        return self._nom_service
    def set_nom_service(self, nom):
        self._nom_service = nom

    def get_categorie_service(self):
        return self._categorie_service
    def set_categorie_service(self, cat):
        self._categorie_service = cat

    def get_seuil_occupation(self):
        return self._seuil_occupation
    def set_seuil_occupation(self, seuil):
        self._seuil_occupation = seuil

    def get_statut_service(self):
        return self._statut_service
    def set_statut_service(self, statut):
        self._statut_service = statut

    def get_desc_service(self):
        return self._desc_service
    def set_desc_service(self, desc):
        self._desc_service = desc

    id_service = property(get_id_service, set_id_service)
    nom_service = property(get_nom_service, set_nom_service)
    categorie_service = property(get_categorie_service, set_categorie_service)
    desc_service = property(get_desc_service, set_desc_service)
    seuil_occupation = property(get_seuil_occupation, set_seuil_occupation)
    statut_service = property(get_statut_service, set_statut_service)


    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Services VALUES(NULL, %s, %s, %s, %s, %s)"
            valeurs = (self.nom_service, self.categorie_service, self.desc_service, self.seuil_occupation, self.statut)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de service: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM services"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des services: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE services SET nom_service = %s, categorie_service = %s, desc_service = %s, seuil_occupation = %s, statut = %s WHERE id_service = %s"
            valeurs = (self.nom_service, self.categorie_service, self.desc_service,self.seuil_occupation, self.statut, self.id_service)
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
            req = "DELETE FROM services WHERE id_service = %s"
            valeur = (self.id_service,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def read_service(cls, id_service):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM services WHERE id_service = %s"
            valeur = (id_service,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
            liste = curseur.fetchone()
            if(liste is None):
                print("Aucun service trouvé")
        except Exception as e:
            print(f"Erreur de lecture pour cet id: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def desactiver(cls, id_service):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE services SET statut = %s WHERE id_service = %s"
            valeurs = ("INACTIF", id_service)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de désactivation: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def chercher_noms(cls):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT nom_service FROM services"
            valeur = ()
            curseur.execute(req, valeur)
            ma_connexion.commit()
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des noms de services: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return [ligne["nom_service"] for ligne in liste]

    @classmethod
    def consulter_lit_service(id_service):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT " \
            "s.id_service," \
            "s.nom_service," \
            "l.id_lit," \
            "l.code_lit," \
            "l.etat_lit," \
            "l.desc_lit," \
            " FROM services INNER " \
            "JOIN lit AS l ON s.id_lit WHERE id_service = %s"
            valeur = (id_service,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
            liste = curseur.fetchone()
            if(liste is None):
                print("Aucun service trouvé")
        except Exception as e:
            print(f"Erreur de lecture pour cet id: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste
