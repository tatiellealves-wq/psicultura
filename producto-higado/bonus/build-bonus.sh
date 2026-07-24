#!/usr/bin/env bash
# Renderiza los 4 PDFs bônus (HTML → PDF con Chrome headless).
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
r(){ "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$DIR/$2" "file://$DIR/$1" 2>/dev/null; echo "OK → $2"; }
r 1-licuados.html      "Bonus-1-7-Licuados.pdf"
r 2-alimentos.html     "Bonus-2-20-Alimentos.pdf"
r 3-comer-fuera.html   "Bonus-3-Comer-Fuera.pdf"
r 4-planificador.html  "Bonus-4-Planificador-21-Dias.pdf"
