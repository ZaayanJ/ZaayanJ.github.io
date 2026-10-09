#!/bin/sh
# page.html -> index.html -> tailwind scan -> preview.html with compiled css
#
# Only needed when cdn.tailwindcss.com is unreachable (the cloud sandbox).
# On a normal machine: python3 build.py, then open index.html.
set -e
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 build.py > /dev/null          # index.html, so tailwind scans fresh markup
./node_modules/.bin/tailwindcss -c tw.config.js -i tw.css -o built.css --minify 2>/dev/null
python3 build.py                      # index.html + preview.html with built.css inlined
