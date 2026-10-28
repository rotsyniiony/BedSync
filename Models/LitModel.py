from Models.Connexion_base import *
from Models.ServiceModel import *

class LitModel():
    def __init__(self, id_lit, id_service,desc_lit, code_lit=None, etat_lit="DISPONIBLE"):
        self.id_lit = id_lit
        self.id_service = id_service
        self.code_lit = code_lit
        self.etat_lit = etat_lit
        self.desc_lit = desc_lit

    def get_id_lit(self):
        return self._id_lit
    def set_id_lit(self, id_lit):
        self._id_lit = id_lit


    def get_code_lit(self):
        return self._code_lit
    def set_code_lit(self, code_lit):
        self._code_lit = code_lit


    def get_id_service(self):
        return self._id_service
    def set_id_service(self, id):
        self._id_service = id


    def get_etat_lit(self):
        return self._etat_lit
    def set_etat_lit(self, etat_lit):
        self._etat_lit = etat_lit


    def get_desc_lit(self):
        return self._desc_lit
    def set_desc_lit(self, desc_lit):
        self._desc_lit = desc_lit

    id_lit = property(get_id_lit, set_id_lit)
    id_service = property(get_id_service, set_id_service)
    code_lit = property(get_code_lit, set_code_lit)
    etat_lit = property(get_etat_lit, set_etat_lit)
    desc_lit = property(get_desc_lit, set_desc_lit)

    def create(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO Lit VALUES(NULL, %s, NULL, %s, %s)"
            valeurs = (self.id_service, "DISPONIBLE", self.desc_lit)
            curseur.execute(chaine_req, valeurs)


            t = ServiceModel.get_service(self.id_service)
            id_lit = curseur.lastrowid
            code_lit = f"LIT-{id_lit:04d}"
            req = "UPDATE lit SET code_lit = %s WHERE id_lit = %s"
            valeurs = (code_lit, id_lit)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de lit: {e}")
        finally:
            curseur.close()

    @classmethod
    def update_etat(cls, etat_lit, id_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE lit SET etat_lit = %s WHERE id_lit = %s"
            valeurs = (etat_lit, id_lit)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de modification: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    
    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM lit"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    def update(self):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE lit SET code_lit = %s, id_service = %s, etat_lit = %s, desc_lit = %s WHERE id_lit = %s"
            valeurs = (self.code_lit, self.id_service, self.etat_lit, self.desc_lit, self.id_lit)
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
            req = "DELETE FROM lit WHERE id_lit = %s"
            valeur = (self.id_lit,)
            curseur.execute(req, valeur)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
    @classmethod
    def rechercher_lit(cls, code_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE code_lit = %s"
            valeur = (code_lit,)
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            print(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def liberer(id_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE lit SET statut_lit WHERE id_lit = %s"
            valeurs = ("DISPONIBLE", id_lit)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de modification: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def indispo(cls, id_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "UPDATE lit SET statut_lit WHERE id_lit = %s"
            valeurs = ("INDISPONIBLE", id_lit)
            curseur.execute(req, valeurs)
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de modification: {e}")
        finally:
            curseur.close()
            ma_connexion.close()

    @classmethod
    def consulter_lit_service(cls, id_service):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE id_service = %s"
            valeur = (id_service,)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def consulter_lit_etat(cls, etat):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE etat_lit = %s"
            valeur = (etat,)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des lits par état: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def compter_lits_service(cls, id_service):
        result = {}
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE etat_lit = %s AND id_service = %s"
            valeur = ("DISPONIBLE", id_service)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['disponibles'] = len(liste)

            liste = []
            req = "SELECT * FROM lit WHERE etat_lit = %s AND id_service = %s"
            valeur = ("INDISPONIBLE",id_service)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['indisponibles'] = len(liste)

            liste = []
            req = "SELECT * FROM lit WHERE etat_lit = %s AND id_service = %s"
            valeur = ("OCCUPÉS",id_service)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['occupes'] = len(liste)

            
        except Exception as e:
            print(f"Erreur de lecture des lits par état: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return result

    @classmethod
    def compter_lits_etablissement(cls):
        result = {}
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE etat_lit = %s"
            valeur = ("DISPONIBLE",)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['disponibles'] = len(liste)

            liste = []
            req = "SELECT * FROM lit WHERE etat_lit = %s"
            valeur = ("INDISPONIBLE",)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['indisponibles'] = len(liste)

            liste = []
            req = "SELECT * FROM lit WHERE etat_lit = %s"
            valeur = ("OCCUPÉS",)
            curseur.execute(req, valeur)
            liste = curseur.fetchall()
            result['occupes'] = len(liste)

            
        except Exception as e:
            print(f"Erreur de lecture des lits par état: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return result

    @classmethod
    def prendre_codes_lit(cls):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT code_lit FROM lit"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return [ligne['code_lit'] for ligne in liste]

    @classmethod
    def lit_occupe(cls, id_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE id_lit = %s AND etat_lit = %s"
            valeur = (id_lit,"OCCUPE")
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            raise ValueError(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def read_lit(cls, id_lit):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT * FROM lit WHERE id_lit = %s"
            valeur = (id_lit,)
            curseur.execute(req, valeur)
            liste = curseur.fetchone()
        except Exception as e:
            raise ValueError(f"Erreur de lecture du lit {id_lit}: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    
        