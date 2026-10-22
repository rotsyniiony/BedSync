from Models.ServiceModel import *
from datetime import *

class ServiceController():
    
    def create(cls, nom_service, categorie_service, desc_service, seuil_occupation, statut_service):
        t = ServiceModel.chercher_noms()
        for x in t:
            if(x == nom_service):
                raise ValueError("Un service de ce nom existe déjà")
        if not nom_service or not categorie_service or not desc_service or not seuil_occupation or not statut_service:
            raise ValueError("Le nom, la catégorie, la description, le seuil, le statut concernés sont obligatoires")

        if(nom_service == ""):
            raise ValueError("Donnez à ce service un nom")

        if(seuil_occupation > 100 or seuil_occupation < 0):
            raise ValueError("Seuil d'occupation doit être entre 0 et 100")

        if(statut_service != "ACTIF" and statut_service != "INACTIF"):
            raise ValueError("le statut doit être soit actif soit inactif")

        if(desc_service == ""):
            raise ValueError("Donnez une description")

        if(categorie_service == ""):
            raise ValueError("Mentionner la catégorie")


        patient = ServiceModel(0, nom_service, categorie_service, desc_service, seuil_occupation, statut_service)        
        patient.create()
    create = classmethod(create)

    def read(cls):
        patient = ServiceModel(0, "", "", "", 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_service , nom_service, categorie_service, desc_service, seuil_occupation, statut_service):
        if not nom_service or not categorie_service:
            raise ValueError("Remplir tous les champs")

        if(seuil_occupation > 100 or seuil_occupation < 0):
            raise ValueError("Seuil d'occupation doit être entre 0 et 100")

        if(statut_service != "ACTIF" or statut_service != "INACTIF"):
            raise ValueError("le statut doit être soit actif soit inactif")

        if(desc_service == ""):
            raise ValueError("Donnez une description")

        if(categorie_service == ""):
            raise ValueError("Mentionner la catégorie")

        patient = ServiceModel(id_service , nom_service, categorie_service, desc_service, seuil_occupation, statut_service)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_service):
        if not id_service:
            raise ValueError("Entrez l'id du service")
        patient = ServiceModel(id_service, "", "", "", 0, "")
        patient.delete()
    delete = classmethod(delete)

    @classmethod
    def desactiver(cls, id_service):
        ServiceModel.desactiver(id_service)
            



    
        

    