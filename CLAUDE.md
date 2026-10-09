# zaayanj.github.io — working notes

Personal portfolio for Zaayan Javed. Single-page static site, deployed with GitHub
Pages from `main` at <https://zaayanj.github.io/>.

Working copy: `~/workspace/portfolio`.
Remote: `git@github.com:ZaayanJ/ZaayanJ.github.io.git` (SSH).

> There is a second clone of this same repo at `~/workspace/ZaayanJ.github.io`
> (cloned 25 Sep, no build chain, no `CLAUDE.md`). `~/workspace/portfolio` is the
> one to work in. If the stale clone is still there, delete it — editing the wrong
> one means hand-editing the generated `index.html`, which the next build silently
> discards.

---

## Build: edit `page.html`, never `index.html`

```
page.html  --build.py-->  index.html   (committed; GitHub Pages serves this)
```

`page.html` is the **source of truth**. It is the page *body* plus its own
`<title>`, Google Fonts `<link>`, Tailwind CDN `<script>`, inline
`tailwind.config`, and the `<style>` block. It carries no `<!DOCTYPE>`, `<html>`,
`<head>` or `<body>` — that shell lives in `build.py`, which also owns every
`<head>` concern: description, canonical, favicon link, OpenGraph and Twitter
card tags, `theme-color`, and the CSS reset.

```sh
python3 build.py          # page.html -> index.html (+ preview.html if built.css exists)
open index.html           # the CDN works fine on a normal machine
```

So: content and styling changes go in `page.html`; anything in `<head>` goes in
`build.py`; then rebuild and commit **both** files. `index.html` is generated —
editing it directly gets silently overwritten on the next build.

Invariant worth preserving: `python3 build.py` on a clean checkout reproduces
the committed `index.html` byte for byte. If it doesn't, someone hand-edited
`index.html`.

### The compiled-CSS path (optional, sandbox only)

Tailwind ships via CDN at runtime — that is deliberate and was an explicit
requirement, so **don't convert the site to a compiled stylesheet**. But
`cdn.tailwindcss.com` and Google Fonts are both blocked inside Anthropic's cloud
sandbox, which makes screenshots there render unstyled in Times New Roman. The
workaround, needed only in that environment:

```sh
npm install
python3 fonts.py          # node_modules/@fontsource/* -> pvfonts/ + faces.css
./rebuild.sh              # build -> tailwind compile -> build again
open preview.html         # identical to index.html, with built.css + @font-face inlined
```

`rebuild.sh` runs `build.py` *twice* on purpose: Tailwind's `content` scanner
reads `index.html`, so it must see fresh markup before it compiles, and the
second pass inlines the result into `preview.html`. Getting that order wrong is
why arbitrary utilities (`text-[2.6rem]`, `font-black`) once silently vanished.

`tw.config.js` duplicates the inline `tailwind.config` from `page.html` for that
compile. **The two must be kept in sync by hand** — changing a token in one and
not the other makes the preview lie to you.

`variant.py` renders themed alternatives into `variants/<name>.html` by remapping
the current palette's literal hex/rgba values and swapping the display face. Its
`CUR` dict still holds the *previous* (violet/oxblood) values, so it needs those
updated to the current palette before the next use.

Generated, not committed: `built.css`, `preview.html`, `pvfonts/`, `variants/`,
`node_modules/`, screenshots.

---

## Design system

Theme is **obsidian & bone** — gothic / cybersigilism keeping a technical edge.
Tokens live in two places that must agree: `:root` CSS variables and the
`tailwind.config` `colors` map, both in `page.html` (plus `tw.config.js`).

| Token          | Value     | Role                                              |
| -------------- | --------- | ------------------------------------------------- |
| `ink`          | `#06070A` | page base                                         |
| `well`         | `#020305` | deepest recess                                    |
| `raise`        | `#0D0F14` | panel fill                                        |
| `hair`         | `rgba(200,208,222,0.14)` | hairline rules               |
| `cy`           | `#D9DEE8` | **bone** — primary accent                         |
| `eb`           | `#8C1C34` | **crimson** — secondary accent, ornament, bloom    |
| `fg` / `ok`    | `#F2F4F8` / `#F2F5FA` | body text / brightest text          |
| `mut`          | `#8A8F9C` | muted text                                        |
| `ver`          | `#34D399` | **terminal status green only** — verified ticks, `● LIVE` |

`ver` is scoped tightly on purpose: it belongs to the terminal widget's status
column and nothing else. The timeline `CURRENT` badge stays bone.

Type: **Chakra Petch** (`font-display`, headings, uppercase, tight tracking),
Plus Jakarta Sans (`font-ui`), Inter (`font-sans`, body), JetBrains Mono
(`font-mono`, labels/terminal), UnifrakturMaguntia (`font-sigil`, currently
unused — kept as an escape hatch). Chakra Petch has no 900 weight, so headings
use `font-bold`, not `font-black`.

