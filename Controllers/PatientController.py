from Models.PatientModel import *
from datetime import *

class PatientController():
    
    def ajout(cls, code_patient, date_fiche):
        if not code_patient or not date_fiche:
            raise ValueError("Le code de patient est la date de fiche concernée sont obligatoires")

        
        patient = PatientModel(0, code_patient, date_fiche)        
        patient.create()
    ajout = classmethod(ajout)

    def read(cls):
        patient = PatientModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_patient,code_patient, date_fiche):
        if not id_patient or not code_patient or not date_fiche:
            raise ValueError("Remplir tous les champs")
        if not isinstance(date_fiche, datetime):
            raise ValueError("Donnez une date valide AAAA-MM-JJ...")
        patient = PatientModel(0, 0, "")
        patient.update(id_patient, code_patient, date_fiche)
    update = classmethod(update)

    def delete(cls, id_patient):
        if not id_patient:
            raise ValueError("Entrez l'id du patient")
        patient = PatientModel(0, 0, "")
        patient.delete(id_patient)
    delete = classmethod(delete)
        

    