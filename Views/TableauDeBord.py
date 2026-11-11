import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Controllers.PatientController import *
from Services.StatService import *
from Controllers.AlerteController import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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


        volant = QFrame()
        volant_layout = QGridLayout(volant)


        for x in alertes_actives:
            alerteX = QLabel(f"Alerte numéro: {x['id_alerte']}\nType: {x['type_alerte']}\nDescription de l'alerte: {x['description']}\nDate: {x['date_alerte']}")
            alerteX.setStyleSheet("background-color: #EDF6F9; color: #83C5BE; text-align: center; font-size: 20px; padding: 10px; border-radius: 20px")
            alertes_layout.addWidget(alerteX)
        alertes_layout.addStretch()



        total_lit = QLabel(f"Total des lits: {infos['TOTAL']}\n")
        dispo = QLabel(f"Lits disponibles: {infos['TOTAL'] - infos['INDISPONIBLE'] - infos['OCCUPE']}\n")
        indispo = QLabel(f"Lits indisponibles: {infos['INDISPONIBLE']}\n")
        occupes = QLabel(f"Lits occupés: {infos['OCCUPE']}\n")

        alertes.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77; padding: 10px;")
        dispo.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77; padding: 10px;")
        occupes.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77; padding: 10px;")
        indispo.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77; padding: 10px;")
        total_lit.setStyleSheet("font-size: 25px; color: #83C5BE; background-color: #006D77; padding: 10px;")


        
        layout.addWidget(titre, 0, 0, 1, 0)
        layout.addWidget(total_lit, 1, 0, 1, 1)
        layout.addWidget(dispo, 1, 1, 1, 1)
        layout.addWidget(alertes, 1, 2, 2, 1)
        layout.addWidget(occupes, 2, 0, 1, 1)
        layout.addWidget(indispo, 2, 1, 1, 1)

        #d = DiagrammeOccupation(StatService.service_et_seuil_occupations(), "Barres", self)
        d2 = DiagrammeOccupation(StatService.serie_occupation(datetime(2026, 10, 28), datetime(2026, 10, 29)), "Courbe", self)
        layout.addWidget(d2, 3, 0, 2, 2)

    

class DiagrammeOccupation(FigureCanvas):
    def __init__(self, donnees, type_diagramme,parent=None):
        self.fig = Figure(figsize=(6, 4), tight_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)

        ax = self.fig.add_subplot(111)

        if type_diagramme == "Barres":
            noms = [d["nom_service"] for d in donnees]
            taux = [d["taux_occupation"] for d in donnees]
            def couleur(t):
                if t >= 90:
                    return "#006D77"   # saturé
                if t >= 70:
                    return "#F77F00"   # élevé
                return "#83C5BE"
            couleurs = [couleur(t) for t in taux]
            barres = ax.bar(noms, taux, color=couleurs, width=0.5)
            ax.bar_label(barres, labels=[f"{t:.1f} %" for t in taux],
                         label_type="center", color="white", fontweight="bold")
            ax.set_ylim(0, 100)
            ax.set_ylabel("Taux d'occupation (%)")
            ax.set_title("Taux d'occupation par service")

        elif type_diagramme == "Courbe":
            dates = [d["date_fin"] for d in donnees]
            taux = [d["taux_occupation"] for d in donnees]
            ax.plot(dates, taux, color="#006D77", marker="o")
            ax.set_ylim(0, 3)
            ax.set_ylabel("Taux d'occupation (%)")
            ax.set_title("Évolution du taux d'occupation")
            self.fig.autofmt_xdate()

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", rotation=0)
