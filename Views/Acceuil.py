from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Controllers.PatientController import *
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