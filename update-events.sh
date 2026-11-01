#!/bin/bash
# Lancé chaque jour par le conteneur viserny-events (~/server/docker/services/viserny-events) :
# régénère events.json et le publie sur GitHub Pages s'il a changé.
set -euo pipefail
cd "$(dirname "$0")"
echo "--- $(date '+%F %T')"
git pull --quiet --rebase
python3 -I update-events.py
if git diff --quiet -- events.json; then
  echo "events.json inchangé"
  exit 0
fi
git add events.json
git commit --quiet -m "Événements du $(date +%F)"
git push --quiet
echo "publié"
