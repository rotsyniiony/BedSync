from Models.Connexion_base import *
from datetime import *

class IndispoModel():
    def __init__(self, id, lit, deb, fin, motif):
        self.id_indispo = id
        self.id_lit = lit
        self.date_debut = deb
        self.date_fin = fin
        self.motif = motif

    def get_id_indispo(self):
        return self._id_indispo
    def set_id_indispo(self,id):
        self._id_indispo = id

    def get_id_lit(self):
        return self._id_lit
    def set_id_lit(self, lit):
        self._id_lit = lit

    def get_debut(self):
        return self._date_debut
    def set_debut(self, deb):
        self._date_debut = deb

    def get_fin(self):
        return self._date_fin
    def set_fin(self, fin):
        self._date_fin = fin

    def get_motif(self):
        return self._motif
    def set_motif(self, motif):
        self._motif = motif

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


    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM indispo"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des indispo: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE indispo SET motif = %s, id_lit = %s, date_debut = %s, date_fin = %s WHERE id_indispo = %s"
            valeurs = (self.motif, self.id_lit, self.date_debut, self.date_fin, self.id_indispo)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de modification: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
    def delete(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "DELETE FROM indispo WHERE id_indispo = %s"
            valeur = (self.id_indispo,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def cloturer(cls, id_indispo):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            date_fin = date.today()
            req = "UPDATE indispo SET date_fin = %s WHERE id_indispo = %s"
            valeurs = (date_fin, id_indispo)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de cloturation: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def chercher_indispo(cls, id_indispo):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(buffered=True, dictionary=True)
            req = "SELECT * FROM indispo WHERE id_indispo = %s"
            valeur = (id_indispo,)
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            raise ValueError(f"Erreur de recherche d'insdisponibilité à id {id_indispo}: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste
