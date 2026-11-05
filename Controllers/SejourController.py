from Models.SejourModel import *
from Models.ServiceModel import *
from Models.PatientModel import *
from Models.LitModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from datetime import *

class SejourController():
    
    def create(cls, id_patient,id_service,id_lit,date_sortie=None):
        p = PatientModel.is_patient_existe(id_patient=id_patient)
        c = SejourModel.is_patient_encours(id_patient=id_patient)
        t = ServiceModel.read_service(id_service)
        l = LitModel.read_lit(id_lit=id_lit)
        
        #VERIFIER PATIENT EXISTE
        if(p == False):
            raise ValueError("Admission non accordée: Ce patient n'existe pas")

        #VERIFIER SI PATIENT DANS SEJOUR EN COURS
        if(c == True):
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

    @classmethod
    def read_all(cls):
        patient = SejourModel(0, 0, 0, 0 , "")
        return patient.read_all()

    @classmethod
    def cloturer(cls, id_s):
        sejour = SejourModel.read_sejour(id_sejour=id_s)
        #SI SEJOUR EXISTE
        if(sejour == []):
            raise ValueError("Echec de cloture: Ce séjour n'existe pas dans la table séjour")

    
        indispos = IndispoModel.read_all_now(sejour['id_lit'])
        SejourModel.cloturer(id_s=id_s)
        dernier_mouvement = MouvementModel.read_last_mouvement(id_sejour=id_s)

        #SI MOUVEMENT EN COURS EXISTE
        if(dernier_mouvement == []):
            raise ValueError("Echec de cloture: Aucun mouvement en cours dans la table mouvement")

        #CREER MOUVEMENT DE SORTIE
        m = MouvementModel(None, id_sejour=id_s, id_lit=sejour['id_lit'], type_mouvement="SORTIE", date_mouvement=datetime.now(), date_fin=datetime.now())
        m.create()     

        #INDISPO OU LIBERER LE LIT
        if(indispos != []):
            LitModel.indispo(sejour['id_lit'])
        else:
            LitModel.liberer(sejour['id_lit'])

        #CLOTURER LE DERNIER MOUVEMENT
        MouvementModel.cloturer(dernier_mouvement['id_mouvement'])

    @classmethod
    def transferer(cls,id_lit, id_sejour):
        nouveau_lit = LitModel.read_lit(id_lit=id_lit)
        sejour = SejourModel.read_sejour(id_sejour=id_sejour)
        service = ServiceModel.read_service(id_service=nouveau_lit['id_service'])
        dernier_mouvement = MouvementModel.read_mouvements(id_sejour= id_sejour)

        if(nouveau_lit['etat_lit'] != "DISPONIBLE"):
            raise ValueError(f"Lit {nouveau_lit['etat_lit']}")

        if(sejour['statut_sejour'] != "EN COURS"):
            raise ValueError(f"Séjour est {sejour['statut_sejour']}")
        if(id_lit == sejour['id_lit']):
            raise ValueError("C'est le même lit")

        if(service['statut'] != "ACTIF"):
            raise ValueError(f"Le service du lit d'arrivée est {service['statut_service']}")

        if(dernier_mouvement == []):
            raise ValueError("Aucun sejour avec date non cloturée pour ce sejour")

        #changer le numéro de lit du séjour
        SejourModel.update_lit(id_lit, id_sejour)

        #créer mouvement Transfert
        t = MouvementModel(None, id_sejour=id_sejour, id_lit=id_lit, type_mouvement="TRANSFERT", date_mouvement=datetime.now())
        t.create()

        #rendre dispo le lit de départ
        LitModel.liberer(id_lit=id_lit)

        #rendre occupé le lit d'arrivée
        LitModel.occuper(id_lit=id_lit)

        #cloturer dernier mouvement
        MouvementModel.cloturer(dernier_mouvement['id_mouvement'])

        if(service['id_service'] != sejour['id_service']):
            SejourModel.update_service(id_service=service['id_service'])

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
        

    