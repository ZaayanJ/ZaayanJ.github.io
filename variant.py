#!/usr/bin/env python3
"""Render palette + type variants of the page so they can be compared by eye.

Each spec remaps the CURRENT palette values to new ones and swaps the display
face. Output: variants/<name>.html (standalone, compiled CSS inlined).
"""
import json, os, re, shutil, subprocess, sys

CUR = {                      # current (violet / oxblood) values
 'ink':'#08070D', 'well':'#050409', 'raise':'#100B18',
 'cy':'#A855F7', 'eb':'#9F1239', 'ok':'#C084FC',
 'fg':'#EAE4F2', 'mut':'#9C90AE',
 'bright':'#C084FC', 'hover':'#D8B4FE', 'pillhover':'#E9D5FF', 'gradhead':'#E9D5FF',
 'term':'#CFC4DE', 'pill':'#C2B5D4', 'subtle':'#D5CADF', 'dots':'#2A2136', 'warn':'#E8A0B4',
}
CUR_RGBA = {'accent':(168,85,247), 'second':(159,18,57), 'hairline':(186,160,224),
            'status':(192,132,252), 'wellfade':(5,4,9)}
CUR_ORN = {'ring':'rgba(223, 214, 234, .40)', 'hair':'rgba(223, 214, 234, .34)',
           'hook':'rgba(216, 180, 254, .46)', 'fill':'rgba(231, 224, 240, .40)'}

SPECS = [
 {
  'name': 'reliquary',
  'label': 'Bone & blood — Bodoni Moda',
  'display': ('Bodoni Moda', 'bodoni-moda', (700, 900), 'serif'),
  'colors': {
    'ink':'#07070A', 'well':'#030305', 'raise':'#0E0D12',
    'cy':'#C2334D', 'eb':'#7A1026', 'ok':'#E0566E',
    'fg':'#F0ECEE', 'mut':'#9B939A',
    'bright':'#E0566E', 'hover':'#F08898', 'pillhover':'#F6D9DE', 'gradhead':'#F6D9DE',
    'term':'#D8D2D6', 'pill':'#C8C0C5', 'subtle':'#E2DCDF', 'dots':'#2B2126', 'warn':'#E8B0A0',
  },
  'rgba': {'accent':(194,51,77), 'second':(122,16,38), 'hairline':(214,200,206),
           'status':(224,86,110), 'wellfade':(3,3,5)},
  'orn': {'ring':'rgba(236, 230, 232, .42)', 'hair':'rgba(236, 230, 232, .34)',
          'hook':'rgba(224, 86, 110, .55)', 'fill':'rgba(240, 236, 238, .40)'},
 },
 {
  'name': 'foundry',
  'label': 'Iron & ash — Oswald condensed',
  'display': ('Oswald', 'oswald', (600, 700), 'sans-serif'),
  'colors': {
    'ink':'#0A0A0C', 'well':'#050506', 'raise':'#131317',
    'cy':'#8E8AA8', 'eb':'#5A4A63', 'ok':'#B6B1CC',
    'fg':'#EDEDF0', 'mut':'#8E8C99',
    'bright':'#B6B1CC', 'hover':'#D2CFE2', 'pillhover':'#E6E4F0', 'gradhead':'#E6E4F0',
    'term':'#D3D2DC', 'pill':'#BFBDC9', 'subtle':'#DCDAE4', 'dots':'#24242B', 'warn':'#D8B79A',
  },
  'rgba': {'accent':(142,138,168), 'second':(90,74,99), 'hairline':(200,198,214),
           'status':(182,177,204), 'wellfade':(5,5,6)},
  'orn': {'ring':'rgba(226, 225, 235, .40)', 'hair':'rgba(226, 225, 235, .32)',
          'hook':'rgba(182, 177, 204, .52)', 'fill':'rgba(232, 231, 240, .38)'},
 },
 {
  'name': 'blade',
  'display': ('Chakra Petch', 'chakra-petch', (600, 700), 'sans-serif'),
  'label': 'Obsidian & bone — Chakra Petch',
  'colors': {
    'ink':'#06070A', 'well':'#020305', 'raise':'#0D0F14',
    'cy':'#D9DEE8', 'eb':'#8C1C34', 'ok':'#F2F5FA',
    'fg':'#F2F4F8', 'mut':'#8A8F9C',
    'bright':'#F2F5FA', 'hover':'#FFFFFF', 'pillhover':'#FFFFFF', 'gradhead':'#FFFFFF',
    'term':'#CDD2DC', 'pill':'#BCC2CE', 'subtle':'#DDE2EA', 'dots':'#1C2029', 'warn':'#E0A8A0',
  },
  'rgba': {'accent':(217,222,232), 'second':(140,28,52), 'hairline':(200,208,222),
           'status':(242,245,250), 'wellfade':(2,3,5)},
  'orn': {'ring':'rgba(226, 232, 242, .44)', 'hair':'rgba(226, 232, 242, .34)',
          'hook':'rgba(200, 40, 70, .62)', 'fill':'rgba(232, 238, 246, .42)'},
 },
]

