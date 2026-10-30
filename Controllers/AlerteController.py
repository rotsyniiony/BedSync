from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *

class AlerteController:
    @classmethod
    def evaluer_alertes(cls):
        lits = LitModel.compter_lits_etablissement()
