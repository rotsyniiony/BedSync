import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Services.StatService import *

class Acceuil(QWidget):
    def __init__(self):
        super().__init__()
        titre = QLabel("Bienvenue dans BedSync!")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size : 30px; color : #006D77")
        self.bouton = QPushButton("Commencer")
        self.bouton.setStyleSheet("font-size: 20px; color: #006D77; background-color: #83C5BE; border: none; padding: 10px; border-radius: 10px")
        layout = QVBoxLayout(self)
        layout.addWidget(titre)
        layout.addWidget(self.bouton)

class tableau_de_bord(QWidget):
    def __init__(self):
        super().__init__()
        infos = StatService.nb_lits_instant_T()
        titre = QLabel("Bienvenue sur le tableau de bord!")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size : 25px; color : #006D77")
        sejours = QLabel(f"Admissions: \nSorties: \nDurée moyenne de séjour: ")
        total_lit = QLabel(f"Total des lits: {infos['TOTAL']}\n")
        dispo = QLabel(f"Lits disponibles: {infos['TOTAL'] - infos['INDISPONBLE']}\n")
        indispo = QLabel(f"Lits indisponibles: {infos['INDISPONIBLE']}\n")
        occupes = QLabel(f"Lits occupés: {infos['OCCUPE']}\n")
        sejours.setStyleSheet("font-size: 15px; color: #83C5BE; background-color: #006D77;")

        dispo.setStyleSheet("font-size: 15px; color: #83C5BE; background-color: #006D77")

        occupes.setStyleSheet("font-size: 15px; color: #83C5BE; background-color: #006D77")

        indispo.setStyleSheet("font-size: 15px; color: #83C5BE; background-color: #006D77")

        total_lit.setStyleSheet("font-size: 15px; color: #83C5BE; background-color: #006D77")
        layout = QGridLayout(self)
        layout.addWidget(titre, 0, 0)
        layout.addWidget(sejours, 1, 0, 2, 1)
        layout.addWidget(total_lit, 1, 1, 1, 1)
        layout.addWidget(dispo, 1, 2, 1, 1)
        layout.addWidget(occupes, 2, 1, 1, 1)
        layout.addWidget(indispo, 2, 2, 1, 1)



class Fenetre(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BedSync")
        self.resize(600, 500)
        self.acceuil = Acceuil()
        self.tableau = tableau_de_bord()
        self.addWidget(self.acceuil)
        self.addWidget(self.tableau)
        self.acceuil.bouton.clicked.connect(self.afficher_tableau)

    def afficher_tableau(self):
        self.setCurrentWidget(self.tableau)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec_())