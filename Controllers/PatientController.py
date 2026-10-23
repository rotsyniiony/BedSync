from Models.PatientModel import *
from datetime import *

class PatientController():
    
    def create(cls):
        PatientModel.create()       
    create = classmethod(create)

    def read(cls):
        patient = PatientModel(0, 0, "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_patient,code_patient, date_fiche):
        if not id_patient or not code_patient or not date_fiche:
            raise ValueError("Remplir tous les champs")
        if not isinstance(date_fiche, datetime):
            raise ValueError("Donnez une date valide AAAA-MM-JJ...")
        patient = PatientModel(id_patient, code_patient, date_fiche)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_patient):
        if not id_patient:
            raise ValueError("Entrez l'id du patient")
        patient = PatientModel(id_patient, 0, "")
        patient.delete()
    delete = classmethod(delete)

    def get_patient(cls, code_patient):
        PatientModel.get_patient(code_patient=code_patient)
        
        

    