from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from Models.AlerteModel import *

class AlerteController:
    

    @classmethod 
    def create(cls,id_service, type_alerte, description, date_alerte, regle):
        alert = AlerteModel(0, id_service, type_alerte, description, date_alerte, regle)
        alert.create()

    @classmethod
    def resoudre(cls, id):
        alert = AlerteModel(id, 0, "", "", "", 0)
        alert.resoudre()

    @classmethod
    def read_active(cls):
        alert = AlerteModel(id, 0, "", "", "", 0)
        return alert.read_active()
        

    






