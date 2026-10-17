from Models.LitModel import *
from Models.PatientModel import *

un_patient = PatientModel(0, 2, '2026-10-17')
un_patient.create()

print(un_patient.id_patient)