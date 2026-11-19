from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def val(d, *cles, defaut=""):
    """Renvoie la première clé présente (et non None) d'un dictionnaire.
    Pratique si le nom exact d'une colonne varie (ex. 'statut' ou 'statut_service')."""
    for c in cles:
        if c in d and d[c] is not None:
            return d[c]
    return defaut


def texte(v):
    """Convertit une valeur en texte lisible (dates au format AAAA-MM-JJ HH:MM:SS)."""
    if v is None:
        return ""
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    return str(v)


def securise(fonction, *args):
    """Appelle un calcul de StatService. Au lieu de planter, renvoie un texte :
    'Non calculable' (ZeroDivisionError) ou le message d'erreur."""
    try:
        return fonction(*args)
    except ZeroDivisionError:
        return "Non calculable"
    except IndexError:
        return "Aucune donnée"
    except Exception as e:
        return f"Erreur : {e}"


def lire(fonction, *args):
    """Appelle une méthode de lecture et renvoie toujours une liste.
    Les contrôleurs lèvent ValueError quand il n'y a aucun résultat : on renvoie alors []."""
    try:
        r = fonction(*args)
    except ValueError:
        return []
    if r is None:
        return []
    if isinstance(r, dict):
        return [r]
    return list(r)


def pct(v):
    """Formate un nombre en pourcentage ; laisse tel quel un texte (« Non calculable »)."""
    if isinstance(v, str):
        return v
    return f"{float(v):.1f} %"


def heures(v):
    if isinstance(v, str):
        return v
    return f"{float(v):.1f} h"


def remplir(table, entetes, lignes):
    """Remplit un QTableWidget avec une liste de lignes (listes de valeurs)."""
    table.setColumnCount(len(entetes))
    table.setHorizontalHeaderLabels(entetes)
    table.setRowCount(len(lignes))
    for i, ligne in enumerate(lignes):
        for j, valeur in enumerate(ligne):
            table.setItem(i, j, QTableWidgetItem(texte(valeur)))
    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)


def remplir_combo(combo, paires, premier=None):
    """paires = liste de (texte affiché, donnée). 'premier' ajoute un choix « tous » (donnée None).
    La sélection précédente est conservée si elle existe encore."""
    choix = combo.currentData()
    combo.blockSignals(True)
    combo.clear()
    if premier:
        combo.addItem(premier, None)
    for t, d in paires:
        combo.addItem(t, d)
    if choix is not None and combo.findData(choix) >= 0:
        combo.setCurrentIndex(combo.findData(choix))
    combo.blockSignals(False)

def paire(liste, nom, valeur):
    if(nom == "code_lit"):
        return[(f"{x[nom]} ({x['nom_service']})", x[valeur]) for x in liste]
    return [(x[nom], x[valeur]) for x in liste]

def erreur(parent, e):
    QMessageBox.warning(parent, "Opération refusée", str(e))


def info(parent, message):
    QMessageBox.information(parent, "Information", message)


def confirmer(parent, question):
    return QMessageBox.question(parent, "Confirmation", question) == QMessageBox.Yes


class Graphique(QWidget):
    """Un graphique Matplotlib intégré dans PyQt (guide, section 12.1)."""

    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def barres(self, titre, noms, valeurs, seuils):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        couleurs = ["#e63946" if v > s else "#2e86de" for v, s in zip(valeurs, seuils)]
        ax.bar(noms, valeurs, color=couleurs)
        ax.set_ylim(0, 100)
        ax.set_ylabel("%")
        ax.set_title(titre, fontsize=10)
        ax.tick_params(axis="x", labelsize=7)
        self.figure.tight_layout()
        self.canvas.draw()

    def courbe(self, titre, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, marker="o", color="#2e86de")
        ax.set_ylim(0, max(100, max(y) + 5))
        ax.set_ylabel("%")
        ax.set_title(titre, fontsize=10)
        ax.tick_params(axis="x", labelsize=7, rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

    def vide(self, titre, message):
        """Affiche un message à la place du graphique (ex. « Non calculable »)."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, message, ha="center", va="center", color="#6b7790",
                transform=ax.transAxes, wrap=True)
        ax.set_title(titre, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
