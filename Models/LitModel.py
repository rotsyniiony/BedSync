from Models.Connexion_base import *

class LitModel():
    def __init__(self, id_lit, id_service, code_lit, etat_lit, desc_lit):
        self.id_lit = id_lit
        self.id_service = id_service
        self.code_lit = code_lit
        self.etat_lit = etat_lit
        self.desc_lit = desc_lit

    def get_id_lit(self):
        return self.id_lit
    def set_id_lit(self, id_lit):
        self.id_lit = id_lit


    def get_code_lit(self):
        return self.code_lit
    def set_code_lit(self, code_lit):
        self.code_lit = code_lit


    def get_id_service(self):
        return self.id_service
    def set_id_service(self, id):
        self.id_service = id


    def get_etat_lit(self):
        return self.etat_lit
    def set_etat_lit(self, etat_lit):
        self.etat_lit = etat_lit


    def get_desc_lit(self):
        return self.desc_lit
    def set_desc_lit(self, desc_lit):
        self.desc_lit = desc_lit

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

