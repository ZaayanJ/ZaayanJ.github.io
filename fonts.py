#!/usr/bin/env python3
"""Populate pvfonts/ from the @fontsource packages so preview.html can render
with real faces when Google Fonts is unreachable (the cloud sandbox blocks it;
on a normal machine you don't need this — just open index.html).

Run after `npm install`. Writes pvfonts/*.woff2 and pvfonts/faces.css.
"""
import os, shutil

# (css family name, @fontsource package, [weights])
FACES = [
    ('UnifrakturMaguntia', 'unifrakturmaguntia', [400]),
    ('Plus Jakarta Sans',  'plus-jakarta-sans',  [500, 700, 800]),
    ('Inter',              'inter',              [400, 500, 600]),
    ('JetBrains Mono',     'jetbrains-mono',     [400, 500, 700]),
    ('Chakra Petch',       'chakra-petch',       [600, 700]),
]

os.makedirs('pvfonts', exist_ok=True)
lines, missing = [], []
for family, pkg, weights in FACES:
    for w in weights:
        name = f'{pkg}-latin-{w}-normal.woff2'
        src, dst = f'node_modules/@fontsource/{pkg}/files/{name}', f'pvfonts/{name}'
        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy(src, dst)
        elif not os.path.exists(dst):
            missing.append(src)
            continue
        lines.append(f"@font-face{{font-family:'{family}';src:url('pvfonts/{name}')"
                     f" format('woff2');font-weight:{w};font-display:block}}")

open('pvfonts/faces.css', 'w').write('\n'.join(lines) + '\n')
print(f'wrote pvfonts/faces.css ({len(lines)} faces)')
if missing:
    print('missing (run npm install):')
    for m in missing:
        print('  ' + m)
