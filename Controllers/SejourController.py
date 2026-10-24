from Models.SejourModel import *
from Models.ServiceModel import *
from Models.PatientModel import *
from Models.LitModel import *
from Models.MouvementModel import *
from datetime import *

class SejourController():
    
    def create(cls, id_patient,id_service,id_lit,date_sortie=None):
        p = PatientModel.patient_existe(id_patient=id_patient)
        c = SejourModel.patient_encours(id_patient=id_patient)
        t = ServiceModel.get_service(id_service)
        l = LitModel.read_lit(id_lit=id_lit)
        
        #VERIFIER PATIENT EXISTE
        if(p == None):
            raise ValueError("Admission non accordée: Ce patient n'existe pas")

        #VERIFIER SI PATIENT DANS SEJOUR EN COURS
        if(c != None):
            raise ValueError("Admission non accordée: Ce patient est dans un séjour en cours")

        #VERIFIER SERVICE EXISTANT
        if(t == None):
            raise ValueError("Admission non accordée: Ce service n'existe pas")

        #VERIFIER SI SERVICE ACTIF
        if(t['statut'] == "INACTIF"):
            raise ValueError("Admission non accordée: service inactif")

        #VERIFIER LIT EXISTE
        if(l == None):
            raise ValueError("Admission non accordée: Ce lit n'existe pas")
        if(l['id_service'] != id_service):
            raise ValueError("Admission non accordée: Ce lit n'appartient pas à ce service")
        if(l['etat_lit'] != "DISPONIBLE"):
            raise ValueError("Admission non accordée: Ce lit n'est pas disponible")
        
        date_admission = date.today()
        statut_sejour="EN COURS"
        patient = SejourModel(0,id_patient,id_service,id_lit,statut_sejour,date_admission, date_sortie)      
        patient.create()
    create = classmethod(create)

    def read(cls):
        patient = SejourModel(0, 0, 0, 0 , "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls, id_sejour, id_patient,id_service,id_lit, date_admission, date_sortie):
        if not id_patient or not id_lit:
            raise ValueError("Remplir tous les champs")
        if not isinstance(date_admission, datetime) or not isinstance(date_sortie, datetime):
            raise ValueError("Donnez une date valide AAAA-MM-JJ...")
        patient = SejourModel(id_sejour, id_patient,id_service,id_lit, date_admission, date_sortie)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_sejour):
        if not id_sejour:
            raise ValueError("Entrez l'id du service")
        patient = SejourModel(id_sejour, 0,0, 0, "")
        patient.delete()
    delete = classmethod(delete)
        

    