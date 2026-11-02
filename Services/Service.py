from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from datetime import *

class Service():
    def __init__(self):
        pass
    @classmethod
    def admission(cls, id_patient,id_service,id_lit):
        p = PatientModel.patient_existe(id_patient=id_patient)
        c = SejourModel.patient_encours(id_patient=id_patient)
        t = ServiceModel.read_service(id_service)
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
        date_admission = datetime.now()
        id = SejourModel(0, id_patient,id_service,id_lit, "EN_COURS", date_admission).create()
        MouvementModel(0, id, id_lit, "ADMISSION", date_admission).create()
        LitModel.occuper(id_lit)
