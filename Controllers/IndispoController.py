from Models.IndispoModel import *
from Models.LitModel import *
from datetime import *


class IndispoController():
    
    def create(cls, id_lit, date_debut, motif, date_fin=None):
        l = LitModel.read_lit(id_lit=id_lit)
        if(l == None):
            raise ValueError("Aucun lit de ce type")
        t = LitModel.lit_occupe(id_lit)
        if(t != None):
            raise ValueError("Le lit est occupé")
        if not id_lit or not motif:
            raise ValueError("Le nom du lit est le motif concernés sont obligatoires")

        
        patient = IndispoModel(0, id_lit, date_debut, date_fin, motif)        
        patient.create()
        LitModel.update_etat("INDISPONIBLE", id_lit)
    create = classmethod(create)

    def read(cls):
        patient = IndispoModel(0, 0, "", "", "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_indispo, id_lit, date_debut, date_fin, motif):
        if not id_lit or not motif:
            raise ValueError("Remplir tous les champs")

        patient = IndispoModel(id_indispo, id_lit, date_debut, date_fin, motif)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_indispo):
        if not id_indispo:
            raise ValueError("Entrez l'id de l'indispo")
        patient = IndispoModel(id_indispo, 0, "", "", "")
        patient.delete()
    delete = classmethod(delete)


    def cloturer(cls, id_indispo):
        IndispoModel.cloturer(id_indispo)
        t = IndispoModel.chercher_indispo(id_indispo=id_indispo)
        LitModel.update_etat("DISPONIBLE", t['id_lit'])
    cloturer = classmethod(cloturer)

        

    