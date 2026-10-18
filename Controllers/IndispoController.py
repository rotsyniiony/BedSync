from Models.IndispoModel import *
from datetime import *

class IndispoController():
    
    def ajout(cls, id_lit, date_debut, date_fin, motif):
        if not id_lit or not motif:
            raise ValueError("Le nom du lit est le motif concernés sont obligatoires")

        
        patient = IndispoModel(0, id_lit, date_debut, date_fin, motif)        
        patient.create()
    ajout = classmethod(ajout)

    def read(cls):
        patient = IndispoModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_indispo, id_lit, date_debut, date_fin, motif):
        if not id_lit or not motif:
            raise ValueError("Remplir tous les champs")

        patient = IndispoModel(0, 0, "")
        patient.update(id_indispo, id_lit, date_debut, date_fin, motif)
    update = classmethod(update)

    def delete(cls, id_indispo):
        if not id_indispo:
            raise ValueError("Entrez l'id de l'indispo")
        patient = IndispoModel(0, 0, "")
        patient.delete(id_indispo)
    delete = classmethod(delete)
        

    