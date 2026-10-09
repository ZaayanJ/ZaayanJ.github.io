# zaayanj.github.io

Personal portfolio — cybersecurity engineering, development, and AI systems.
Live at <https://zaayanj.github.io/>.

Static single page: HTML + Tailwind CSS (CDN) + vanilla JavaScript.

- `page.html` — **source of truth** (body, styles, inline Tailwind config, JS)
- `build.py` — wraps `page.html` into `index.html` and owns the `<head>`
- `index.html` — generated, committed, served by GitHub Pages. Don't edit it.
- `favicon.svg`, `assets/`, `Zaayan_Javed_Resume.pdf`

```sh
python3 build.py && open index.html
```

Deployed with GitHub Pages from `main`. See `CLAUDE.md` for the design tokens,
the optional compiled-CSS preview path, and the content rules.
