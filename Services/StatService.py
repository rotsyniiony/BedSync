from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *

#calculs et detecteurs
class StatService():
    def __init__(self):
        pass
    def litOccupe_sansSejourCours():
        lits_occupes = LitModel.lits_occupes()
        for x in lits_occupes:
            sejour_lit = SejourModel.lit_a_sejour(x)
            if(sejour_lit == []):
                raise ValueError(f"Le lit id: {x} est occupé mais ne possède pas de séjour en cours")

    @classmethod
    def sejour_sans_lit_occupe():
        sejour = SejourModel.sejour_a_lit()
        if(sejour != []):
            for x in sejour:
                raise ValueError(f"Le sejour {x['id_sejour']} n'a pas de lit occupé {x['id_lit']}")

    @classmethod
    def sejour_meme_lit():
        sejour = SejourModel.sejour_deux_lits()
        for i in len(sejour) - 1:
            for j in range(i+1, len(sejour)):
                if(sejour[i]['id_lit'] == sejour[j]['id_lit']):
                    raise ValueError(f"ces sejours ont le même lit: {sejour[i]['id_sejour']}")

    @classmethod
    def compter_lits_service(cls, id_service):
        liste = LitModel.compter_lits_service( id_service= id_service)
        return liste
    
    @classmethod
    def compter_lits_etablissement(cls):
        liste = LitModel.compter_lits_etablissement()
        return liste

    @classmethod
    def occupation_instantanee(cls):
        liste = LitModel.compter_lits_etablissement()
        taux = liste['occupes'] / (liste['occupes'] + liste['indisponibles'])
        return taux

    
            
