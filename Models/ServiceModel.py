from Models.Connexion_base import *

class ServiceModel():
    def __init__(self, id, nom, cat, des, seui, satut):
        self.id_service = id
        self.nom_service = nom
        self.categorie_service = cat
        self.desc_service = des
        self.seuil_occupation = seui
        self.statut_service = satut


    def get_id_service(self):
        return self.id_service
    def set_id_service(self, id):
        self.id_service = id

    def get_nom_service(self):
        return self.nom_service
    def set_nom_service(self, nom):
        self.nom_service = nom

    def get_categorie_service(self):
        return self.categorie_service
    def set_categorie_service(self, cat):
        self.categorie_service = cat

    def get_seuil_occupation(self):
        return self.seuil_occupation
    def set_seuil_occupation(self, seuil):
        self.seuil_occupation = seuil

    def get_statut_service(self):
        return self.statut_service
    def set_statut_service(self, statut):
        self.statut_service = statut

    def get_desc_service(self):
        return self.desc_service
    def set_desc_service(self, desc):
        self.desc_service = desc

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
        except:
            print("Erreur lors de l'ajout de service")
        finally:
            curseur.close()
            ma_connexion.close()
