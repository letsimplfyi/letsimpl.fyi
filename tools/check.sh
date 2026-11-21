#!/bin/sh
# Sanity checks for public/. Runs locally (`sh tools/check.sh`) and in CI before
# every deploy. Fails on anything that would break the site's own rules.
set -eu
cd "$(dirname "$0")/.."

fail=0
bad() { echo "FAIL: $*" >&2; fail=1; }

# Required files.
for f in index.html styles.css tokens/tokens.css css/base.css css/components.css favicon.svg _headers fonts/Atkinson-Hyperlegible-Mono.OFL.txt img/CREDIT.json; do
  [ -f "public/$f" ] || bad "public/$f is missing"
done

# Cloudflare Pages limits a single file to 25 MiB.
big=$(find public -type f -size +25M)
[ -z "$big" ] || bad "files over 25 MiB: $big"

# Every local src/href in the HTML points at a file that exists.
for page in $(find public -name '*.html'); do
  grep -oE '(src|href)="/[^"#]*"' "$page" | sed -E 's/^[a-z]+="//; s/"$//; s/\?.*$//' | sort -u | while read -r p; do
    [ "$p" = "/" ] && continue
    [ -e "public$p" ] || { echo "FAIL: $page links to $p, which does not exist" >&2; exit 1; }
  done || fail=1
done

# Page basics.
grep -q '<html lang="' public/index.html || bad "index.html has no lang attribute"
grep -q '<title>' public/index.html || bad "index.html has no title"

# No third-party requests beyond the approved ones (see AGENTS.md).
allowed='^(commons\.wikimedia\.org|upload\.wikimedia\.org|thumb\.wikimedia\.org|github\.com|chaikadi\.fyi|eatsights\.letsimpl\.fyi|letsimpl\.fyi|www\.w3\.org)$'
hosts=$(grep -rhoE --include='*.html' --include='*.css' --include='*.js' --include='*.svg' 'https?://[^"'"'"' )<>]+' public | sed -E 's#^https?://([^/:]+).*#\1#' | sort -u)
for h in $hosts; do
  echo "$h" | grep -Eq "$allowed" || bad "unapproved external host: $h"
done

# The CSP must exist and must not allow scripts from anywhere but this site.
grep -q 'Content-Security-Policy' public/_headers || bad "_headers has no Content-Security-Policy"
grep -E "script-src [^;]*(https?:|\*|unsafe)" public/_headers >/dev/null && bad "script-src is too loose" || true

[ "$fail" -eq 0 ] && echo "ok: public/ passes all checks"
exit "$fail"
