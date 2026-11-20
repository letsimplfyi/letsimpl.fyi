#!/usr/bin/env python3
"""Build the taped-on prints from Wikimedia Commons (public domain / CC0 only).

For each slot the first title is the committed fallback: it is downloaded,
converted to grayscale WebP (480 and 960 wide) into public/img/, and credited in
public/img/CREDIT.json. The whole pool is written into public/index.html as
data-pool, so public/js/prints.js can swap in a fresh one live.

Run by hand when the pools change. The site never runs this. Needs ImageMagick
(`magick`):

  nix shell nixpkgs#imagemagick nixpkgs#python3 -c python3 tools/photos.py
"""

import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "img"
INDEX = ROOT / "public" / "index.html"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "letsimpl.fyi-site/0.1 (https://github.com/letsimplfyi/letsimpl.fyi; build tool)"
FREE = re.compile(r"^(public domain|pd\b|cc0|pdm)", re.I)
WIDTHS = (480, 960)

# First title of each pool is the committed fallback.
POOLS = [
    [  # repair
        "File:Dell Inspiron tablet laptop teardown.jpg",
        "File:Repair tool kit.jpg",
        "File:Screwdrivers on a table.JPG",
    ],
    [  # electronics
        "File:Primed and ready forces throughout Atlantic Trident 25 (9138194).jpg",
        "File:Circuit board after manual etching.jpg",
        "File:DEC System Building Block 0107942 component side.jpg",
        "File:Close-up of a VHS Player Circuit Board.jpg",
    ],
    [  # community and making
        "File:Hacker repairs a computer - Linux Day in Torino 2022.jpg",
        "File:Happylab Makerspace.jpg",
        "File:Oxfordshire county library makerspace.jpg",
        "File:Witten Zentralbibliothek Makerspace.jpg",
    ],
]


def request(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=60)


def info(title, width):
    params = dict(action="query", format="json", formatversion=2, titles=title, prop="imageinfo",
                  iiprop="url|extmetadata", iiurlwidth=width)
    with request(API + "?" + urllib.parse.urlencode(params)) as response:
        page = json.load(response)["query"]["pages"][0]
    return page["imageinfo"][0]


def build(slot, title):
    data = info(title, 960)
    meta = data.get("extmetadata", {})
    licence = meta.get("LicenseShortName", {}).get("value", "")
    if not FREE.search(licence):
        raise RuntimeError(f"{title}: licence is {licence!r}, only public domain / CC0 allowed")
    url = data.get("thumburl") or data["url"]
    if urllib.parse.urlparse(url).hostname not in ("upload.wikimedia.org", "thumb.wikimedia.org"):
        raise RuntimeError("unexpected image host")
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "source"
        with request(url) as response:
            source.write_bytes(response.read())
        for width in WIDTHS:
            subprocess.run(["magick", str(source), "-auto-orient", "-colorspace", "Gray", "-resize", f"{width}x",
                            "-strip", "-quality", "60", "-define", "webp:method=6",
                            str(OUT / f"print-{slot}-{width}.webp")], check=True, timeout=120)
    return {
        "slot": slot, "title": title, "source": data.get("descriptionurl", ""),
        "artist": re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")),
        "license": licence, "license_url": meta.get("LicenseUrl", {}).get("value", ""),
    }


def figure(slot, pool):
    attr = "|".join(pool).replace("&", "&amp;").replace('"', "&quot;")
    return (f'  <figure class="print">\n'
            f'    <img src="/img/print-{slot}-960.webp" srcset="/img/print-{slot}-480.webp 480w, /img/print-{slot}-960.webp 960w"\n'
            f'         sizes="320px" width="960" height="720" alt="" decoding="async" loading="eager" data-pool="{attr}">\n'
            f'  </figure>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.webp"):
        old.unlink()
    credits = []
    try:
        for slot, pool in enumerate(POOLS, 1):
            credits.append(build(slot, pool[0]))
            print(slot, pool[0], "-", credits[-1]["license"])
            time.sleep(1)
    except (OSError, ValueError, KeyError, IndexError, RuntimeError, subprocess.SubprocessError) as error:
        print("photos: " + str(error), file=sys.stderr)
        sys.exit(1)
    (OUT / "CREDIT.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2) + "\n")
    html = INDEX.read_text()
    block = "<!-- PRINTS:start -->\n" + "\n".join(figure(i, p) for i, p in enumerate(POOLS, 1)) + "\n  <!-- PRINTS:end -->"
    html, count = re.subn(r"<!-- PRINTS:start -->.*?<!-- PRINTS:end -->", lambda m: block, html, flags=re.S)
    if count != 1:
        raise SystemExit("photos: PRINTS markers not found in public/index.html")
    INDEX.write_text(html)


if __name__ == "__main__":
    main()
