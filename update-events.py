#!/usr/bin/env python3
"""Génère events.json : événements à venir à moins de 25 km de Viserny.

Source : export quotidien DATAtourisme (fêtes et manifestations) sur data.gouv.fr,
Licence Ouverte 2.0. Pas de clé nécessaire. Lancé chaque jour par update-events.sh.
"""
import csv
import datetime
import io
import json
import math
import os
import sys
import urllib.request

# Lien stable vers la dernière version de datatourisme-fma.csv
SOURCE = "https://www.data.gouv.fr/fr/datasets/r/2c6023f2-ffce-4c1a-9728-bdc020e463b5"
LAT, LON = 47.5633, 4.2836  # centre de Viserny (geo.api.gouv.fr)
RAYON_KM = 25
SORTIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "events.json")

ETIQUETTES = {
    "Concert": "Concert",
    "Exhibition": "Exposition",
    "Market": "Marché",
    "FleaMarket": "Brocante",
    "GarageSale": "Vide-grenier",
    "SaleEvent": "Vente",
    "ScreeningEvent": "Cinéma",
    "TheaterEvent": "Théâtre",
    "ShowEvent": "Spectacle",
    "DanceEvent": "Danse",
    "Festival": "Festival",
    "SportsEvent": "Sport",
    "Visit": "Visite",
    "GuidedTour": "Visite guidée",
    "ChildrensEvent": "Enfants",
    "Conference": "Conférence",
    "TrainingWorkshop": "Atelier",
    "Game": "Jeu",
    "LocalAnimation": "Animation",
    "TraditionalCelebration": "Fête",
    "ReligiousEvent": "Religieux",
    "Gastronomy": "Gastronomie",
    "WineTasting": "Dégustation",
}

RESEAUX = ("facebook.com", "instagram.com", "twitter.com", "x.com")


def distance_km(lat, lon):
    p = math.radians
    a = (math.sin(p(lat - LAT) / 2) ** 2
         + math.cos(p(LAT)) * math.cos(p(lat)) * math.sin(p(lon - LON) / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(a))


def periodes(texte, aujourdhui):
    """« 2026-11-04<->2026-11-04|2026-11-25<->2026-11-25 » → périodes pas encore finies."""
    res = set()
    for morceau in texte.split("|"):
        debut, _, fin = morceau.partition("<->")
        fin = fin or debut
        if len(debut) == 10 and fin >= aujourdhui:
            res.add((debut, fin))
    return sorted(res)


def lien(contacts):
    """Choisit le lien le plus précis parmi « tel#url<>url|#url » (pas les réseaux sociaux)."""
    urls = []
    for contact in contacts.split("|"):
        _, _, partie = contact.partition("#")
        urls += [u for u in partie.split("<>") if u.startswith("http")]
    bons = [u for u in urls if not any(r in u for r in RESEAUX)] or urls
    return max(bons, key=lambda u: len(u.split("://", 1)[-1].rstrip("/").split("/")), default="")


def etiquettes(categories):
    noms = [c.rsplit("#", 1)[-1].rsplit("/", 1)[-1] for c in categories.split("|")]
    vues = []
    for n in noms:
        e = ETIQUETTES.get(n)
        if e and e not in vues:
            vues.append(e)
    return vues[:3]


def resume(description, limite=180):
    d = " ".join(description.split())
    return d if len(d) <= limite else d[:limite].rsplit(" ", 1)[0] + "…"


def main():
    aujourdhui = datetime.date.today().isoformat()
    requete = urllib.request.Request(SOURCE, headers={"User-Agent": "viserny.maxteiger.com"})
    evenements = {}
    with urllib.request.urlopen(requete, timeout=300) as reponse:
        lecteur = csv.DictReader(io.TextIOWrapper(reponse, encoding="utf-8", newline=""))
        for ligne in lecteur:
            try:
                d = distance_km(float(ligne["Latitude"]), float(ligne["Longitude"]))
            except ValueError:
                continue
            if d > RAYON_KM:
                continue
            p = periodes(ligne["Periodes_regroupees"], aujourdhui)
            if not p:
                continue
            commune = ligne["Code_postal_et_commune"].partition("#")[2]
            titre = " ".join(ligne["Nom_du_POI"].split())
            cle = (titre.lower(), commune)  # même événement publié par deux offices
            evenements[cle] = {
                "titre": titre,
                "commune": commune,
                "km": round(d),
                "periodes": p,
                "types": etiquettes(ligne["Categories_de_POI"]),
                "lien": lien(ligne["Contacts_du_POI"]),
                "resume": resume(ligne["Description"]),
            }
    liste = sorted(evenements.values(), key=lambda e: (e["periodes"][0][0], e["km"]))
    if not liste:
        sys.exit("Aucun événement trouvé : source vide ou format changé, events.json conservé.")
    with open(SORTIE, "w", encoding="utf-8") as f:
        json.dump({"maj": aujourdhui, "rayon_km": RAYON_KM, "evenements": liste},
                  f, ensure_ascii=False, indent=0)
        f.write("\n")
    print(f"{len(liste)} événements écrits dans {SORTIE}")


if __name__ == "__main__":
    main()
