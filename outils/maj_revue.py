"""Met a jour _data/revue.yml : revue de presse des medias mahorais.

Principe juridique strict : on ne conserve QUE le titre et le lien de chaque
article (pas d'extrait, pas de description, pas d'image) et le lecteur est
renvoye vers le site de la redaction. Aucun contenu n'est reproduit.

Execute par la GitHub Action quotidienne, ou a la main :
python outils/maj_revue.py
"""
import json
import pathlib
import sys
import urllib.request
import xml.etree.ElementTree as ET

RACINE = pathlib.Path(__file__).resolve().parent.parent
PAR_SOURCE = 4

SOURCES = [
    ("Mayotte Hebdo", "https://mayottehebdo.com/feed/"),
    ("Le Journal de Mayotte", "https://lejournaldemayotte.yt/feed/"),
    ("L'Info Kwezi", "https://www.linfokwezi.fr/feed/"),
]


def lire_flux(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (revue de presse)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        racine = ET.fromstring(r.read())
    articles = []
    # RSS 2.0 : rss/channel/item ; Atom : feed/entry
    for item in racine.iter("item"):
        titre = (item.findtext("title") or "").strip()
        lien = (item.findtext("link") or "").strip()
        if titre and lien.startswith("http"):
            articles.append((titre, lien))
        if len(articles) >= PAR_SOURCE:
            break
    if not articles:
        atom = "{http://www.w3.org/2005/Atom}"
        for entry in racine.iter(f"{atom}entry"):
            titre = (entry.findtext(f"{atom}title") or "").strip()
            lien_el = entry.find(f"{atom}link")
            lien = lien_el.get("href", "") if lien_el is not None else ""
            if titre and lien.startswith("http"):
                articles.append((titre, lien))
            if len(articles) >= PAR_SOURCE:
                break
    return articles


def principal():
    lignes = [
        "# Genere par outils/maj_revue.py - titres et liens seulement, aucun contenu reproduit",
        "sources:",
    ]
    total = 0
    for nom, url in SOURCES:
        try:
            articles = lire_flux(url)
        except Exception as e:
            print(f"{nom} indisponible : {e}", file=sys.stderr)
            continue
        if not articles:
            print(f"{nom} : flux vide", file=sys.stderr)
            continue
        site = "/".join(url.split("/")[:3]) + "/"
        lignes.append(f"  - nom: {json.dumps(nom, ensure_ascii=False)}")
        lignes.append(f"    site: {json.dumps(site, ensure_ascii=False)}")
        lignes.append("    titres:")
        for titre, lien in articles:
            lignes.append(f"      - titre: {json.dumps(titre, ensure_ascii=False)}")
            lignes.append(f"        lien: {json.dumps(lien, ensure_ascii=False)}")
        total += len(articles)

    if total == 0:
        print("Aucune source disponible : _data/revue.yml laisse en l'etat.", file=sys.stderr)
        return

    cible = RACINE / "_data" / "revue.yml"
    cible.parent.mkdir(exist_ok=True)
    cible.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Ecrit {cible} : {total} titres.")


if __name__ == "__main__":
    principal()
