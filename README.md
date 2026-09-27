# L'Observateur de Mayotte — site statique (maquette de démonstration)

Maquette d'un journal en ligne mahorais fictif, au style « broadsheet » des grands quotidiens.
**Ce journal n'existe pas** : tous les articles, signatures, chiffres et adresses sont inventés,
et chaque page l'annonce (bandeau en tête, mentions en pied de page). L'identité visuelle
(sceau hippocampe compris) est une création originale réalisée pour cette maquette.

## Structure

```
index.html            La une (7 rubriques, rail d'opinions, Matinale)
article.html          Gabarit page article (la barge « Karihani »)
tribune.html          Gabarit tribune de la rubrique L'Écho du Lagon
assets/
  style.css           Feuille de style commune (thème clair + sombre automatique)
  favicon.svg/.ico    Favicon hippocampe (SVG moderne + ICO 16/32/64/256)
  apple-touch-icon.png  Icône 256 px pour mobile
  logo-sceau-couleur.svg / -encre.svg / -blanc.svg
  logo-horizontal.svg Sceau + nom, pour en-têtes larges
```

## Aperçu local

```bash
python -m http.server 8080
```

puis ouvrir <http://localhost:8080>. Aucune dépendance, aucun build : du HTML, du CSS,
et quelques lignes de JavaScript (formulaire de démonstration, bouton « Copier le lien »).
Les polices (UnifrakturMaguntia, Libre Franklin) sont chargées depuis Google Fonts ;
sans réseau, le site retombe proprement sur Georgia/Arial.

## Déploiement

Copier le dossier tel quel sur n'importe quel hébergement statique (Nginx/Apache,
GitHub Pages, Netlify, Cloudflare Pages…). Il n'y a ni backend ni base de données :
le formulaire « La Matinale » n'envoie rien (démonstration).

## Identité graphique

La charte complète (sceau, palette avec équivalents thème sombre, typographies,
filets, gabarits, bonnes pratiques) est décrite dans l'artifact « Charte de
L'Observateur ». Palette de référence : encre `#121212`, marine `#14536b`,
turquoise lagon `#2f8fa3`, ambre ylang `#c99036`, lagon pâle `#e9f5f6`.
