from Models.LitModel import *
from Models.PatientModel import *
from Controllers.LitController import *
from Controllers.PatientController import *
from Controllers.ServiceController import *


##PATIENT

##PatientController.create(11, '2026-10-09')
##PatientController.update(9, 13, datetime(2026, 6, 7))
##l = PatientController.read()
##for x in (l):
##    print(x)

##PatientController.delete(4)


##SERVICE

#ServiceController.create("nom", "t", "desc", 12, "VI")
ServiceController.update(1, "nom", "toto", "desc", 12, "VI")
#l = ServiceController.read()
#for x in (l):
#    print(x)

#ServiceController.delete()


