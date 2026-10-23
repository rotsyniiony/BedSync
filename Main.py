from Models.LitModel import *
from Models.PatientModel import *
from Controllers.LitController import *
from Controllers.PatientController import *
from Controllers.ServiceController import *
from Controllers.SejourController import *
from Controllers.MouvementController import *
from Controllers.IndispoController import *
from Models.ServiceModel import *


##PATIENT

#PatientController.create()
##PatientController.update(9, 13, datetime(2026, 6, 7))
#l = PatientController.read()
#for x in (l):
#    print(x)

##PatientController.delete(4)


##SERVICE

#ServiceController.create("1", "ophtalmologie", "pour les yeux", 20, "ACTIF")
#ServiceController.update(1, "nom", "toto", "desc", 12, "VI")
#l = ServiceController.read()
#for x in (l):
#    print(x)
#ServiceController.delete(1)
#ServiceController.desactiver(2)


#LIT

#LitController.create(id_service=2, desc_lit="description: pour chirurgie ophtalmologie")

#LitController.update(id_lit=1, code_lit=1, id_service=2, desc_lit="description: pour chirurgie ophtalmologie", etat_lit="INDISPONIBLE")
#l = LitController.read()
#for x in (l):
#    print(x)
#LitController.delete(1)
#t = LitController.rechercher_lit(code_lit=2)
#for x in t.items():
#    print(x)
#t = LitController.consulter_lit_etat("DISPONIBLE")

#for x in t:
#    print(x)
#t = LitController.compter_lits_service(2)
#for x in t.items():
#    print(x)

#t = LitController.compter_lits_etablissement()
#for x in t.items():
#    print(x)



#SEJOUR

#SejourController.create(id_lit=1, id_patient=5, id_service=2, date_admission=datetime(2026,10,21))
#SejourController.update(id_sejour=1, id_lit=1, id_patient=5, id_service=1, date_admission=datetime(2026, 6, 7), date_sortie=datetime(2026, 6, 8))
#l = SejourController.read()
#for x in (l):
#    print(x)
#SejourController.delete(1)

#MOUVEMENTS
#MouvementController.create(id_sejour=2, id_lit=1, type_mouvement="Transfert", date_mouvement=datetime(2026, 10, 22))

#MouvementController.update(id_mouvement=1, id_sejour=2, id_lit=1, type_mouvement="Transfert", date_mouvement=datetime(2026, 10, 22))
#l = MouvementController.read()
#for x in (l):
#    print(x)
#MouvementController.delete(1)


#INDISPO
#IndispoController.create(id_lit=1, motif="rien", date_debut=datetime(2026, 8, 7), date_fin=datetime(2026, 8, 7))

#IndispoController.cloturer(5)

#IndispoController.update(id_indispo=1, id_lit=1, motif="rien tout", date_debut=datetime(2026, 8, 7), date_fin=datetime(2026, 8, 7))
#l = IndispoController.read()
#for x in (l):
#    print(x)
#IndispoController.delete(1)





