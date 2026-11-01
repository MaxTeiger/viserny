# La maison de Viserny

Site de la famille pour la maison de campagne : météo, sorties à moins de 25 km, consignes d'ouverture et de fermeture.
Publié sur https://viserny.maxteiger.com via GitHub Pages. Le site est public : jamais de code, de cachette de clé ni d'adresse.

- `index.html` : météo (Open-Meteo, côté navigateur) et sorties (lit `events.json`).
- `consignes.html` : étapes pour ouvrir et fermer la maison. Mode d'emploi pour compléter en commentaire en haut du fichier ; photos dans `photos/`.
- `update-events.py` : régénère `events.json` depuis l'export quotidien DATAtourisme sur data.gouv.fr (Licence Ouverte, sans clé).
- `update-events.sh` : lancé chaque matin sur le Mac Mini par `~/Library/LaunchAgents/com.max.viserny-events.plist`, publie `events.json` s'il a changé. Logs : `~/server/docker/logs/viserny-events.log`.
