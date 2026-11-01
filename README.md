# La maison de Viserny

Site de la famille pour la maison de campagne : météo, sorties à moins de 25 km, consignes d'ouverture et de fermeture.
Publié sur https://viserny.maxteiger.com via GitHub Pages. Le site est public : jamais de code, de cachette de clé ni d'adresse.

- `index.html` : météo (Open-Meteo, côté navigateur) et sorties (lit `events.json`).
- `consignes.html` : arrivée, séjour, départ (d'après les notes manuscrites de la famille, 2026-11). Photos dans `photos/`. Après modification, lancer `./make-pdf.sh` pour régénérer `consignes.pdf` (Chrome headless, styles `@media print`).
- `update-events.py` : régénère `events.json` depuis l'export quotidien DATAtourisme sur data.gouv.fr (Licence Ouverte, sans clé).
- `update-events.sh` : lancé chaque matin sur le Mac Mini par le LaunchAgent `com.max.viserny-events.plist` (copie dans `~/Library/LaunchAgents/`), publie `events.json` s'il a changé. Logs : `~/server/docker/logs/viserny-events.log`.
