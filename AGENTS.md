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
- **Offline-friendly and tiny.** Keep pages light. Everything the site needs
  ships in the repo.

## Design

Follow `DESIGN.md`. It is the source of truth for colour, type, spacing,
components and accessibility. Do not invent new colours, fonts or components
without approval.

## Layout

```
index.html     home page
styles.css     tokens and components
fonts/         self-hosted WOFF2 + OFL notices
DESIGN.md      design and brand book
AGENTS.md      this file
LICENSE        AGPL-3.0
```

Keep it flat. Add a file only when there is a reason.

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
