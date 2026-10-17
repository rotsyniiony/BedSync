from Models.Connexion_base import *

class IndispoModel():
    def __init__(self, id, lit, deb, fin, motif):
        self.id_indispo = id
        self.id_lit = lit
        self.date_debut = deb
        self.date_fin = fin
        self.motif = motif

    def get_id_indispo(self):
        return self.id_indispo
    def set_id_indispo(self,id):
        self.id_indispo = id

    def get_id_lit(self):
        return self.id_lit
    def set_id_lit(self, lit):
        self.id_lit = lit

    def get_debut(self):
        return self.date_debut
    def set_debut(self, deb):
        self.date_debut = deb

    def get_fin(self):
        return self.date_fin
    def set_fin(self, fin):
        self.date_fin = fin

    def get_motif(self):
        return self.motif
    def set_motif(self, motif):
        self.motif = motif

    id_indispo = property(get_id_indispo, set_id_indispo)
    id_lit = property(get_id_lit, set_id_lit)
    date_debut = property(get_debut, set_debut)
    date_fin = property(get_fin, set_fin)
    motif = property(get_motif, set_motif)

    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Indispo VALUES(NULL, %s, %s, %s, %s)"
            valeurs = (self.id_lit, self.date_debut, self.date_fin, self.motif)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except:
            print("Erreur lors de l'ajout de sejour")
        finally:
            curseur.close()
            ma_connexion.close()