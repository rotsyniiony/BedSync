from Models.LitModel import *
from Models.PatientModel import *
from Controllers.LitController import *
from Controllers.PatientController import *


PatientController.create(12, '2026-10-09')
PatientController.update(7, 13, datetime(2026, 6, 7))
l = PatientController.read()
for x in (l):
    print(x)

PatientController.delete()


