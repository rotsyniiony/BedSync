from Models.MouvementModel import *
from datetime import *

class MouvementController():
    
    def create(cls, id_sejour, id_lit, type_mouvement, date_mouvement):
        if not id_sejour or not type_mouvement:
            raise ValueError("Le nom du sejour est le type de mouvement concernés sont obligatoires")

        
        patient = MouvementModel(0, id_sejour, id_lit, type_mouvement, date_mouvement)        
        patient.create()
    create = classmethod(create)

    def read(cls):
        patient = MouvementModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_mouvement , id_sejour, id_lit, type_mouvement, date_mouvement):
        if not id_sejour or not type_mouvement:
            raise ValueError("Remplir tous les champs")

        patient = MouvementModel(0, 0, "")
        patient.update(id_mouvement , id_sejour, id_lit, type_mouvement, date_mouvement)
    update = classmethod(update)

    def delete(cls, id_mouvement):
        if not id_mouvement:
            raise ValueError("Entrez l'id du mouvement")
        patient = MouvementModel(0, 0, "")
        patient.delete(id_mouvement)
    delete = classmethod(delete)
        

    