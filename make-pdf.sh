#!/bin/bash
# Régénère consignes.pdf à partir de consignes.html (Chrome headless, styles @media print).
set -euo pipefail
cd "$(dirname "$0")"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="$PWD/consignes.pdf" "file://$PWD/consignes.html" 2>/dev/null
echo "consignes.pdf : $(du -h consignes.pdf | cut -f1)"
