from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Controllers.PatientController import *
from Services.StatService import *
from Views.Acceuil import *
from Views.TableauDeBord import *

class Fenetre(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BedSync")
        self.resize(600, 500)
        self.acceuil = Acceuil()
        self.tableau = TableauDeBord()
        self.addWidget(self.acceuil)
        self.addWidget(self.tableau)
        self.acceuil.bouton.clicked.connect(self.afficher_tableau)

    def afficher_tableau(self):
        self.setCurrentWidget(self.tableau)