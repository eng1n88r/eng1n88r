# Profile README candidates

Three styles to compare. Nothing is live yet — `README.md` on `main` is untouched.

- [A — dark HUD, restrained](README-a-hud.md)
- [B — full neon](README-b-neon.md)
- [C — pure terminal](README-c-terminal.md)

Pick one and it becomes `README.md`; the other two and their unused assets get deleted.

## Why the old stats card was unreliable

The previous README pointed at a live endpoint (`vercel-git-main-eng1n88r.vercel.app`).
Every view cold-started a serverless function and hit the GitHub GraphQL API, so it
was slow when it worked and blank when it did not. The upstream public instance
currently returns 503, and two other popular widgets have gone the same way —
`github-profile-trophy` and `github-readme-activity-graph` both answer 402 now.

Everything in `assets/` is a static SVG committed to this repo instead. It cannot
rate-limit, cold-start, or start charging.

## Why the cards were rendering blank

github-readme-stats reveals its content with CSS (`.stagger { opacity: 0; animation:
fadeInAnimation ... }`). If those animations do not run, the card is a correctly-sized
but empty box — which looks exactly like "still loading".

`scripts/bake-svg-animations.py` rewrites each `animation:` declaration into the `to {}`
block of its `@keyframes`, so the finished state is what ships. The workflow runs it on
every regeneration.

## Regeneration

`.github/workflows/profile-assets.yml` rebuilds every asset nightly and commits the
result. It needs a `PROFILE_TOKEN` repository secret: a classic PAT with `repo` and
`read:user`. The workflow's own `GITHUB_TOKEN` cannot reach the stats GraphQL API — it
comes back "Resource not accessible by integration" and renders an error card, so the
job now checks for that and fails rather than committing it.

## Typography and palette

Lettering is Chakra Petch, converted to outlines by `scripts/build-neon-assets.py`.
A webfont cannot load inside an SVG that GitHub serves as an `<img>` — raw.githubusercontent.com
sends `default-src 'none'`, which blocks `@import` and data-URI `@font-face` alike — and naming
the family in `font-family` only works for viewers who happen to have it installed. Outlines
travel with the file. Chakra Petch is OFL-licensed; the licence is in `assets/fonts/`.

Colours follow the GTA VI marketing palette: a Miami sunset (gold `#FFC24B`, orange `#FF9142`,
pink `#FF3D7F`, magenta `#C42A8E`) over deep violet night (`#0B0518`, `#1A0B33`), with teal
`#37D6C4` as the single cool accent.

Re-run after editing copy or colours:

    scripts/build-neon-assets.py --fonts <dir with ChakraPetch-*.ttf>