os.makedirs('variants', exist_ok=True)
os.makedirs('pvfonts', exist_ok=True)
base = open('page.html').read()
faces_common = open('pvfonts/faces.css').read()

for spec in SPECS:
    page = base
    for key, cur in CUR.items():
        page = page.replace(cur, spec['colors'][key])
    for key, (r, g, b) in CUR_RGBA.items():
        nr, ng, nb = spec['rgba'][key]
        page = re.sub(rf'rgba\(\s*{r},\s*{g},\s*{b}', f'rgba({nr}, {ng}, {nb}', page)
    for key, cur in CUR_ORN.items():
        page = page.replace(cur, spec['orn'][key])

    fam, pkg, weights, fallback = spec['display']
    page = page.replace("display: ['Cinzel', 'Georgia', 'serif'],",
                        f"display: ['{fam}', '{fallback}'],")
    page = page.replace('family=Cinzel:wght@600;700;800;900',
                        f"family={fam.replace(' ', '+')}:wght@{';'.join(str(w) for w in weights)}")
    # Oswald and Chakra Petch have no 900; step the heading weights down
    if 900 not in weights:
        page = page.replace('font-black uppercase', 'font-bold uppercase')

    faces = faces_common
    for w in weights:
        src = f'node_modules/@fontsource/{pkg}/files/{pkg}-latin-{w}-normal.woff2'
        dst = f'pvfonts/{pkg}-latin-{w}-normal.woff2'
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
        faces += (f"\n@font-face{{font-family:'{fam}';src:url('../pvfonts/{pkg}-latin-{w}-normal.woff2')"
                  f" format('woff2');font-weight:{w};font-display:block}}")
    faces = faces.replace("url('pvfonts/", "url('../pvfonts/")

    tmp_page, tmp_cfg = f'.v_{spec["name"]}.html', f'.v_{spec["name"]}.cfg.js'
    open(tmp_page, 'w').write(page)
    cfg = open('tw.config.js').read()
    cfg = cfg.replace("content: ['./index.html']", f"content: ['./{tmp_page}']")
    cfg = cfg.replace("display: ['Cinzel','Georgia','serif']", f"display: ['{fam}','{fallback}']")
    for key in ('ink','well','raise','cy','eb','fg','mut','ok'):
        cfg = re.sub(rf"{key}:'{CUR[key]}'", f"{key}:'{spec['colors'][key]}'", cfg)
    open(tmp_cfg, 'w').write(cfg)

    subprocess.run(['./node_modules/.bin/tailwindcss', '-c', tmp_cfg, '-i', 'tw.css',
                    '-o', f'.v_{spec["name"]}.css', '--minify'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    css = open(f'.v_{spec["name"]}.css').read()

    i = page.index('<div class="substrate"')
    html = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<style>*,*::before,*::after{box-sizing:border-box}html{color-scheme:dark}'
            'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
            + page[:i].replace('<script src="https://cdn.tailwindcss.com"></script>',
                               '<style>' + faces + css + '</style>')
            + '</head><body>' + page[i:] + '</body></html>')
    out = f'variants/{spec["name"]}.html'
    open(out, 'w').write(html)
    print(f'{spec["name"]:10} {spec["label"]}')
    os.remove(tmp_page); os.remove(tmp_cfg); os.remove(f'.v_{spec["name"]}.css')
