#!/usr/bin/env bash
# Renderiza el ebook HTML → PDF con Chrome headless (calidad de impresión).
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$DIR/Higado-Ligero.pdf" "file://$DIR/index.html"
echo "OK → $DIR/Higado-Ligero.pdf"
