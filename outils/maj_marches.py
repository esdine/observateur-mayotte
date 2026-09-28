"""Met a jour _data/marches.yml : derniers appels d'offres publics pour Mayotte.

Source : open data du BOAMP (boamp-datadila.opendatasoft.com), donnees publiques
sous licence ouverte - la reutilisation est autorisee avec mention de la source.
Chaque entree renvoie vers l'avis officiel sur boamp.fr.

Execute par la GitHub Action quotidienne, ou a la main :
python outils/maj_marches.py
"""
import json
import pathlib
import sys
import urllib.parse
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
NOMBRE = 6

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

API = "https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records"


def date_fr(iso):
    """'2026-10-30T12:00:00+00:00' ou '2026-10-30' -> '30 octobre 2026'."""
    if not iso:
        return None
    j = iso[:10]
    try:
        a, m, q = j.split("-")
        return f"{int(q)} {MOIS[int(m) - 1]} {a}"
    except Exception:
        return j


def principal():
    params = {
        "where": 'code_departement="976" AND nature="APPEL_OFFRE"',
        "order_by": "dateparution desc",
        "limit": str(NOMBRE),
        "select": "idweb,objet,nomacheteur,type_marche_facette,famille_libelle,dateparution,datelimitereponse,url_avis",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (edition du matin)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        donnees = json.load(r)

    avis = []
    for e in donnees.get("results", []):
        objet = (e.get("objet") or "").strip()
        if len(objet) > 140:
            objet = objet[:137].rstrip() + "…"
        types = e.get("type_marche_facette") or []
        avis.append({
            "objet": objet,
            "acheteur": (e.get("nomacheteur") or "Acheteur non précisé").strip(),
            "type": types[0] if types else "Marché public",
            "famille": e.get("famille_libelle") or "",
            "parution": date_fr(e.get("dateparution")),
            "limite": date_fr(e.get("datelimitereponse")),
            "lien": e.get("url_avis") or f"https://www.boamp.fr/pages/avis/?q=idweb:{e.get('idweb', '')}",
        })

    if not avis:
        print("Aucun avis renvoye : _data/marches.yml laisse en l'etat.", file=sys.stderr)
        return

    lignes = [
        "# Genere par outils/maj_marches.py - source BOAMP (open data, licence ouverte)",
        "avis:",
    ]
    for a in avis:
        lignes.append(f"  - objet: {json.dumps(a['objet'], ensure_ascii=False)}")
        for cle in ("acheteur", "type", "famille", "parution", "limite", "lien"):
            if a[cle]:
                lignes.append(f"    {cle}: {json.dumps(a[cle], ensure_ascii=False)}")

    cible = RACINE / "_data" / "marches.yml"
    cible.parent.mkdir(exist_ok=True)
    cible.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Ecrit {cible} : {len(avis)} avis.")


if __name__ == "__main__":
    principal()
