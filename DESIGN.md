# Design

**https://brand.letsimpl.fyi is the source of truth for the design.** Colour,
type, spacing, components and accessibility are defined there, not here.

The site vendors the brand's plain files, unedited:

- `public/tokens/tokens.css`
- `public/css/base.css`
- `public/css/components.css`
- `public/fonts/` (the brand's WOFF2 files)

To update, re-fetch them from the brand site (`/tokens/tokens.css`,
`/css/base.css`, `/css/components.css`, `/fonts/*`). Do not edit them here.

`public/styles.css` is the site layer only: page layout built from brand tokens.
Use the brand's `ls-` components and tokens. Do not add colours, fonts or
components of our own. If the brand lacks something, change the brand first.

This file contains no site copy. All words are the founder's (see `AGENTS.md`).
