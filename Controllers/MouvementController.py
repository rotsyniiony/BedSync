from Models.MouvementModel import *
from Models.SejourModel import *
from datetime import *

class MouvementController():
    
    def create(cls, id_sejour, id_lit, type_mouvement, date_mouvement):
        if not id_sejour or not type_mouvement:
            raise ValueError("Le nom du sejour est le type de mouvement concernés sont obligatoires")

        if(type_mouvement == "SORTIE"):
            sejour = SejourModel.read_sejour(id_sejour)
            if(sejour == []):
                raise ValueError("Aucun sejour de ce type");
            if(sejour['statut_sejour'] != "EN_COURS"):
                raise ValueError(f"Ce sejour est {sejour['statut_sejour']}")
            if(date_mouvement <= sejour['date_admission']):
                raise ValueError(f"Date antérieure à la date d'admission")
            patient = MouvementModel(id_mouvement=0, id_sejour=id_sejour, id_lit=id_lit, type_mouvement=type_mouvement, date_mouvement=date_mouvement) 

        
        patient = MouvementModel(id_mouvement=0, id_sejour=id_sejour, id_lit=id_lit, type_mouvement=type_mouvement, date_mouvement=date_mouvement)        
        patient.create()
    create = classmethod(create)

    

    def read(cls):
        patient = MouvementModel(0, 0, 0, "", "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_mouvement , id_sejour, id_lit, type_mouvement, date_mouvement):
        if not id_sejour or not type_mouvement:
            raise ValueError("Remplir tous les champs")

        patient = MouvementModel(id_mouvement , id_sejour, id_lit, type_mouvement, date_mouvement)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_mouvement):
        if not id_mouvement:
            raise ValueError("Entrez l'id du mouvement")
        patient = MouvementModel(id_mouvement, 0, 0, "","")
        patient.delete()
    delete = classmethod(delete)
        

    