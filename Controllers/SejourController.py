from Models.SejourModel import *
from datetime import *

class SejourController():
    
    def ajout(cls, id_patient,id_sevice,id_lit, date_admission, date_sortie):
        if not id_patient or not id_lit:
            raise ValueError("Le code de service est le lit concerné sont obligatoires")

        
        patient = SejourModel(0,id_patient,id_sevice,id_lit, date_admission, date_sortie)        
        patient.create()
    ajout = classmethod(ajout)

    def read(cls):
        patient = SejourModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls, id_sejour, id_patient,id_sevice,id_lit, date_admission, date_sortie):
        if not id_patient or not id_lit:
            raise ValueError("Remplir tous les champs")
        if not isinstance(date_admission, datetime) or not isinstance(date_sortie, datetime):
            raise ValueError("Donnez une date valide AAAA-MM-JJ...")
        patient = SejourModel(0, 0, "")
        patient.update(id_sejour, id_patient,id_sevice,id_lit, date_admission, date_sortie)
    update = classmethod(update)

    def delete(cls, id_sejour):
        if not id_sejour:
            raise ValueError("Entrez l'id du service")
        patient = SejourModel(0, 0, "")
        patient.delete(id_sejour)
    delete = classmethod(delete)
        

    