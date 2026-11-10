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
    def nb_lits_etablissement(cls):
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
    def nb_lits_service(cls):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT l.id_service, s.seuil_indispo,
                    SUM(l.etat_lit = %s) AS DISPONIBLE,
                    SUM(l.etat_lit = %s) AS OCCUPE,
                    SUM(l.etat_lit = %s) AS INDISPONIBLE,
                    COUNT(*)             AS TOTAL
                FROM lit l
                JOIN services s ON l.id_service = s.id_service
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
    def taux_instantanee(cls):
        liste = StatService.nb_lits_instant_T()
        lits_occupes = int(liste['OCCUPE'])
        lits_operationnels = int(liste['TOTAL']) - int(liste['INDISPONIBLE'])
        if(lits_operationnels <= 0):
            raise ZeroDivisionError("NON CALCULABLE")
        return round(lits_occupes / lits_operationnels * 100 ,2)

    @classmethod
    def nb_lits_instant_T(cls):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT 
                    COUNT(*) AS TOTAL,
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
            liste = curseur.fetchone()
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
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
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
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
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
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['heures']

    @classmethod
    def total_heures_indisponibilite(cls, p1, p2):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
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
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['heures']

    
    @classmethod
    def taux_periode(cls, d1, d2):
        #Journees_lits_occupé / Journées_lits_opérationnels
        journee_lits_occupes = int(StatService.total_heures_occupation(d1, d2) / 24)
        journee_lits_operationnels = int((StatService.nb_lits_instant_T()['TOTAL'] * (d2 - d1).total_seconds() / 3600) - int(StatService.total_heures_indisponibilite(d1, d2)) /24)
        if(journee_lits_operationnels <= 0):
            raise ZeroDivisionError("NON CALCULABLE")
        return round(journee_lits_occupes / journee_lits_operationnels, 3)

    @classmethod
    def nbr_sejours_termines(cls):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = """
                SELECT
                COUNT(*) AS sejours_termines
                FROM sejour s
                WHERE
                EXISTS(
                    SELECT 1 FROM mouvement mm
                    WHERE mm.id_sejour = s.id_sejour
                    AND mm.type_mouvement = %s
                )
            """
            valeurs = ("SORTIE", )
            curseur.execute(req, valeurs)
            total = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise Exception("Erreur de compte des séjours terminés: " + e)
        finally:
            curseur.close()
            ma_connexion.close()
        return total['sejours_termines']


    @classmethod
    def durees_sejours_termines(cls):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = """
                SELECT
                COALESCE(SUM(
                GREATEST(0,
                TIMESTAMPDIFF(SECOND, m.date_mouvement, 
                COALESCE(m.date_fin_mouvement, NOW()))
                ))/3600 ,0)
                AS duree_total_sejours
                FROM mouvement m
                WHERE
                m.type_mouvement IN (%s, %s)
                AND EXISTS(
                    SELECT 1 FROM mouvement mm
                    WHERE mm.id_sejour = m.id_sejour
                    AND mm.type_mouvement = %s
                )
            """
            valeurs = ("ADMISSION", "TRANSFERT", "SORTIE")
            curseur.execute(req, valeurs)
            total = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise Exception(f"Erreur de compte des séjours terminés: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return total['duree_total_sejours']


    @classmethod
    def duree_moyenne_sejour(cls):
        #duree_total_sejours_terminés / nbr_sejours_terminés
        return round(StatService.durees_sejours_termines() / StatService.nbr_sejours_termines(), 3)


    #autres indicateurs
    @classmethod
    def nombre_admission(cls, d1=None, d2=None, id_service=None):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = """
                SELECT
                COUNT(*) AS total
                FROM mouvement m
                JOIN lit l ON m.id_lit = l.id_lit
                WHERE ((%s IS NULL AND %s IS NULL) OR (m.date_mouvement < %s AND COALESCE(m.date_fin_mouvement, %s) > %s)) 
                AND (%s IS NULL OR l.id_service = %s)
                AND (m.type_mouvement = %s)
            """
            valeurs = (d2, d1,d2,datetime.today(),d1, id_service, id_service, "SORTIE")
            curseur.execute(req, valeurs)
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['total']

    @classmethod
    def nombre_sortie(cls, d1=None, d2=None, id_service=None):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT
                COUNT(*) AS total
                FROM mouvement m
                JOIN lit l ON m.id_lit = l.id_lit
                WHERE ((%s IS NULL AND %s IS NULL) OR (m.date_mouvement < %s AND COALESCE(m.date_fin_mouvement, %s) > %s)) 
                AND (%s IS NULL OR l.id_service = %s)
                AND (m.type_mouvement = %s)
            """
            valeurs = (d2, d1,d2, datetime.today(), d1, id_service, id_service, "SORTIE")
            curseur.execute(req, valeurs)
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['total']

    @classmethod
    def nombre_transfert(cls, d1=None, d2=None, id_service=None):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT
                COUNT(*) AS total
                FROM mouvement m
                JOIN lit l ON m.id_lit = l.id_lit
                WHERE ((%s IS NULL AND %s IS NULL) OR m.date_mouvement < %s AND COALESCE(m.date_fin_mouvement, %s) > %s) 
                AND (%s IS NULL OR l.id_service = %s)
                AND m.type_mouvement = %s
            """
            valeurs = (d2, d1,d2,datetime.today(), d1, id_service, id_service, "TRANSFERT")
            curseur.execute(req, valeurs)
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['total']

    @classmethod
    def nombre_lits_indispo(cls, d1=None, d2=None, id_service=None):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT
                COUNT(*) AS total
                FROM lit l
                LEFT JOIN indispo i
                ON i.id_lit = l.id_lit
                WHERE (%s IS NULL AND %s IS NULL) OR (i.date_debut < %s AND COALESCE(i.date_fin, %s) > %s)
                AND (%s IS NULL) OR (l.id_service = %s)
            """
            valeurs = (d2, d1, d2,datetime.today(), d1, id_service, id_service)
            curseur.execute(req, valeurs)
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du taux par période: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['total']

    #A REVOIR
    @classmethod
    def service_et_seuil_occupations(cls):
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT
                    s.id_service,
                    s.nom_service,
                    SUM(l.etat_lit = 'OCCUPE')      AS OCCUPE,
                    SUM(l.etat_lit = 'DISPONIBLE')  AS DISPONIBLE,
                    SUM(l.etat_lit = 'INDISPONIBLE') AS INDISPONIBLE,
                    s.seuil_occupation,
                    ROUND(100 * SUM(l.etat_lit = 'OCCUPE')
                    / SUM(l.etat_lit IN ('OCCUPE', 'DISPONIBLE')), 1) AS taux_occupation
                FROM services s
                JOIN lit l ON l.id_service = s.id_service
                WHERE s.statut = 'ACTIF'
                GROUP BY s.id_service, s.nom_service
                HAVING SUM(l.etat_lit IN ('OCCUPE', 'DISPONIBLE')) > 0
                ORDER BY taux_occupation DESC
            """
            curseur.execute(req)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du service avec seuil occupation élevé: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste

    @classmethod
    def service_seuil_eleve(cls):
        return StatService.service_et_seuil_occupations()[0]


    @classmethod
    def serie_taux(cls, d1, d2, pas=timedelta(days=1)):
        serie = []
        while (d1 < d2):
            t = d1 + pas
            fin = min(t, d2)
            serie.append((t, fin, StatService.taux_periode(d1=t, d2=fin)))
        return serie

    @classmethod
    def nbr_heures_indispo(cls, d1=None, d2=None, id_service=None):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = """
                SELECT 
                COALESCE(SUM(
                    GREATEST(0, 
                    TIMESTAMPDIFF(SECOND, i.date_debut, COALESCE(i.date_fin, %s))
                    )/3600
                )) AS total
                FROM indispo i
                JOIN lit l ON i.id_lit = l.id_lit
                WHERE
                (%s IS NULL OR i.date_debut < %s) AND (%s IS NULL OR COALESCE(i.date_fin, %s) > %s)
                AND (%s IS NULL OR l.id_service = %s)
            """
            valeurs = (datetime.today(), d1, d1, d2, datetime.today(), d2, id_service, id_service)
            curseur.execute(req, valeurs)
            liste = curseur.fetchone()
            ma_connexion.commit()
        except Exception as e:
            raise ValueError(f"Erreur de calcul du service avec seuil occupation élevé: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return liste['total']

    @classmethod
    def periode_depassement(cls, d1=None, d2=None, id_service=None):
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = """
            WITH capacite AS (
                SELECT s.id_service, s.seuil_occupation, COUNT(l.id_lit) AS nb_lits
                FROM services s
                JOIN lit l ON l.id_service = s.id_service
                WHERE (%s IS NULL OR s.id_service = %s)
                GROUP BY s.id_service, s.seuil_occupation
            ),
            evenements AS (
                SELECT l.id_service, m.date_mouvement AS dt, 1 AS delta
                FROM mouvement m
                JOIN lit l ON l.id_lit = m.id_lit
                JOIN capacite c ON c.id_service = l.id_service

                UNION ALL

                SELECT l.id_service, COALESCE(m.date_fin_mouvement, NOW()) AS dt, -1 AS delta
                FROM mouvement m
                JOIN lit l ON l.id_lit = m.id_lit
                JOIN capacite c ON c.id_service = l.id_service
            ),
            cumul AS (
                SELECT id_service, dt,
                    SUM(SUM(delta)) OVER (PARTITION BY id_service ORDER BY dt) AS occupation,
                    LEAD(dt) OVER (PARTITION BY id_service ORDER BY dt) AS dt_suivant
                FROM evenements
                GROUP BY id_service, dt
            ),
            taux AS (
                SELECT cu.id_service, cu.dt, cu.dt_suivant, cu.occupation,
                    c.seuil_occupation,
                    ROUND(cu.occupation / c.nb_lits * 100, 1) AS taux_occupation,
                    ROW_NUMBER() OVER (PARTITION BY cu.id_service ORDER BY cu.dt) AS rn_all
                FROM cumul cu
                JOIN capacite c ON c.id_service = cu.id_service
            ),
            depassements AS (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY id_service ORDER BY dt) AS rn_dep
                FROM taux
                WHERE taux_occupation > seuil_occupation
                AND dt_suivant IS NOT NULL
            ),
            ilots AS (
                SELECT *, rn_all - rn_dep AS grp
                FROM depassements
            )
            SELECT id_service,
                MIN(dt)              AS debut_depassement,
                MAX(dt_suivant)      AS fin_depassement,
                MAX(taux_occupation) AS pic_taux,
                seuil_occupation
            FROM ilots
            GROUP BY id_service, seuil_occupation, grp
            HAVING (%s IS NULL OR MAX(dt_suivant) > %s)
            AND (%s IS NULL OR MIN(dt) < %s)
            ORDER BY id_service, debut_depassement
            """
            valeurs = (id_service, id_service, d1, d1, d2, d2)
            curseur.execute(req, valeurs)
            periodes = curseur.fetchone()

        except Exception as e:
            raise ValueError(f"Erreur de calcul du service avec seuil occupation élevé: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
        return periodes

    



    

    







       
    
            
