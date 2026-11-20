#!/usr/bin/env python3
"""Pick one public-domain black-and-white landscape from Wikimedia Commons and
write responsive grayscale WebP files into public/img/.

Adapted from the desktop wallpaper script in nix-config. Run by hand; the site
itself never calls Commons. Needs ImageMagick (`magick`).

  python3 tools/wallpaper.py                    random pick
  python3 tools/wallpaper.py --list             show candidates, write nothing
  python3 tools/wallpaper.py --title "File:X"   pin a specific file
"""

import argparse
import json
import random
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "letsimpl.fyi-site/0.1 (https://github.com/letsimplfyi/letsimpl.fyi; build tool)"
CATEGORIES = (
    "Black and white photographs of landscapes",
    "Black and white photographs of mountains",
    "Black and white photographs of forests",
    "Black and white photographs of beaches",
    "Black and white photographs of clouds",
)
WIDTHS = (640, 1280, 1920, 2560)
MIN_SOURCE_WIDTH = 2560
FREE = re.compile(r"^(public domain|pd\b|cc0|pdm)", re.I)
EXCLUDE = re.compile(r"\b(war|military|soldiers?|battle|corpse|nude|naked|violence|nara|postcard)\b", re.I)
OUT = Path(__file__).resolve().parent.parent / "public" / "img"


def request(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=60)


def api(**params):
    params.update(action="query", format="json", formatversion=2)
    with request(API + "?" + urllib.parse.urlencode(params)) as response:
        data = json.load(response)
    if "error" in data:
        raise RuntimeError(data["error"].get("info", "Commons API error"))
    return data.get("query", {}).get("pages", [])


def candidates():
    found = []
    for category in CATEGORIES:
        pages = api(generator="categorymembers", gcmtitle="Category:" + category, gcmtype="file",
                    gcmlimit=500, prop="imageinfo", iiprop="size|mime|extmetadata")
        for page in pages:
            info = next(iter(page.get("imageinfo", [])), {})
            meta = info.get("extmetadata", {})
            licence = meta.get("LicenseShortName", {}).get("value", "")
            w, h = info.get("width", 0), info.get("height", 0)
            title = page.get("title", "")
            if (info.get("mime") == "image/jpeg" and h and w >= MIN_SOURCE_WIDTH and 1.4 <= w / h <= 2.2
                    and FREE.search(licence) and not EXCLUDE.search(title)):
                found.append(title)
    return sorted(set(found))


def build(title):
    info = api(titles=title, prop="imageinfo", iiprop="url|size|mime|extmetadata", iiurlwidth=MIN_SOURCE_WIDTH)[0]["imageinfo"][0]
    meta = info.get("extmetadata", {})
    url = info.get("thumburl") or info["url"]
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ("upload.wikimedia.org", "thumb.wikimedia.org"):
        raise RuntimeError("unexpected image host")
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("bg-*.webp"):
        old.unlink()
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "source"
        with request(url) as response, source.open("wb") as out:
            out.write(response.read())
        for width in WIDTHS:
            subprocess.run(["magick", str(source), "-auto-orient", "-colorspace", "Gray", "-resize", f"{width}x",
                            "-strip", "-quality", "58", "-define", "webp:method=6", str(OUT / f"bg-{width}.webp")],
                           check=True, timeout=120)
    credit = {
        "title": title,
        "source": info.get("descriptionurl", ""),
        "artist": re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")),
        "license": meta.get("LicenseShortName", {}).get("value", ""),
        "license_url": meta.get("LicenseUrl", {}).get("value", ""),
        "note": "Converted to grayscale and resized. Public domain / CC0 only, so no attribution is required.",
    }
    (OUT / "CREDIT.json").write_text(json.dumps(credit, ensure_ascii=False, indent=2) + "\n")
    print(title, "-", credit["source"], "-", credit["license"])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--title")
    args = parser.parse_args()
    try:
        if args.title:
            build(args.title)
            return
        choices = candidates()
        if not choices:
            raise RuntimeError("no suitable public-domain image found")
        if args.list:
            print("\n".join(choices))
            return
        build(random.choice(choices))
    except (OSError, ValueError, KeyError, IndexError, RuntimeError, subprocess.SubprocessError) as error:
        print("wallpaper: " + str(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
