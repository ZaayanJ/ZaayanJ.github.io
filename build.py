#!/usr/bin/env python3
"""Wrap page.html (the artifact body) into the standalone index.html for GitHub Pages.

page.html carries the content; everything that must live in <head> — social
tags, canonical, favicon — is assembled here so the two stay in sync.
"""
import sys

DESC = ("Cybersecurity engineer at Charles Schwab in Austin. Secure configuration management, "
        "enterprise vulnerability management, full-stack development, and AI systems.")
URL = "https://zaayanj.github.io/"
OG = URL + "assets/og-image.jpg"

HEAD = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{DESC}">
<meta name="author" content="Zaayan Javed">
<meta name="theme-color" content="#0F172A">
<link rel="canonical" href="{URL}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Zaayan Javed">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Zaayan Javed — Cybersecurity Engineer">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{OG}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Zaayan Javed — Cybersecurity Engineer, Austin, Texas. Dark card with the Austin skyline.">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Zaayan Javed — Cybersecurity Engineer">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{OG}">

<style>
  *,*::before,*::after{{box-sizing:border-box}}
  html{{color-scheme:dark}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]{{display:none!important}}
</style>
'''

body = open('page.html').read()
i = body.index('<div class="substrate"')
open('index.html', 'w').write(HEAD + body[:i] + '</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n')

# local preview: swap the Tailwind CDN for the compiled stylesheet
try:
    css = open('built.css').read()
    page = open('index.html').read()
    try:
        faces = open('pvfonts/faces.css').read()
    except FileNotFoundError:
        faces = ''
    open('preview.html', 'w').write(
        page.replace('<script src="https://cdn.tailwindcss.com"></script>', '<style>' + faces + css + '</style>'))
except FileNotFoundError:
    pass

print('built index.html + preview.html')
