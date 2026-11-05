from Models.PatientModel import *
from datetime import *

class PatientController():
    @classmethod
    def create(cls):
        PatientModel.create()       

    @classmethod
    def read_all(cls):
        patient = PatientModel(0, 0, "")
        return patient.read_all()
    
    @classmethod
    def update(cls,id_patient,code_patient, date_fiche):
        if not id_patient or not code_patient or not date_fiche:
            raise ValueError("Remplir tous les champs")
        if not isinstance(date_fiche, datetime):
            raise ValueError("Donnez une date valide AAAA-MM-JJ...")
        patient = PatientModel(id_patient, code_patient, date_fiche)
        patient.update()

    @classmethod
    def delete(cls, id_patient):
        if not id_patient:
            raise ValueError("Entrez l'id du patient")
        patient = PatientModel(id_patient, 0, "")
        patient.delete()

    @classmethod
    def read_by_code(cls, code_patient):
        PatientModel.read_by_code(code_patient=code_patient)
        
        

    