from Models.Connexion_base import *

class LitModel():
    def __init__(self, id_lit, id_service, code_lit, etat_lit, desc_lit):
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
            chaine_req = "INSERT INTO Lit VALUES(NULL, %d, %d, %s, %s)"
            valeurs = (self.id_service, self.code_lit, self.etat_lit, self.desc_lit)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
        except:
            print("Erreur lors de l'ajout de lit")
        finally:
            curseur.close()
    def read_all(self):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req = "SELECT * FROM lit"
            curseur.execute(req)
            liste = curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des sejours: {e}")
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

