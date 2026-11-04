from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *

#calculs et detecteurs
class StatService():
    def __init__(self):
        pass
    def litOccupe_sansSejourCours():
        lits_occupes = LitModel.lits_occupes()
        for x in lits_occupes:
            sejour_lit = SejourModel.lit_a_sejour(x)
            if(sejour_lit == []):
                raise ValueError(f"Le lit id: {x} est occupé mais ne possède pas de séjour en cours")

    @classmethod
    def sejour_sans_lit_occupe():
        sejour = SejourModel.sejour_a_lit()
        if(sejour != []):
            for x in sejour:
                raise ValueError(f"Le sejour {x['id_sejour']} n'a pas de lit occupé {x['id_lit']}")

    @classmethod
    def sejour_meme_lit():
        sejour = SejourModel.sejour_deux_lits()
        for i in len(sejour) - 1:
            for j in range(i+1, len(sejour)):
                if(sejour[i]['id_lit'] == sejour[j]['id_lit']):
                    raise ValueError(f"ces sejours ont le même lit: {sejour[i]['id_sejour']}")

    @classmethod
    def compter_lits_service(cls, id_service):
        liste = LitModel.compter_lits_service( id_service= id_service)
        return liste
    
    @classmethod
    def compter_lits_etablissement(cls):
        liste = LitModel.compter_lits_etablissement()
        return liste

    @classmethod
    def taux_occupation_instantane():
        liste = LitModel.compter_lits_etablissement()
        T_inst = liste['occupes'] / (liste['occupes'] + liste['disponibles'])
        return T_inst

    @classmethod
    def occupation_instantanee(cls):
        liste = LitModel.compter_lits_etablissement()
        taux = liste['occupes'] / (liste['occupes'] + liste['indisponibles'])
        return taux

    #ICI
    @classmethod
    def nb_lits_etablissement():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT l.etat_lit, COUNT(*) AS nb_lits FROM lit l GROUP BY l.etat_lit
            """
            curseur.execute(req)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def nb_lits_service():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT l.id_service,
                    SUM(l.etat_lit = %s) AS disponibles,
                    SUM(l.etat_lit = %s) AS occupes,
                    SUM(l.etat_lit = %s) AS indisponibles,
                    COUNT(*)             AS total
                FROM lit l
                GROUP BY l.id_service
            """
            valeurs = ("DISPONIBLE", "OCCUPE", "INDISPONIBLE")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste


    @classmethod
    def taux_occupation_instant_T():
        liste = StatService.nb_lits_instant_T()
        dispo = liste['TOTAL'] - liste['OCCUPE'] - liste['INDISPONIBLE']
        try:
            result = liste['OCCUPE'] / (liste['OCCUPE'] + dispo) * 100
        except ZeroDivisionError as e:
            raise ZeroDivisionError("NON CALCULABLE: Aucun lit opérationnel")
        return round(result, 2)

    @classmethod
    def nb_lits_instant_T():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT 
                    COUNT(*) AS total,
                    SUM(EXISTS (
                        SELECT 1 FROM mouvement m
                        WHERE m.id_lit = l.id_lit
                        AND m.date_debut_mouvement <= %s
                        AND (m.date_fin_mouvement IS NULL OR date_fin_mouvement > %s)
                    ))AS OCCUPE,
                    SUM(EXISTS(
                        SELECT 1 FROM indisponibilite i WHERE i.id_lit = l.id_lit
                        AND i.date_debut <= %s
                        AND i.date_fin IS NULL OR i.date_fin > %s
                    ))AS INDISPONIBLE
                FROM lit l              
            """
            t = datetime.today()
            valeurs = (t, t, t, t)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de lecture des lits: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste
    
            
