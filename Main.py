from Models.LitModel import *
from Models.PatientModel import *

un_patient = PatientModel(0, 2, '2026-10-17')
l = un_patient.read_all()

print(l)