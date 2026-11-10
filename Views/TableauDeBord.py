import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Controllers.PatientController import *
from Services.StatService import *
from Controllers.AlerteController import *



class TableauDeBord(QWidget):
    def __init__(self):
        super().__init__()
        infos = StatService.nb_lits_instant_T()
        a = StatService.nombre_admission()
        t = StatService.nombre_transfert()
        s = StatService.nombre_sortie()
        alertes_actives = AlerteController.read_active()
        titre = QLabel("Bienvenue sur le tableau de bord!")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size : 25px; color : #006D77")



        layout = QGridLayout(self)
        alertes = QFrame()
        alertes_layout = QVBoxLayout(alertes)
        titre_alerte = QLabel("Les alertes")
        alertes_layout.addWidget(titre_alerte)

        for x in alertes_actives:
            alerteX = QLabel(f"Alerte numéro: {x['id_alerte']}\nType: {x['type_alerte']}\nDescription de l'alerte: {x['description']}\nDate: {x['date_alerte']}")
            alerteX.setStyleSheet("background-color: #EDF6F9; color: #83C5BE; text-align: center; font-size: 20px; padding: 10px; border-radius: 20px")
            alertes_layout.addWidget(alerteX)
        alertes_layout.addStretch()



        total_lit = QLabel(f"Total des lits: {infos['TOTAL']}\n")
        dispo = QLabel(f"Lits disponibles: {infos['TOTAL'] - infos['INDISPONIBLE'] - infos['OCCUPE']}\n")
        indispo = QLabel(f"Lits indisponibles: {infos['INDISPONIBLE']}\n")
        occupes = QLabel(f"Lits occupés: {infos['OCCUPE']}\n")

        alertes.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77;")
        dispo.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77")
        occupes.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77")
        indispo.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77")
        total_lit.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77")


        
        layout.addWidget(titre, 0, 0, 1, 1)
        layout.addWidget(total_lit, 1, 0, 1, 1)
        layout.addWidget(dispo, 1, 1, 1, 1)
        layout.addWidget(alertes, 1, 2, 2, 1)
        layout.addWidget(occupes, 2, 0, 1, 1)
        layout.addWidget(indispo, 2, 1, 1, 1)

        



