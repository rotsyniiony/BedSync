from Models.LitModel import *

class LitController:
    def ajout(cls, code_lit, id_service, etat_lit, desc_lit):
        if (not code_lit or not id_service):
            raise ValueError("Le code du lit et le service sont obligatoires")
        lit = LitModel(0, code_lit, id_service, etat_lit, desc_lit)
    ajout = classmethod(ajout)