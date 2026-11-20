# AGENTS.md

Instructions for AI agents working in this repository. Humans: read this too.

## What this repo is

The website of **letsimpl.fyi**, the org that builds and maintains projects such
as chaikadi.fyi, eatsights and containers_anywhere. It is a simple, static site.
Its subject is the org's goals, mission and values.

This repo lives at the root of the org working directory. Sibling project repos
live in their own folders beside it, each with its own git repo under
https://github.com/letsimplfyi.

## The content rule (non-negotiable)

**Agents write zero content.**

- Do not generate, draft, paraphrase, "improve", translate or placeholder any
  word of copy that appears on the site. That covers headings, goals, mission,
  values, taglines, button labels, alt text, meta descriptions, titles, and
  the 404 page.
- All copy is authored by the founder and approved by the founder before it is
  committed. Copy goes in exactly as given, with no silent edits.
- No lorem ipsum and no "Your text here". If copy is missing, leave the spot
  empty or fail visibly, and ask.
- Agents may build structure, styles, tooling, accessibility and docs about the
  code. That is the limit.
- If unsure whether something counts as content, treat it as content and ask.

## Principles

- **Simple, stupid.** Plain HTML and CSS. No framework, no bundler, no build
  step, no package manager needed to ship. JS only if it earns its place, and
  the site must fully work without it.
- **Repairable.** Anyone should be able to read the whole site in one sitting and
  fix it with a text editor.
- **Neuro-atypical first.** The founder is neuro-atypical, and the site is
  built to meet those needs: low sensory load, predictable layout, short
  lines, one idea per screen, no motion by default, no popups, no autoplay, no
  dark patterns. Complexity is the thing we are against; the site must not
  embody it.
- **No walls.** No paywalls, logins, cookie banners, trackers, analytics or
  third-party requests. Fonts and assets are self-hosted.
  **One approved exception, on principle (see Open data):** `public/js/prints.js`
  may fetch public-domain photos live from Wikimedia Commons (one API request
  per session). It is an enhancement only: every print
  ships a committed fallback photo and must look right when JS is off, the
  visitor is offline or Commons is down. The CSP in `public/_headers` allows
  only that host. Do not add any other third-party request.
- **Open data first.** The org uses and promotes open, freely available data:
  Wikidata, OpenStreetMap, Wikimedia Commons and the like. It encourages its
  users and community to contribute to these commons, does not reinvent the
  wheel, and works in coalition with them to close their gaps. So when the
  site needs data or media, look to the commons first. Using Commons live for
  the background is this principle in practice. Prefer public-domain or CC0
  material, record provenance, and never scrape or hotlink closed sources.
  Any wording about this on the site is the founder's to write.
- **Offline-friendly and tiny.** Keep pages light. Everything the site needs
  ships in the repo.

## Design

Follow `DESIGN.md`. It is the source of truth for colour, type, spacing,
components and accessibility. Do not invent new colours, fonts or components
without approval.

## Layout

```
public/              exactly what Cloudflare Pages serves (no build step)
  index.html         home page
  styles.css         tokens and components
  favicon.svg
  _headers           CSP and caching
  fonts/             self-hosted WOFF2 + OFL notice
  img/               fallback prints (grayscale WebP) + CREDIT.json
  js/prints.js       optional live Commons photos for the prints
tools/photos.py      one-off: builds fallback prints + data-pool from its pools
templates/           page skeletons (not published); community.html for new communities
DESIGN.md            design and brand book
AGENTS.md            this file
LICENSE              AGPL-3.0
```

Keep it flat. Add a file only when there is a reason. Cloudflare Pages
settings: build command `exit 0`, output directory `public`.

## Deploying

`.github/workflows/deploy.yml` checks every push and pull request with
`sh tools/check.sh` (required files, broken links, 25 MiB file limit, only
approved external hosts, CSP not loosened). A push to `main` that passes then
publishes `public/` to the Cloudflare Pages project `letsimpl-fyi` (production
environment, https://letsimpl.fyi). Nothing outside `public/` is published.
Run the check locally before pushing: `sh tools/check.sh`.

One-time setup (needs the founder's Cloudflare account; agents have no access):

1. Create the project: `npx wrangler pages project create letsimpl-fyi --production-branch=main`
2. Create an API token with *Account > Cloudflare Pages > Edit*.
3. Store secrets (repo level, or once at org level `letsimplfyi` for all repos):
   `gh secret set CLOUDFLARE_API_TOKEN -R letsimplfyi/letsimpl.fyi` and
   `gh secret set CLOUDFLARE_ACCOUNT_ID -R letsimplfyi/letsimpl.fyi`
4. In the Pages project, add the custom domain `letsimpl.fyi`.
5. Run the workflow once (push to `main` or *Run workflow*).

The photo pools live in `tools/photos.py` (public domain / CC0 only; it refuses
anything else). Edit them, then run
`nix shell nixpkgs#imagemagick nixpkgs#python3 -c python3 tools/photos.py`
to rebuild the fallbacks and the `data-pool` attributes in `index.html`.
Be gentle with Commons: it rate-limits bursts.

## Working agreements

- License: **AGPL-3.0-or-later**. Keep `LICENSE` intact. Fonts keep their own
  OFL notices.
- Never commit secrets, tokens or keys.
- Small, focused commits with plain messages. Do not push, force-push or
  rewrite history unless asked.
- Do not add dependencies or external requests without approval.
- Validate before handing over: HTML is valid, works with JS off, contrast
  passes (see DESIGN.md), usable at 200% text size and on a phone width.
- Ask when in doubt. Prefer fewer files, fewer lines, fewer ideas.
