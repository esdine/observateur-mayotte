"""Met a jour _data/meteo.yml avec la meteo reelle de Mamoudzou (Open-Meteo, sans cle).

Execute par la GitHub Action .github/workflows/meteo.yml chaque matin,
ou a la main : python outils/maj_meteo.py
"""
import json
import urllib.request
import datetime
import pathlib
import sys

LAT, LON = -12.78, 45.228  # Mamoudzou
RACINE = pathlib.Path(__file__).resolve().parent.parent

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

# Codes temps WMO -> description courte en francais
CIEL = {
    0: "Ciel dégagé", 1: "Plutôt dégagé", 2: "Partiellement nuageux", 3: "Couvert",
    45: "Brume", 48: "Brouillard givrant",
    51: "Bruine légère", 53: "Bruine", 55: "Bruine dense",
    61: "Pluie faible", 63: "Pluie", 65: "Pluie forte",
    66: "Pluie verglaçante", 67: "Pluie verglaçante forte",
    71: "Neige faible", 73: "Neige", 75: "Neige forte", 77: "Grésil",
    80: "Averses faibles", 81: "Averses", 82: "Averses fortes",
    95: "Orages", 96: "Orages avec grêle", 99: "Orages violents",
}


def api(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def principal():
    prev = api(
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&daily=temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max"
        "&timezone=Indian%2FMayotte&forecast_days=1"
    )
    d = prev["daily"]
    tmax = round(d["temperature_2m_max"][0])
    tmin = round(d["temperature_2m_min"][0])
    ciel = CIEL.get(d["weather_code"][0], "Temps variable")
    vent = round(d["wind_speed_10m_max"][0])

    temp_mer = None
    try:
        mer = api(
            "https://marine-api.open-meteo.com/v1/marine"
            f"?latitude={LAT}&longitude={LON + 0.05}"
            "&hourly=sea_surface_temperature&timezone=Indian%2FMayotte&forecast_days=1"
        )
        valeurs = [v for v in mer["hourly"]["sea_surface_temperature"] if v is not None]
        if valeurs:
            temp_mer = round(sum(valeurs) / len(valeurs))
    except Exception as e:  # la mer est optionnelle, la page s'en passe
        print(f"Marine indisponible : {e}", file=sys.stderr)

    auj = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
    date_affichee = f"{JOURS[auj.weekday()]} {auj.day}{'ᵉʳ' if auj.day == 1 else ''} {MOIS[auj.month - 1]} {auj.year}"

    lignes = [
        "# Genere par outils/maj_meteo.py - source Open-Meteo (donnees reelles)",
        f'date_affichee: "{date_affichee}"',
        f"tmin: {tmin}",
        f"tmax: {tmax}",
        f'ciel: "{ciel}"',
        f"vent_kmh: {vent}",
    ]
    if temp_mer is not None:
        lignes.append(f"temp_mer: {temp_mer}")
    lignes.append(f'maj: "{auj.strftime("%Y-%m-%dT%H:%M%z")}"')

    cible = RACINE / "_data" / "meteo.yml"
    cible.parent.mkdir(exist_ok=True)
    cible.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Ecrit {cible} : {tmin}/{tmax}, {ciel}, vent {vent} km/h, mer {temp_mer}")


if __name__ == "__main__":
    principal()
