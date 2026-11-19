import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QLabel, QPushButton, QLineEdit, QSpinBox,
                             QComboBox, QTableWidget, QListWidget, QStackedWidget, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QGroupBox, QDateTimeEdit, QCheckBox)
from PyQt5.QtCore import QDateTime

from Controllers.ServiceController import ServiceController
from Controllers.LitController import LitController
from Controllers.PatientController import PatientController
from Controllers.SejourController import SejourController
from Controllers.IndispoController import IndispoController
from Controllers.AlerteController import AlerteController
from Services.StatService import StatService
from Services.Detecteur import Detecteur

from Views.outils_vue import (val, texte, securise, lire, pct, heures, remplir, paire, remplir_combo,
                        erreur, info, confirmer, Graphique)

STYLE = """
QWidget { font-family: Arial; font-size: 13px; background: #f4f6f9; color: #222; }
QListWidget#menu { background: #1f2a44; color: #cfd8ea; border: none; font-size: 14px; }
QListWidget#menu::item { padding: 12px 16px; }
QListWidget#menu::item:selected { background: #2e86de; color: white; }
QFrame#panneau { background: #1f2a44; }
QLabel#titre { font-size: 22px; font-weight: bold; color: #1f2a44; }
QLabel#logo { background: #1f2a44; color: white; font-size: 16px; font-weight: bold; padding: 16px; }
QFrame#carte { background: white; border: 1px solid #dde3ee; border-radius: 10px; }
QLineEdit, QSpinBox, QComboBox, QDateTimeEdit { background: white; border: 1px solid #b8c2d6;
    border-radius: 6px; padding: 5px; }
QTableWidget { background: white; border: 1px solid #dde3ee; gridline-color: #e8ecf4; }
QHeaderView::section { background: #1f2a44; color: white; padding: 5px; border: none; }
QPushButton { background-color: #2e86de; color: white; border: none; border-radius: 6px;
    padding: 8px 16px; font-weight: bold; }
QPushButton:hover { background-color: #1b6ac9; }
QPushButton#danger { background-color: #e63946; }
QPushButton#reset { background-color: #3a4a6b; margin: 10px; }
QGroupBox { background: white; border: 1px solid #dde3ee; border-radius: 10px; margin-top: 12px;
    font-weight: bold; padding-top: 10px; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }
"""


def lire_services():
    return lire(ServiceController.read)


def service_actif(s):
    return val(s, "statut", "statut_service") == "ACTIF"


def paires_services(actifs_seulement=False):
    """[(nom, id_service), ...] pour remplir une liste déroulante."""
    return [(val(s, "nom_service", "nom"), val(s, "id_service"))
            for s in lire_services() if service_actif(s) or not actifs_seulement]


def noms_tables():
    """Dictionnaires id -> nom lisible, pour afficher des noms au lieu d'identifiants."""
    services = {val(s, "id_service"): val(s, "nom_service", "nom") for s in lire_services()}
    lits = {val(l, "id_lit"): val(l, "code_lit") for l in lire(LitController.read)}
    patients = {val(p, "id_patient"): val(p, "code_patient") for p in lire(PatientController.read_all)}
    return services, lits, patients


def paires_lits(lits):
    """[(« CODE (service) », id_lit), ...]"""
    services, _, _ = noms_tables()
    return [(f"{val(l, 'code_lit')} ({services.get(val(l, 'id_service'), '?')})", val(l, "id_lit"))
            for l in lits]


def lits_disponibles(id_service=None):
    if id_service is None:
        lits = lire(LitController.read_by_etat, "DISPONIBLE")
    else:
        lits = lire(LitController.read_by_service, id_service)
    return [l for l in lits if val(l, "etat_lit") == "DISPONIBLE"]


def compter_lits(id_service=None):
    """Renvoie {'DISPONIBLE': n, 'OCCUPE': n, 'INDISPONIBLE': n} (établissement ou service)."""
    etats = {"DISPONIBLE": 0, "OCCUPE": 0, "INDISPONIBLE": 0}
    if id_service is None:
        for l in StatService.nb_lits_etablissement() or []:
            etats[val(l, "etat_lit")] = int(val(l, "nb_lits", defaut=0))
    else:
        for l in StatService.nb_lits_service() or []:
            if val(l, "id_service") == id_service:
                for e in etats:
                    etats[e] = int(l[e] or 0)
    return etats


