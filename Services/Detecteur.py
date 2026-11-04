from Models.LitModel import *
from Models.PatientModel import *
from Models.ServiceModel import *
from Models.SejourModel import *
from Models.MouvementModel import *
from Models.IndispoModel import *
from datetime import *

class Detecteur():
    def __init__(self):
        pass

    @classmethod
    def D_lit_occupe_no_sejour():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT l.id_lit, l.code_lit, l.id_service FROM lits l JOIN service d ON l.id_service = d.id_service" \
            "WHERE l.etat_lit = %s " \
            "AND NOT EXISTS" \
            "(SELECT 1 FROM mouvement m " \
            "JOIN sejour s ON s.id_sejour = m.id_sejour " \
            "WHERE m.id_lit = l.id_lit " \
            "AND m.date_fin_mouvement IS NULL " \
            "AND s.statut = %s)"
            valeurs = ("OCCUPE", "EN_COURS")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de lecture des lits occupés sans séjours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
            if(liste == []):
                raise ValueError("Aucun lit occupé sans séjour en cours")
            elif(liste != []):
                for x in liste.items():
                    raise ValueError(f"Lit occupé sans séjour en cours -> code: {x['code_lit']} du service  {x['nom_service']}|  id: {x['id_lit']}")

    @classmethod
    def D_sejour_cours_no_lit():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req = "SELECT s.id_sejour, p.code_patient, s.id_lit FROM sejour s JOIN patient p ON s.id_patient = p.id_patient" \
            "WHERE s.statut_sejour = %s" \
            "AND NOT EXISTS" \
            "(SELECT 1 FROM mouvement m" \
            "JOIN lit l ON m.id_lit = l.id_lit WHERE m.id_sejour = s.id_sejour AND " \
            "m.date_fin_mouvement IS NULL AND" \
            "l.etat_lit = %s)"
            valeurs = ("EN_COURS", "OCCUPE")
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de lecture des lits occupés sans séjours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
            if(liste == []):
                raise ValueError("Séjour en cours sans lit occupé")
            elif(liste != []):
                for x in liste.items():
                    raise ValueError(f"Séjour en cours sans lit occupé: {x['id_sejour']} sur lit {x['id_lit']}")

    @classmethod
    def deux_sejours_meme_lit():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT m.id_lit,
                    GROUP_CONCAT(m.id_sejour ORDER BY m.id_sejour) AS sejours,
                    COUNT(*) AS nb_sejours
                FROM mouvement m
                JOIN sejour s ON s.id_sejour = m.id_sejour
                WHERE m.date_fin_mouvement IS NULL
                    AND s.statut_sejour = %s
                GROUP BY m.id_lit
                HAVING COUNT(*) > 1
            """
            valeurs = ("EN_COURS",)
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de lecture des lits occupés sans séjours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
            if(liste == []):
                raise ValueError("Séjour sur un même lit")
            elif(liste != []):
                for x in liste.items():
                    raise ValueError(f"Les séjours sur un même lit : sur {x['id_lit']} on a {x['sejours']} donc {x['nb_sejours']}")

    @classmethod
    def mouvements_chevauchent():
        liste = []
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True, buffered=True)
            req= """ 
                SELECT m1.id_lit,
                    m1.id_mouvement,
                    COUNT(m2.id_mouvement) AS nb_chevauchements
                    GROUP_CONCAT(m2.id_mouvement ORDER BY m2.id_mouvement) AS en_conflit
                FROM mouvement m1
                JOIN mouvement m2 ON m2.id_lit = m1.id_lit AND m2.id_mouvement <> m1.id_mouvement WHERE m1.date_mouvement < COALESCE(m2.date_fin_mouvement , %s) AND m2.date_mouvement < COALESCE(m1.date_fin_mouvement, %s)
                GROUP BY m1.id_lit, m1.id_mouvement
            """
            valeurs = (datetime.today(), datetime.today())
            curseur.execute(req, valeurs)
            liste = curseur.fetchall()
            ma_connexion.commit()
        except Exception as e:
            print(f"Erreur de lecture des lits occupés sans séjours: {e}")
        finally:
            curseur.close()
            ma_connexion.close()
            if(liste == []):
                raise ValueError("Les séjours qui se chevauchent")
            elif(liste != []):
                for x in liste.items():
                    raise ValueError(f"Les séjours qui se chevauchent: sur {x['id_lit']} de {x['id_mouvement']} par les séjours {x['en_conflits']} donc {x['nb_chevauchements']}")
    