Custom classes in the `<style>` block: `.substrate` (grid + aurora background),
`.glass`, `.lift` (panel with 3px radius and asymmetric corner brackets via
`::before` top-left / `::after` bottom-right), `.pill`, `.rail` / `.node`
(timeline rail and rotated diamond markers), `.job` (de-carded timeline entry,
separated by a top hairline), `.sigil` + `.sg-*` (SVG ornament), `.rune`
(divider), `.label`, `.navlink`, `.tnum`, `.caret`, `.rise`.

Sections: `#about` (hero + terminal), `#skills`, `#experience` (roles +
education), `#projects` (projects + leadership), `#contact`.

JS is one vanilla block at the end of `page.html`: mobile menu toggle, smooth
scroll, scroll-spy, terminal typing animation, `mailto:` contact form, footer
year. No framework, no bundler.

### Known layout traps

- `#about` needs `position: relative; overflow: hidden` — the sigil SVG
  overflows horizontally without it (desktop scrollWidth went to 1289px).
- Check phone width after any pill or badge change; unwrapped pills were the
  original source of horizontal overflow.
- Tailwind rejects fractional arbitrary spacing like `h-4.5`; use `h-[18px]`.

---

## Content rules

These came from the user directly and should not be re-litigated or "improved":

- Title is **Cybersecurity Engineer** — not "Cybersecurity & Data Engineer".
- No "open to roles" language. He accepted a full-time Charles Schwab role
  (Sep 2026 – present): Data Protection & **Attack** Surface, Secure
  Configuration Management team, Enterprise Vulnerability Management program.
- Experience is **"three years"**, not five. An earlier draft said five; that
  was invented, not inferred from the résumé. Don't restate tenure without
  checking.
- Only claims backed by a real source. The Formance numbers come from the
  capstone deck (3 exercises, 33 landmarks, 4 phases, 94.7% peak validation
  accuracy, ~60% class imbalance handled with class weights and LR scheduling).
  The README's "50 concurrent users" and "sub-100ms" are aspirational and were
  deliberately **excluded**.
- **Formance has no repo link, on purpose.** The real capstone
  (`ayaan-cs/Formance`) is private, and `ZaayanJ/FormanceDemo` is a pristine
  fork of `rishic3/DepthCheck` with zero commits by Zaayan — linking it would
  misrepresent authorship. The footer credit "squat-depth approach referenced
  rishic3/DepthCheck" stays.
- Contact form is `mailto:` by design. The user considered a form backend and
  chose to leave it.
- Club role is "Organizer & mentor"; teammate names and a "team of 3" badge
  were removed at his request.

### Rejected ideas — don't reintroduce

- Skill **tiering** ("expert / proficient / familiar"). Rejected: the tiers were
  inferred rather than stated. Flat pills only.
- The **needle fringe** under the nav. Removed entirely, element and CSS.

---

## Deploy

```sh
python3 build.py
git add -A && git commit -m "..." && git push
```

Then wait — GitHub Pages plus its CDN can serve stale HTML for several minutes.
Verify with `git show origin/main:index.html` before assuming a bug.

(Historical note, now moot: when this work ran from the cloud sandbox, `git push`
had to be done by hand — that VM had no SSH key and no SSH egress. From Claude
Code on the Mac, push works normally.)

Caution on `favicon.svg`: round-tripping SVGs through the cloud file bridge
injected a C2PA metadata block and inflated it from 410 B to ~8 KB. If the file
grows, check for `c2pa` and rewrite it in place.

---

## Related files outside this repo

- `~/Documents/JobApps/Zaayan_Javed_Resume_2026.docx` — résumé source. It is wedged at
  exactly one page: 0.18" margins, and three weak lines were cut to fit (Citgo
  pipelines bullet, Nature Conservancy visualizations bullet, the tooling line).
  Adding anything means removing something. Edited via raw `word/document.xml`
  when `python-docx` wasn't enough; converted with LibreOffice `soffice`.
  `Zaayan_Javed_Resume.pdf` in this repo is the export the Résumé button links to.
- `~/Documents/linkedin/` — LinkedIn banner (1584×396) and the OG card
  (1200×630, committed here as `assets/og-image.jpg`). Both are standalone
  HTML + Playwright screenshot, sharing the site's palette, Chakra Petch, and an
  Austin skyline SVG. Two constraints learned the hard way: the headline needs
  `white-space: nowrap` or it wraps into LinkedIn's mobile photo zone, and the
  atmospheric bloom must be carried by crimson — a bone-dominant bloom renders
  as flat grey.
- `assets/formance-dashboard.jpg` — 1500×360 crop of the analytics dashboard
  from the capstone deck. Chosen over the pose-skeleton frames, which are
  overlaid on stock photography of a person.

---

## Open items

- **Analytics** — never implemented. Cloudflare Web Analytics is the
  recommendation (no cookies, one script tag); needs a token from the user.
- Custom domain (`zaayanjaved.com`) — discussed, deferred.
- Crimson on inline links for affordance — offered, not done. They're currently
  bone, the same colour as body text.
- The Schwab role card is deliberately thin; the user will supply real detail.
- `variant.py`'s `CUR` palette is stale (see above).
