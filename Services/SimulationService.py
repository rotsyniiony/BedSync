from Services.StatService import StatService


class SimulationService:
    """Simulation (phase 7) : lectures et calculs en mémoire uniquement, AUCUNE écriture en base.
    Scénario A : plus d'admissions / B : lits indisponibles / C : réouverture de lits."""

    DUREE_DEFAUT_JOURS = 5.0   # utilisée s'il n'existe aucun séjour terminé (à documenter)

    @classmethod
    def simuler(cls, scenario, id_service, nombre, periode=30):
        lignes = StatService.nb_lits_service() or []
        if id_service is not None:
            lignes = [x for x in lignes if x["id_service"] == id_service]
        disponibles = sum(int(x["DISPONIBLE"] or 0) for x in lignes)
        occupes = sum(int(x["OCCUPE"] or 0) for x in lignes)
        indisponibles = sum(int(x["INDISPONIBLE"] or 0) for x in lignes)

        # durée moyenne de séjour : StatService la donne en heures
        try:
            duree = float(StatService.duree_moyenne_sejour()) / 24
        except Exception:
            duree = cls.DUREE_DEFAUT_JOURS
        if duree <= 0:
            duree = cls.DUREE_DEFAUT_JOURS

        capacite = occupes + disponibles
        journees_occupees = occupes * periode
        capacite_apres, occupees_apres = capacite, journees_occupees
        if scenario == "A":
            occupees_apres = journees_occupees + nombre * duree
        elif scenario == "B":
            capacite_apres = max(0, capacite - nombre)
        elif scenario == "C":
            capacite_apres = capacite + min(nombre, indisponibles)

        def taux(occ, cap):
            return occ / (cap * periode) * 100 if cap > 0 else None

        t0, t1 = taux(journees_occupees, capacite), taux(occupees_apres, capacite_apres)
        affiche = lambda t: "Non calculable" if t is None else f"{t:.1f}"
        resultat = [
            ("Capacité opérationnelle (lits)", capacite, capacite_apres, capacite_apres - capacite),
            ("Journées-lits occupées", round(journees_occupees, 1), round(occupees_apres, 1),
             round(occupees_apres - journees_occupees, 1)),
            ("Taux d'occupation (%)", affiche(t0), affiche(t1),
             "-" if t0 is None or t1 is None else round(t1 - t0, 1)),
        ]

        alertes = []
        if t1 is None:
            alertes.append("Aucun lit opérationnel après simulation.")
        elif t1 > 100:
            alertes.append("Risque de saturation : la demande dépasse la capacité.")
        elif id_service is not None:
            seuils = {x["id_service"]: x["seuil_occupation"]
                      for x in StatService.service_et_seuil_occupations() or []}
            if id_service in seuils and t1 > float(seuils[id_service]):
                alertes.append("Le seuil d'occupation du service serait dépassé.")
        return {"lignes": resultat, "alertes": alertes, "duree_moyenne": duree}
