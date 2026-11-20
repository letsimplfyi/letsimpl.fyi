# letsimpl.fyi design and brand book · v0.1

**Build source of truth for the org site.** It inherits the system from
chaikadi.fyi (v0.3): a black-and-white wireframe, a hyperlegible monospace,
and crayon colour only where it means something. This book carries over what
applies to a static content site and drops the app-specific parts (receipts,
tabs, sheets, PeerJS and so on).

This document contains **no site copy**. All words on the site are written and
approved by the founder (see `AGENTS.md`).

## Intent

Peak simplicity. The site acknowledges the neuro-atypicality of its founder
and works to reduce those challenges for readers. In practice that means:

- One column, one idea at a time, predictable structure.
- Nothing moves, flashes, pops up or asks for attention.
- Plain high contrast, large type, generous space.
- No hidden state: no menus that hide pages, no carousels, no accordions
  unless they are native and optional.

## Decisions

| Decision | Selected |
| --- | --- |
| Page | Pure white `#FFFFFF` (light), pitch black `#000000` (dark) |
| Type | Atkinson Hyperlegible Mono 400 / 700, self-hosted WOFF2 |
| Colour | Crayon only, with meaning (below); everything else black and white |
| Theme | Light and Dark. Follows the device via `prefers-color-scheme`; no JS needed |
| Build | None. Hand-written HTML and one `styles.css` |
| Third parties | None. No analytics, no CDNs, no external fonts |
| Language | English first. Copy supplied by the founder only |
| Motion | None by default |

## Crayon colour = meaning

Soft hand-coloured wax fills, used sparingly. Text on crayon is always
`#111111`. Colour never works alone: each crayon also carries a word or shape.

| Crayon | Hex | Only for |
| --- | --- | --- |
| Yellow | `#FFE066` | The slip in the wordmark: the dot and the **i** that swapped places |
| Blue | `#9FCBFF` | Outbound: links that leave the site (for example project repos) |
| Green | `#A7E3A0` | The one forward action on a page, if there is one |

Hex values match chaikadi.fyi for a shared family look. Meanings may be
refined by the founder; do not add a crayon or reuse one for decoration.

## Palette

| Token | Light | Dark |
| --- | --- | --- |
| `--page` | #FFFFFF | #000000 |
| `--ink` | #000000 | #FFFFFF |
| `--muted` | #4D4D4D | #B8B8B8 |
| `--line` | #8C8C8C | #767676 |
| `--crayon-ink` | #111111 | #111111 |

Controls and key rules use a 2px ink border. Square corners, except crayon
fills which may have a very slight hand-cut radius (`2px 3px 2px 4px`). No
shadows, gradients (other than the crayon hatch texture) or translucency.

## Crayon texture

Crayon fills are a flat colour with a faint diagonal wax hatch, as in
chaikadi.fyi:

```css
background-image: repeating-linear-gradient(115deg,
  rgb(255 255 255 / 22%) 0 1.5px, transparent 1.5px 4px,
  rgb(0 0 0 / 5%) 4px 5px, transparent 5px 7px);
```

## Type and grid

Atkinson Hyperlegible Mono has distinct 0/O and 1/I/l. Font files come from
chaikadi.fyi's `fonts/` (with their OFL notices) and stay in this repo.
Fallback: `ui-monospace, "Courier New", monospace`.

| Role | Size / line height |
| --- | --- |
| Page title | 32 / 40 (1.75rem of an 18px root) |
| Section heading | 22 / 30 |
| Subheading | 18 / 28 |
| Body | 18 / 28 |
| Secondary | 16 / 24 |
| Smallest (optional text only) | 14 / 20 |

- Root size 18px; sizes are rem-based. Respect user text scaling.
- Measure: 560px maximum for prose (about 60 characters), 16px side padding on
  phones, 24px from 600px.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64px.
- Left-align everything. Two weights only (400 and 700). Sentence case.
- Page titles carry a 2px ink rule beneath.
- Links are underlined, ink-coloured, with 4px offset. Never colour-only.

## Wordmark

"let's simplify" is written `letsimpl.fyi`: the **i** slid to the end and a
dot was left in its place, as if typed by a dyslexic hand. Like the arrow in
Amazon's a-to-z, the mark owns the slip instead of hiding it: the clumsiness
is visible, and so is the recovery. Both slipped glyphs (`.` and `i`) sit on
yellow crayon, and a hand-drawn ink arrow carries the **i** back to the dot.

- Real text in the DOM (`aria-label="letsimpl.fyi"` on the link); the arrow is
  an `aria-hidden` SVG. Still, never animated.
- Set in the monospace so `ch` units line the arrow up under columns 9 and 12.
- Ink arrow, not crayon: the yellow alone would fail 3:1 graphics contrast.
- It is the `h1` on the home page; the founder's copy follows it.

## Background photo

A decorative, always-grayscale photo sits behind a solid panel, so text never
sits on the photo and contrast is guaranteed on any image.

- Source: Wikimedia Commons, public domain or CC0 only (no attribution needed;
  provenance is recorded in `public/img/CREDIT.json`).
- Fallback is committed in four widths (640 / 1280 / 1920 / 2560, WebP) via
  `srcset`. `js/bg.js` may swap in a fresh one live; see `AGENTS.md`.
- Fixed `<img>` with `object-fit: cover`, not `background-attachment: fixed`
  (broken on iOS). Dimmed to 50% in dark mode. Hidden in forced-colors and print.
- Skipped when the browser asks to save data.

## Layout

- Single column, no sidebars, no sticky or fixed elements.
- Home page shows peak simplicity: very little on screen, and a clear
  reading order that matches the DOM order.
- Navigation, if any, is a plain list of real links at the top of the page,
  visible always (no hamburger).
- Pages are separate HTML files; no client-side routing.

## Motion

None by default. Hover/focus state changes take 120ms at most and carry no
movement. If motion is ever added it must honour `prefers-reduced-motion`
and never carry meaning on its own.

## Accessibility

Built for neuro-atypical readers first, so these are the floor, not the goal.

- Text contrast ≥4.5:1 (large text ≥3:1); control edges ≥3:1.
- Touch targets ≥44px (48px preferred), 8px gaps.
- 3px ink focus outline with 3px offset; visible on every interactive element.
- Semantic landmarks (`header`, `main`, `footer`), a single `h1`, no skipped
  heading levels, a skip link.
- Works with JavaScript disabled; works at 200% text size and at 320px width.
- Declare `color-scheme` and `<meta name="theme-color">` for both themes.
- No autoplay, popups, timers, or cookie banners.
- Every image has meaningful alt text supplied by the founder, or empty alt
  when purely decorative.

## Implementation notes

- Files live in `public/`: `index.html`, `styles.css`, `fonts/`, `img/`, `js/`.
  No build step.
- Tokens as CSS custom properties on `:root`, with dark overrides under
  `@media (prefers-color-scheme: dark)`.
- Hosting: any static host. Add `CNAME` only when the domain is set up.
- Fonts under 150 KB total; subset to Latin.
