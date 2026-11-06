from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from datetime import *

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
    def nb_lits_instant_T(cls):
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
                        AND m.date_mouvement <= %s
                        AND (m.date_fin_mouvement IS NULL OR date_fin_mouvement > %s)
                    ))AS OCCUPE,
                    SUM(EXISTS(
                        SELECT 1 FROM indispo i WHERE i.id_lit = l.id_lit
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

    #Periode
    @classmethod
    def heures_indisponibilite(cls, p1, p2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT l.id_lit, l.code_lit,
                COALESCE(SUM(
                GREATEST(0, 
                TIMESTAMPDIFF(SECOND, GREATEST(i.date_debut, %s), LEAST(COALESCE(i.date_fin, %s), %s)
                )))/3600,0) AS heures
                FROM lit l
                LEFT JOIN indispo i
                ON i.id_lit = l.id_lit
                AND i.date_debut < %s
                AND COALESCE(i.date_fin, %s) > %s
                GROUP BY l.id_lit, code_lit
            """
            valeurs = (p1,p2, p2, p2, p2, p1)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def total_heures_occupation(cls, p1, p2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                COALESCE(SUM(
                GREATEST(0, 
                TIMESTAMPDIFF(SECOND, GREATEST(m.date_mouvement, %s), LEAST(COALESCE(m.date_fin_mouvement, %s), %s)
                )))/3600,0) AS heures
                FROM mouvement m
                WHERE m.date_mouvement < %s
                AND COALESCE(m.date_fin_mouvement, %s) > %s 
            """
            valeurs = (p1,p2, p2, p2, p2, p1)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def total_heures_indisponibilite(cls, p1, p2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                COALESCE(SUM(
                GREATEST(0, 
                TIMESTAMPDIFF(SECOND, GREATEST(i.date_debut, %s), LEAST(COALESCE(i.date_fin, %s), %s)
                )))/3600,0) AS heures
                FROM indispo i
                WHERE i.date_debut < %s
                AND COALESCE(i.date_fin, %s) > %s 
            """
            valeurs = (p1,p2, p2, p2, p2, p1)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    #A VERIFIER
    @classmethod
    def taux_periode(cls, d1, d2):
        journees_lits_occupation = float(StatService.total_heures_occupation(d1, d2)[0][0] / 24)
        nbr_lits = StatService.nb_lits_instant_T()[0]['total']
        heures = (d2 - d1).total_seconds() / 3600
        heures_indispo = float(StatService.total_heures_indisponibilite(d1, d2)[0][0])
        journees_lits_operationnels = ((nbr_lits * heures) - heures_indispo)/24
        print(nbr_lits * heures)
        print(journees_lits_occupation)
        print(journees_lits_operationnels)
        return (journees_lits_occupation / journees_lits_operationnels)

    @classmethod
    def nombre_admission_periode(d1, d2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                SUM(*)
                FROM mouvement m
                WHERE m.date_mouvement < %s AND m.date_mouvement > %s 
                AND m.statut_mouvement = %s
            """
            valeurs = (d1, d2, "ADMISSION")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def nombre_sortie_periode(d1, d2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                SUM(*)
                FROM mouvement m
                WHERE m.date_mouvement < %s AND m.date_mouvement > %s 
                AND m.statut_mouvement = %s
            """
            valeurs = (d1, d2, "SORTIE")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def nombre_transfert_periode(d1, d2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                SUM(*)
                FROM mouvement m
                WHERE m.date_mouvement < %s AND m.date_mouvement > %s 
                AND m.statut_mouvement = %s
            """
            valeurs = (d1, d2, "TRANSFERT")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def nombre_lits_indispo_periode(d1, d2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                SUM(*)
                FROM lit l
                LEFT JOIN indispo i
                ON i.id_lit = l.id_lit
                WHERE i.date_debut < %s AND i.date_fin > %s 
            """
            valeurs = (d1, d2)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def service_taux_occupation_eleve(d1, d2):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            req= """ 
                SELECT
                GREATEST(seuil_occupation)
                FROM service s
                LEFT JOIN mouvement m
                ON m.id_lit.id_service = s.id_service
                WHERE 
            """
            valeurs = (d1, d2)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    

    







       
    
            
