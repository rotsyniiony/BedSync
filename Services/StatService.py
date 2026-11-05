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
    
            
