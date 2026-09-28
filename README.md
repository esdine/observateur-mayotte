# L'Observateur de Mayotte — site Jekyll (maquette de démonstration)

Maquette d'un journal en ligne mahorais fictif, au style « broadsheet » des grands quotidiens.
**Ce journal n'existe pas** : tous les articles, signatures, chiffres et adresses sont inventés,
et chaque page l'annonce (bandeau en tête, mentions en pied de page). L'identité visuelle
(sceau hippocampe compris) est une création originale réalisée pour cette maquette.

Site en ligne : <https://esdine.github.io/observateur-mayotte/> — construit par le
Jekyll natif de GitHub Pages (branche `gh-pages`), sans aucune installation locale.

## Structure

```
index.html            La une (art dirigée à la main + bande « Dernières publications » automatique)
_config.yml           Configuration Jekyll (baseurl, permaliens des futurs articles)
_posts/               LES ARTICLES — un fichier Markdown par papier
_layouts/
  article.html        Gabarit page article (chapô, signature, lettrine, Repères…)
  tribune.html        Gabarit tribune L'Écho du Lagon (bandeau vague, auteur en tête…)
_includes/            Briques partagées : head, note démo, nav compacte, pied de page
assets/               style.css (thème clair + sombre), logos, favicons
```

## Ajouter un article

Créer `_posts/AAAA-MM-JJ-mon-slug.md` :

```markdown
---
layout: article            # ou « tribune » pour L'Écho du Lagon
title: "Titre de l'article"
date: 2026-10-05
date_affichee: "5 octobre 2026"
heure: "06 h 00"
rubrique: "Économie"
chapo: "Le chapô en une ou deux phrases."
auteur: "Prénom Nom"
initiales: "PN"
bio_auteur: "Une ligne de présentation."   # gabarit article
# qualite: "Économiste."                   # gabarit tribune (remplace bio_auteur)
lecture: "4 min"
etiquettes: [Mot-clé, Autre]
---

Le corps de l'article en Markdown. Les blocs spéciaux (exergue, Repères,
Lire aussi) s'écrivent en HTML avec les classes de la charte, voir les
deux articles existants en modèle.
```

Le nouvel article apparaît automatiquement dans « Dernières publications »
sur la une et dans « À lire ensuite » des autres articles. Les rubriques de
la une elle-même restent choisies à la main (c'est une page art dirigée).

## Publier

```bash
git add . ; git commit -m "..." ; git push origin main main:gh-pages
```

GitHub Pages reconstruit le site en une minute environ. Les deux premiers
articles gardent leurs adresses historiques (`/article.html`, `/tribune.html`) ;
les suivants sortiront en `/articles/<slug>.html`.

## Aperçu local (facultatif)

Sans Ruby/Jekyll sur le poste, l'aperçu fidèle se fait sur une branche de
test poussée sur `gh-pages`, ou en installant Jekyll (`gem install jekyll`)
puis `jekyll serve`. Le HTML statique seul (`python -m http.server`) ne
rend plus les gabarits, puisque les pages passent par Liquid.

## Météo réelle (première donnée non fictive)

Le bloc « Le temps à Mamoudzou » de la une est alimenté par `_data/meteo.yml`,
mis à jour chaque matin (05 h 45 heure de Mayotte) par la GitHub Action
`.github/workflows/meteo.yml` : elle exécute `outils/maj_meteo.py` (Open-Meteo,
API ouverte sans clé — températures, ciel, vent, température de l'eau), commite
le fichier si la météo a changé et pousse `main` + `gh-pages`. Lancement manuel
possible depuis l'onglet Actions (« Météo quotidienne » → Run workflow).
La date affichée en tête de une vient du même fichier. Les horaires de marées
(données SHOM, payantes) ne sont pas affichés tant qu'ils ne sont pas réels.
NB : GitHub désactive les crons après 60 jours sans activité sur le dépôt ;
un simple commit ou un lancement manuel les réactive.

## Identité graphique

La charte complète (sceau, palette avec équivalents thème sombre, typographies,
filets, gabarits, bonnes pratiques) est décrite dans l'artifact « Charte de
L'Observateur ». Palette de référence : encre `#121212`, marine `#14536b`,
turquoise lagon `#2f8fa3`, ambre ylang `#c99036`, lagon pâle `#e9f5f6`.
