from Models.ServiceModel import *
from datetime import *

class ServiceController():
    
    def create(cls, nom_service, categorie_service, desc_service, seuil_occupation, statut_service):
        if not nom_service or not categorie_service:
            raise ValueError("Le nom de service est la catégorie concernés sont obligatoires")

        
        patient = ServiceModel(0, nom_service, categorie_service, desc_service, seuil_occupation, statut_service)        
        patient.create()
    create = classmethod(create)

    def read(cls):
        patient = ServiceModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_service , nom_service, categorie_service, desc_service, seuil_occupation, statut_service):
        if not nom_service or not categorie_service:
            raise ValueError("Remplir tous les champs")

        patient = ServiceModel(0, 0, "")
        patient.update(id_service , nom_service, categorie_service, desc_service, seuil_occupation, statut_service)
    update = classmethod(update)

    def delete(cls, id_service):
        if not id_service:
            raise ValueError("Entrez l'id du service")
        patient = ServiceModel(0, 0, "")
        patient.delete(id_service)
    delete = classmethod(delete)
        

    