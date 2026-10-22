from Models.LitModel import *
from Models.ServiceModel import *

class LitController:
    def create(cls, code_lit, id_service, etat_lit, desc_lit):
        t = ServiceModel.get_service(id_service)
        if (not code_lit or not id_service):
            raise ValueError("Le code du lit et le service sont obligatoires")
        if(t['statut'] == "INACTIF"):
            raise ValueError(f"Le service {t['nom_service']} est inactif")
        
        lit = LitModel(id_lit=0, code_lit=code_lit, id_service=id_service, etat_lit=etat_lit, desc_lit=desc_lit)
        lit.create()
    create = classmethod(create)

    def read(cls):
        patient = LitModel(0, 0, 0, "", "")
        return patient.read_all()
    read = classmethod(read)

    def update(cls,id_lit, code_lit, id_service, etat_lit, desc_lit):
        if not code_lit or not id_service:
            raise ValueError("Remplir tous les champs")

        patient = LitModel(id_lit, id_service , code_lit, etat_lit, desc_lit)
        patient.update()
    update = classmethod(update)

    def delete(cls, id_lit):
        if not id_lit:
            raise ValueError("Entrez l'id du service")
        patient = LitModel(id_lit, 0, 0 , "", "")
        patient.delete()
    delete = classmethod(delete)

    def rechercher_lit(cls, code_lit):
        liste = LitModel.rechercher_lit(code_lit=code_lit)
        if(liste == None):
            raise ValueError("Aucun lit ne possède ce code")
        else:
            return liste
    rechercher_lit = classmethod(rechercher_lit)

    def consulter_lit_service(cls, id_service):
        t = LitModel.consulter_lit_service(id_service=id_service)
        if(t == []):
            raise ValueError("Aucun lit de ce service")
        else:
            return t
    consulter_lit_service = classmethod(consulter_lit_service)