def sejours_en_cours():
    return [s for s in lire(SejourController.read_all) if val(s, "statut_sejour", "statut") == "EN_COURS"]


def paires_sejours(sejours):
    _, lits, patients = noms_tables()
    return [(f"#{val(s, 'id_sejour')} - {patients.get(val(s, 'id_patient'), val(s, 'id_patient'))}"
             f" - lit {lits.get(val(s, 'id_lit'), val(s, 'id_lit'))}", val(s, "id_sejour"))
            for s in sejours]



class Carte(QFrame):
    """Une carte avec un grand nombre coloré et un petit titre."""

    def __init__(self, titre, couleur):
        super().__init__()
        self.setObjectName("carte")
        self.valeur = QLabel("0")
        self.valeur.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {couleur}; border: none;")
        legende = QLabel(titre)
        legende.setStyleSheet("color: #6b7790; border: none;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.valeur)
        layout.addWidget(legende)

    def definir(self, valeur):
        self.valeur.setText(str(valeur))


class Page(QWidget):
    """Classe de base : chaque page a un titre, une méthode actualiser() et executer()."""
    titre = ""

    def __init__(self, fenetre):
        super().__init__()
        self.fenetre = fenetre

    def actualiser(self):
        pass

    def executer(self, action, message=None):
        """Lance une action (appel de contrôleur). Les erreurs métier (ValueError...)
        deviennent un message lisible. Renvoie True si tout s'est bien passé."""
        try:
            action()
        except Exception as e:
            erreur(self, e)
            return False
        if message:
            info(self, message)
        self.fenetre.apres_operation()
        return True


# ======================================================================
# Tableau de bord
# ======================================================================
class PageAccueil(Page):
    titre = "Tableau de bord"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.cartes = {
            "total": Carte("Total des lits", "#1f2a44"),
            "occupe": Carte("Occupés", "#e63946"),
            "dispo": Carte("Disponibles", "#2a9d8f"),
            "indispo": Carte("Indisponibles", "#f4a261"),
            "taux": Carte("Taux d'occupation", "#2e86de"),
            "alertes": Carte("Alertes actives", "#e63946"),
            "duree": Carte("Durée moy. séjours", "#6c5ce7"),
        }
        rangee = QHBoxLayout()
        for carte in self.cartes.values():
            rangee.addWidget(carte)
        self.graph1 = Graphique()
        self.graph2 = Graphique()
        graphiques = QHBoxLayout()
        graphiques.addWidget(self.graph1)
        graphiques.addWidget(self.graph2)
        layout = QVBoxLayout(self)
        layout.addLayout(rangee)
        layout.addLayout(graphiques)

    def actualiser(self):
        etats = compter_lits()
        self.cartes["total"].definir(sum(etats.values()))
        self.cartes["occupe"].definir(etats["OCCUPE"])
        self.cartes["dispo"].definir(etats["DISPONIBLE"])
        self.cartes["indispo"].definir(etats["INDISPONIBLE"])

        taux = securise(StatService.taux_instantanee)
        self.cartes["taux"].definir("N/C" if isinstance(taux, str) else pct(taux))
        self.cartes["alertes"].definir(len(lire(AlerteController.read_active)))
        duree = securise(StatService.duree_moyenne_sejour)       # en heures
        self.cartes["duree"].definir("N/C" if isinstance(duree, str) else f"{float(duree) / 24:.1f} j")

        # Graphique 1 : taux par service (rouge = seuil dépassé)
        donnees = securise(StatService.service_et_seuil_occupations)
        if isinstance(donnees, list) and donnees:
            self.graph1.barres("Occupation par service (rouge = seuil dépassé)",
                               [val(x, "nom_service") for x in donnees],
                               [float(x["taux_occupation"]) for x in donnees],
                               [float(x["seuil_occupation"]) for x in donnees])
        else:
            self.graph1.vide("Occupation par service", "Aucune donnée")

        # Graphique 2 : évolution du taux sur 14 jours
        fin = datetime.now()
        serie = securise(StatService.serie_taux, fin - timedelta(days=14), fin)
        if isinstance(serie, list) and serie:
            self.graph2.courbe("Évolution du taux (14 jours)",
                               [s["date_fin"].strftime("%d/%m") for s in serie],
                               [float(s["taux_journee_lit"]) * 100 for s in serie])
        else:
            self.graph2.vide("Évolution du taux (14 jours)",
                             serie if isinstance(serie, str) else "Aucune donnée")


# ======================================================================
# Services
# ======================================================================
class PageServices(Page):
    titre = "Services"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.services = []
        self.table = QTableWidget()
        self.nom = QLineEdit()
        self.categorie = QLineEdit()
        self.description = QLineEdit()
        self.seuil = QSpinBox()
        self.seuil.setRange(1, 100)
        self.seuil.setValue(85)
        self.statut = QComboBox()
        self.statut.addItems(["ACTIF", "INACTIF"])
        b_creer = QPushButton("Créer")
        b_creer.clicked.connect(self.creer)
        b_desactiver = QPushButton("Désactiver la sélection")
        b_desactiver.setObjectName("danger")
        b_desactiver.clicked.connect(self.desactiver)

        form = QFormLayout()
        form.addRow("Nom :", self.nom)
        form.addRow("Catégorie :", self.categorie)
        form.addRow("Description :", self.description)
        form.addRow("Seuil (%) :", self.seuil)
        form.addRow("Statut :", self.statut)
        form.addRow(b_creer)
        boite = QGroupBox("Nouveau service")
        boite.setLayout(form)
        boite.setFixedWidth(300)
        droite = QVBoxLayout()
        droite.addWidget(boite)
        droite.addWidget(b_desactiver)
        droite.addStretch()
        layout = QHBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(droite)

    def actualiser(self):
        self.services = ServiceController.read()
        remplir(self.table, ["ID", "Nom", "Catégorie", "Description", "Seuil", "Statut"],
                [[val(s, "id_service"), val(s, "nom_service"), val(s, "categorie_service"),
                  val(s, "desc_service"), val(s, "seuil_occupation"),
                  val(s, "statut")] for s in self.services])

    def creer(self):
        ok = self.executer(lambda: ServiceController.create(
            self.nom.text().strip(), self.categorie.text().strip(), self.description.text().strip(),
            self.seuil.value(), self.statut.currentText()), "Service créé.")
        if ok:
            for champ in (self.nom, self.categorie, self.description):
                champ.clear()

    def desactiver(self):
        ligne = self.table.currentRow()
        if ligne < 0:
            erreur(self, "Sélectionne d'abord un service.")
            return
        service = self.services[ligne]
        if confirmer(self, f"Désactiver « {val(service, 'nom_service', 'nom')} » ?"):
            self.executer(lambda: ServiceController.desactiver(val(service, "id_service")))



class PageLits(Page):
    titre = "Lits"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.lits = QTableWidget()
        self.c_dispo = Carte("Disponibles", "#2a9d8f")
        self.c_occupe = Carte("Occupés", "#e63946")
        self.c_indispo = Carte("Indisponibles", "#f4a261")
        cartes = QHBoxLayout()
        for c in (self.c_dispo, self.c_occupe, self.c_indispo):
            cartes.addWidget(c)

        self.filtre_service = QComboBox()
        self.filtre_etat = QComboBox()
        self.filtre_etat.addItem("Tous les états", None)
        for etat in ("DISPONIBLE", "OCCUPE", "INDISPONIBLE"):
            self.filtre_etat.addItem(etat, etat)
        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Code exact du lit puis Entrée...")
        self.filtre_service.currentIndexChanged.connect(self.actualiser)
        self.filtre_etat.currentIndexChanged.connect(self.actualiser)
        self.recherche.returnPressed.connect(self.actualiser)
        filtres = QHBoxLayout()
        for w in (self.filtre_service, self.filtre_etat, self.recherche):
            filtres.addWidget(w)

        self.table = QTableWidget()
        self.description = QLineEdit()
        self.description.setPlaceholderText("Description du nouveau lit")
        self.service = QComboBox()
        b_ajout = QPushButton("Ajouter un lit")
        b_ajout.clicked.connect(self.ajouter)
        ajout = QHBoxLayout()
        for w in (self.description, self.service, b_ajout):
            ajout.addWidget(w)

        layout = QVBoxLayout(self)
        layout.addLayout(cartes)
        layout.addLayout(filtres)
        layout.addWidget(self.table)
        layout.addLayout(ajout)

    def charger_lits(self, id_service, etat, code):
        if code:
            lits = lire(LitController.read_by_code, code)
        elif id_service is not None:
            lits = lire(LitController.read_by_service, id_service)
        elif etat is not None:
            lits = lire(LitController.read_by_etat, etat)
        else:
            lits = lire(LitController.read)
        if id_service is not None:
            lits = [l for l in lits if val(l, "id_service") == id_service]
        if etat is not None:
            lits = [l for l in lits if val(l, "etat_lit") == etat]
        return lits

    def actualiser(self):
        remplir_combo(self.filtre_service, paires_services(), premier="Tous les services")
        remplir_combo(self.service, paires_services(actifs_seulement=True))
        id_service = self.filtre_service.currentData()
        self.lits = self.charger_lits(id_service, self.filtre_etat.currentData(), self.recherche.text().strip())
        services, _, _ = noms_tables()
        remplir(self.table, ["ID", "Code", "Service", "État", "Description"],
                [[val(l, "id_lit"), val(l, "code_lit"), services.get(val(l, "id_service"), val(l, "id_service")),
                  val(l, "etat_lit"), val(l, "desc_lit")] for l in self.lits])
        etats = compter_lits(id_service)
        self.c_dispo.definir(etats["DISPONIBLE"])
        self.c_occupe.definir(etats["OCCUPE"])
        self.c_indispo.definir(etats["INDISPONIBLE"])

    def ajouter(self):
        ok = self.executer(lambda: LitController.create(self.service.currentData(),
        self.description.text().strip()), "Lit ajouté.")
        if ok:
            self.description.clear()


class PageIndispos(Page):
    titre = "Indisponibilités"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.indispos = []
        self.table = QTableWidget()
        self.lit = QComboBox()
        self.motif = QLineEdit()
        self.debut = QDateTimeEdit(QDateTime.currentDateTime())
        self.debut.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.avec_fin = QCheckBox("Avec date de fin")
        self.fin = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.fin.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        b_declarer = QPushButton("Déclarer l'indisponibilité")
        b_declarer.setObjectName("danger")
        b_declarer.clicked.connect(self.declarer)
        b_cloturer = QPushButton("Clôturer la sélection (remise en service)")
        b_cloturer.clicked.connect(self.cloturer)

        form = QFormLayout()
        form.addRow("Lit :", self.lit)
        form.addRow("Motif :", self.motif)
        form.addRow("Début :", self.debut)
        form.addRow(self.avec_fin)
        form.addRow("Fin :", self.fin)
        form.addRow(b_declarer)
        boite = QGroupBox("Nouvelle indisponibilité")
        boite.setLayout(form)
        boite.setFixedWidth(320)
        droite = QVBoxLayout()
        droite.addWidget(boite)
        droite.addWidget(b_cloturer)
        droite.addStretch()
        layout = QHBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(droite)

    def actualiser(self):
        _, lits, _ = noms_tables()
        self.indispos = lire(IndispoController.read)
        remplir(self.table, ["ID", "Lit", "Début", "Fin", "Motif", "Statut"],
                [[val(i, "id_indispo"), val(i, "id_lit"),
                  val(i, "date_debut"), val(i, "date_fin"), val(i, "motif"),
                  "TERMINE" if val(i, "date_fin") else "EN_COURS"] for i in self.indispos])
        remplir_combo(self.lit, paires_lits(lire(LitController.read)))

    def declarer(self):
        fin = self.fin.dateTime().toPyDateTime() if self.avec_fin.isChecked() else None
        ok = self.executer(lambda: IndispoController.create(
            self.lit.currentData(), self.debut.dateTime().toPyDateTime(), self.motif.text().strip(), fin),
            "Indisponibilité déclarée.")
        if ok:
            self.motif.clear()

    def cloturer(self):
        ligne = self.table.currentRow()
        if ligne < 0:
            erreur(self, "Sélectionne d'abord une indisponibilité.")
            return
        indispo = self.indispos[ligne]
        if val(indispo, "date_fin"):
            erreur(self, "Cette indisponibilité est déjà terminée.")
            return
        self.executer(lambda: IndispoController.cloturer(val(indispo, "id_indispo", "id_indisponibilite", "id")),
                      "Lit remis en service.")



class PageSejours(Page):
    titre = "Séjours"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.table = QTableWidget()
        self.seulement_en_cours = QCheckBox("Séjours en cours seulement")
        self.seulement_en_cours.stateChanged.connect(self.actualiser)

        # --- Admission
        self.a_patient = QComboBox()
        b_patient = QPushButton("+ Patient fictif")
        self.b_nouveau_p = QCheckBox("Nouveau patient")
        self.b_nouveau_p.clicked.connect(PatientController.create)
        b_patient.clicked.connect(self.nouveau_patient)
        self.a_service = QComboBox()
        self.a_service.currentIndexChanged.connect(self.maj_lits_admission)
        self.a_lit = QComboBox()
        b_a = QPushButton("Admettre")
        b_a.clicked.connect(self.admettre)
        f1 = QFormLayout()
        f1.addRow("Patient :", self.a_patient)
        f1.addRow(self.b_nouveau_p)
        f1.addRow("Service :", self.a_service)
        f1.addRow("Lit disponible :", self.a_lit)
        f1.addRow(b_a)
        f1.addRow(b_patient)
        w1 = QWidget()
        w1.setLayout(f1)


        self.s_sejour = QComboBox()
        b_s = QPushButton("Enregistrer la sortie")
        b_s.clicked.connect(self.sortir)
        f2 = QFormLayout()
        f2.addRow("Séjour en cours :", self.s_sejour)
        f2.addRow(QLabel("La sortie est enregistrée à l'heure actuelle."))
        f2.addRow(b_s)
        w2 = QWidget()
        w2.setLayout(f2)

        # --- Transfert
        self.t_sejour = QComboBox()
        self.t_lit = QComboBox()
        b_t = QPushButton("Transférer")
        b_t.clicked.connect(self.transferer)
        f3 = QFormLayout()
        f3.addRow("Séjour en cours :", self.t_sejour)
        f3.addRow("Lit de destination :", self.t_lit)
        f3.addRow(b_t)
        w3 = QWidget()
        w3.setLayout(f3)

        self.pile = QStackedWidget()
        for w in (w1, w2, w3):
            self.pile.addWidget(w)
        self.choix = QComboBox()
        self.choix.addItems(["Admission", "Sortie", "Transfert"])
        self.choix.currentIndexChanged.connect(self.pile.setCurrentIndex)
        boite = QGroupBox("Opération")
        layout_boite = QVBoxLayout(boite)
        layout_boite.addWidget(self.choix)
        layout_boite.addWidget(self.pile)
        boite.setFixedWidth(330)

        gauche = QVBoxLayout()
        gauche.addWidget(self.seulement_en_cours)
        gauche.addWidget(self.table)
        droite = QVBoxLayout()
        droite.addWidget(boite)
        droite.addStretch()
        layout = QHBoxLayout(self)
        layout.addLayout(gauche)
        layout.addLayout(droite)

    def actualiser(self):
        services, lits, patients = noms_tables()
        sejours = lire(SejourController.read_all)
        if self.seulement_en_cours.isChecked():
            sejours = [s for s in sejours if val(s, "statut_sejour", "statut") == "EN_COURS"]
        remplir(self.table, ["N°", "Patient", "Service", "Lit", "Admission", "Sortie", "Statut"],
                [[val(s, "id_sejour"), patients.get(val(s, "id_patient"), val(s, "id_patient")),
                  services.get(val(s, "id_service"), val(s, "id_service")),
                  lits.get(val(s, "id_lit"), val(s, "id_lit")),
                  val(s, "date_admission"), val(s, "date_sortie"), val(s, "statut_sejour", "statut")]
                 for s in sejours])

        pat = paire(PatientController.patient_sans_sejour(), "code_patient", "id_patient")
        remplir_combo(self.a_patient, pat)

        se = paire(ServiceController.read_actifs(), "nom_service", "id_service")
        remplir_combo(self.a_service, se)

        self.maj_lits_admission()


        en_cours = SejourController.read_all_statuts("EN_COURS")


        remplir_combo(self.s_sejour,en_cours)
        remplir_combo(self.t_sejour, en_cours)


        lits_dispo = paire(LitController.read_by_etat(etat="DISPONIBLE"), "code_lit", "id_lit")
        remplir_combo(self.t_lit, lits_dispo)

    def maj_lits_admission(self):
        """Uniquement les lits disponibles du service choisi."""
        lits_dispo = paire(LitController.read_by_etat(etat="DISPONIBLE"), "code_lit", "id_lit")
        remplir_combo(self.a_lit, lits_dispo)


    def nouveau_patient(self):
        self.executer(lambda: PatientController.create(), "Patient fictif créé.")

    def admettre(self):
        patient = PatientController.create() if self.b_nouveau_p.isChecked() else self.a_patient.currentData()
        self.executer(lambda: SejourController.create(
            patient, self.a_service.currentData(), self.a_lit.currentData()),
            f"Admission enregistrée.Nouveau patient: {patient}" if self.b_nouveau_p.isChecked() else f"Admission enregistrée.Patient {self.a_patient.currentData()}")

    def sortir(self):
        self.executer(lambda: SejourController.cloturer(self.s_sejour.currentData()),
                      "Sortie enregistrée.")

    def transferer(self):
        self.executer(lambda: SejourController.transferer(self.t_lit.currentData(),
                                                          self.t_sejour.currentData()),
                      "Transfert enregistré.")



class PageIndicateurs(Page):
    titre = "Indicateurs"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.service = QComboBox()
        self.debut = QDateTimeEdit(QDateTime.currentDateTime().addDays(-30))
        self.fin = QDateTimeEdit(QDateTime.currentDateTime())
        for d in (self.debut, self.fin):
            d.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        b_calculer = QPushButton("Calculer")
        b_calculer.clicked.connect(self.actualiser)
        self.table = QTableWidget()

        filtres = QHBoxLayout()
        for texte_label, widget in (("Service :", self.service), ("Du :", self.debut), ("Au :", self.fin)):
            filtres.addWidget(QLabel(texte_label))
            filtres.addWidget(widget, 1)
        filtres.addWidget(b_calculer)
        layout = QVBoxLayout(self)
        layout.addLayout(filtres)
        layout.addWidget(self.table)

    def actualiser(self):
        remplir_combo(self.service, paires_services(), premier="Tous les services")
        id_service = self.service.currentData()
        d1 = self.debut.dateTime().toPyDateTime()
        d2 = self.fin.dateTime().toPyDateTime()
        if d2 <= d1:
            erreur(self, "La date de fin doit être postérieure à la date de début.")
            return

        etats = compter_lits(id_service)
        lignes = [("Lits disponibles", etats["DISPONIBLE"]),
                  ("Lits occupés", etats["OCCUPE"]),
                  ("Lits indisponibles", etats["INDISPONIBLE"])]

        # taux instantané : global, ou celui du service choisi
        if id_service is None:
            taux = securise(StatService.taux_instantanee)
        else:
            donnees = securise(StatService.service_et_seuil_occupations)
            ligne = next((x for x in donnees if val(x, "id_service") == id_service), None) \
                if isinstance(donnees, list) else None
            taux = float(ligne["taux_occupation"]) if ligne else "Non calculable"
        lignes.append(("Taux d'occupation instantané", pct(taux)))

        taux_p = securise(StatService.taux_periode, d1, d2)
        lignes.append(("Taux d'occupation sur la période (établissement)",
                       taux_p if isinstance(taux_p, str) else pct(float(taux_p) * 100)))
        lignes.append(("Durée moyenne des séjours terminés",
                       heures(securise(StatService.duree_moyenne_sejour))))
        lignes.append(("Admissions sur la période", securise(StatService.nombre_admission, d1, d2, id_service)))
        lignes.append(("Sorties sur la période", securise(StatService.nombre_sortie, d1, d2, id_service)))
        lignes.append(("Transferts sur la période", securise(StatService.nombre_transfert, d1, d2, id_service)))
        lignes.append(("Lits indisponibles sur la période",
                       securise(StatService.nombre_lits_indispo, d1, d2, id_service)))
        lignes.append(("Heures d'indisponibilité",
                       heures(securise(StatService.nbr_heures_indispo, d1, d2, id_service))))

        plus_eleve = securise(StatService.service_seuil_eleve)
        if isinstance(plus_eleve, dict):
            lignes.append(("Service au taux d'occupation le plus élevé",
                           f"{val(plus_eleve, 'nom_service')} ({pct(plus_eleve['taux_occupation'])})"))
        else:
            lignes.append(("Service au taux d'occupation le plus élevé", plus_eleve))

        p = securise(StatService.periode_depassement, d1, d2, id_service)
        if isinstance(p, dict):
            p = (f"{texte(p.get('debut_depassement'))} -> {texte(p.get('fin_depassement'))} "
                 f"(pic {p.get('pic_taux')} %)")
        elif p is None:
            p = "Aucun dépassement"
        lignes.append(("Dépassement des seuils", p))
        remplir(self.table, ["Indicateur", "Valeur"], lignes)


# ======================================================================
# Alertes
# ======================================================================
class PageAlertes(Page):
    titre = "Alertes"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.alertes = []
        self.table = QTableWidget()
        b_resoudre = QPushButton("Marquer la sélection comme résolue")
        b_resoudre.clicked.connect(self.resoudre)
        b_evaluer = QPushButton("Réévaluer les alertes")
        b_evaluer.clicked.connect(self.reevaluer)
        boutons = QHBoxLayout()
        boutons.addWidget(b_resoudre)
        boutons.addWidget(b_evaluer)
        boutons.addStretch()
        layout = QVBoxLayout(self)
        layout.addLayout(boutons)
        layout.addWidget(self.table)

    def actualiser(self):
        services, _, _ = noms_tables()
        self.alertes = lire(AlerteController.read_active)
        remplir(self.table, ["N°", "Date", "Type", "Service", "Description", "Règle", "Statut"],
                [[val(a, "id_alerte"), val(a, "date_alerte"), val(a, "type_alerte"),
                  services.get(val(a, "id_service"), val(a, "id_service")), val(a, "description"),
                  val(a, "regle"), val(a, "statut_alerte")] for a in self.alertes])

    def resoudre(self):
        ligne = self.table.currentRow()
        if ligne < 0:
            erreur(self, "Sélectionne d'abord une alerte.")
            return
        self.executer(lambda: AlerteController.resoudre(val(self.alertes[ligne], "id_alerte")),
                      "Alerte marquée comme résolue.")

    def reevaluer(self):
        self.fenetre.apres_operation()


# ======================================================================
# Simulation
# ======================================================================
class PageSimulation(Page):
    titre = "Simulation"

    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.scenario = QComboBox()
        self.scenario.addItem("A - Plus d'admissions", "A")
        self.scenario.addItem("B - Lits indisponibles", "B")
        self.scenario.addItem("C - Réouverture de lits", "C")
        self.service = QComboBox()
        self.nombre = QSpinBox()
        self.nombre.setRange(1, 100)
        self.nombre.setValue(5)
        bouton = QPushButton("Simuler")
        bouton.clicked.connect(self.simuler)
        form = QFormLayout()
        form.addRow("Scénario :", self.scenario)
        form.addRow("Service :", self.service)
        form.addRow("Nombre :", self.nombre)
        form.addRow(bouton)
        boite = QGroupBox("Paramètres")
        boite.setLayout(form)
        boite.setFixedWidth(320)

        self.table = QTableWidget()
        self.alertes = QLabel("Lance une simulation.")
        self.alertes.setStyleSheet("color: #c1121f; font-weight: bold;")
        self.alertes.setWordWrap(True)
        note = QLabel("Estimation sur 30 jours, pas une prédiction. Aucune donnée n'est modifiée.")
        note.setStyleSheet("color: #6b7790;")
        note.setWordWrap(True)
        gauche = QVBoxLayout()
        gauche.addWidget(boite)
        gauche.addWidget(note)
        gauche.addStretch()
        droite = QVBoxLayout()
        droite.addWidget(self.table)
        droite.addWidget(self.alertes)
        layout = QHBoxLayout(self)
        layout.addLayout(gauche)
        layout.addLayout(droite)

    def actualiser(self):
        remplir_combo(self.service, paires_services(), premier="Tous les services")

    def simuler(self):
        try:
            r = SimulationService.simuler(self.scenario.currentData(), self.service.currentData(),
                                          self.nombre.value())
        except Exception as e:
            erreur(self, e)
            return
        remplir(self.table, ["Indicateur", "Avant", "Après", "Différence"], r["lignes"])
        self.alertes.setText("\n".join(r["alertes"]) if r["alertes"] else "Aucune alerte simulée.")


# ======================================================================
# Fenêtre principale
# ======================================================================
class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de l'occupation des lits")
        self.resize(1150, 720)
        self.message = ""

        self.pages = [PageAccueil(self), PageServices(self), PageLits(self), PageIndispos(self),
                      PageSejours(self), PageIndicateurs(self), PageAlertes(self), PageSimulation(self)]
        self.menu = QListWidget()
        self.menu.setObjectName("menu")
        self.pile = QStackedWidget()
        for page in self.pages:
            self.menu.addItem(page.titre)
            self.pile.addWidget(page)
        self.menu.currentRowChanged.connect(self.changer_page)

        logo = QLabel("Lits")
        logo.setObjectName("logo")
        bouton_reset = QPushButton("Réinitialiser la démo")
        bouton_reset.setObjectName("reset")
        bouton_reset.clicked.connect(self.reinitialiser)
        panneau = QFrame()
        panneau.setObjectName("panneau")
        panneau.setFixedWidth(200)
        layout_panneau = QVBoxLayout(panneau)
        layout_panneau.setContentsMargins(0, 0, 0, 0)
        layout_panneau.setSpacing(0)
        layout_panneau.addWidget(logo)
        layout_panneau.addWidget(self.menu)
        layout_panneau.addWidget(bouton_reset)

        self.titre = QLabel()
        self.titre.setObjectName("titre")
        self.statut = QLabel()
        self.statut.setStyleSheet("color: #c1121f;")
        droite = QVBoxLayout()
        droite.addWidget(self.titre)
        droite.addWidget(self.pile)
        droite.addWidget(self.statut)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 12, 8)
        layout.addWidget(panneau)
        layout.addLayout(droite)

        self.menu.setCurrentRow(0)

    def changer_page(self, i):
        self.pile.setCurrentIndex(i)
        self.titre.setText(self.pages[i].titre)
        self.rafraichir()

    def rafraichir(self):
        """Actualise seulement la page affichée (les autres le seront quand on les ouvrira)."""
        try:
            self.pile.currentWidget().actualiser()
            self.statut.setText(self.message)
        except Exception as e:
            self.statut.setText(f"Erreur d'affichage : {e}")

    def apres_operation(self):
        """Appelée après chaque admission, sortie, transfert ou changement d'indisponibilité."""
        try:
            Detecteur.evaluation_alerte()
            self.message = ""
        except Exception as e:
            self.message = f"Évaluation des alertes : {e}"
        self.rafraichir()

    def reinitialiser(self):
        if not confirmer(self, "Remplacer toutes les données par les données de démonstration ?"):
            return
        try:
            from data.seed import reinitialiser_donnees
        except ImportError:
            erreur(self, "Fichier data/seed.py introuvable (fonction reinitialiser_donnees).")
            return
        try:
            reinitialiser_donnees()
        except Exception as e:
            erreur(self, e)
            return
        self.apres_operation()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec_())
