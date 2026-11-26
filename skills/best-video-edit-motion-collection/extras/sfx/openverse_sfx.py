"""Search and download openly licensed sound effects from the Openverse API, with a credits file.

Standard library only. Usage:
  python openverse_sfx.py search "whoosh" [--license cc0,by] [--max-sec 3] [--limit 15]
  python openverse_sfx.py get "whoosh" --count 3 --out ./sfx [--license cc0] [--max-sec 3]
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openverse.org/v1/audio/"
UA = "openverse-sfx-skill/1.0"
SAFE_DEFAULT = "cc0,pdm,by"


def fetch_json(url, tries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))  # the API sometimes answers 500 for a moment


def search(q, licence, category, source, page_size):
    """One query per licence, merged: the API intermittently fails on long licence lists."""
    seen, out = set(), []
    for lic in [x for x in licence.split(",") if x]:
        params = {"q": q, "license": lic, "page_size": str(page_size)}
        if category:  # many Freesound items have no category, so this filter is off by default
            params["category"] = category
        if source:
            params["source"] = source
        try:
            res = fetch_json(API + "?" + urllib.parse.urlencode(params)).get("results", [])
        except urllib.error.HTTPError as e:
            print(f"licence {lic}: API error {e.code}, skipped", file=sys.stderr)
            continue
        for r in res:
            if r.get("id") not in seen:
                seen.add(r.get("id"))
                out.append(r)
    return out


def keep(res, min_sec, max_sec):
    out = []
    for r in res:
        if not r.get("url"):
            continue
        dur = (r.get("duration") or 0) / 1000
        if max_sec and dur and dur > max_sec:
            continue
        if min_sec and dur and dur < min_sec:
            continue
        out.append(r)
    return out


def describe(r):
    dur = (r.get("duration") or 0) / 1000
    lic = f"{r.get('license', '?')} {r.get('license_version') or ''}".strip()
    return (f"{r.get('id', '')[:8]}  {dur:5.2f}s  {lic:10}  {(r.get('title') or '')[:50]!s:50}  "
            f"by {(r.get('creator') or '?')[:25]}  {r.get('foreign_landing_url') or ''}")


def safe_name(r, i):
    base = re.sub(r"[^A-Za-z0-9_-]+", "_", (r.get("title") or "sound"))[:40].strip("_") or "sound"
    ext = (r.get("filetype") or Path(urllib.parse.urlparse(r["url"]).path).suffix.lstrip(".") or "mp3").lower()
    if not re.fullmatch(r"[a-z0-9]{2,5}", ext):
        ext = "mp3"
    return f"{i:02d}_{base}_{(r.get('id') or '')[:8]}.{ext}"


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)


def credit_line(r):
    lic = f"CC {r.get('license', '').upper()} {r.get('license_version') or ''}".strip()
    if r.get("license") in ("cc0", "pdm"):
        lic = r.get("license").upper()
    return (f"\"{r.get('title') or 'Untitled'}\" by {r.get('creator') or 'unknown'}, {lic}"
            f" ({r.get('license_url') or ''}), source: {r.get('foreign_landing_url') or r.get('url')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["search", "get"])
    ap.add_argument("query")
    ap.add_argument("--license", default=SAFE_DEFAULT, help="comma list, default cc0,pdm,by")
    ap.add_argument("--category", default="", help="sound_effect | music (off by default: Freesound items often have none)")
    ap.add_argument("--source", default="freesound", help="freesound (default, real recordings) | jamendo | wikimedia_audio | '' for all")
    ap.add_argument("--min-sec", type=float, default=0)
    ap.add_argument("--max-sec", type=float, default=0)
    ap.add_argument("--limit", type=int, default=15, help="results to show (search)")
    ap.add_argument("--count", type=int, default=3, help="files to download (get)")
    ap.add_argument("--out", default="./sfx")
    a = ap.parse_args()

    bad = {"by-nc", "by-nc-sa", "by-nd", "by-nc-nd", "sampling+", "nc-sampling+"}
    asked = {x.strip() for x in a.license.split(",") if x.strip()}
    if asked & bad:
        print("note: non-commercial or no-derivative licences requested; never use them for client work",
              file=sys.stderr)

    order = [x for x in ("cc0", "pdm", "by", "by-sa") if x in asked] + sorted(asked - {"cc0", "pdm", "by", "by-sa"})
    res = keep(search(a.query, ",".join(order), a.category, a.source, 20), a.min_sec, a.max_sec)  # 20 = anonymous cap
    if not res:
        sys.exit(f"no results for '{a.query}' with licence {a.license}; try other words or a wider licence")

    if a.mode == "search":
        for r in res[: a.limit]:
            print(describe(r))
        return

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    credits = out / "CREDITS.md"
    lines = [] if credits.exists() else ["# Sound credits (Openverse)\n"]
    got = 0
    for r in res:
        if got >= a.count:
            break
        name = safe_name(r, got + 1)
        try:
            download(r["url"], out / name)
        except Exception as e:  # skip a dead file and keep going
            print(f"skip {r.get('id')}: {e}", file=sys.stderr)
            continue
        got += 1
        print("saved", out / name, "|", describe(r))
        lines.append(f"- `{name}`: {credit_line(r)}")
        if r.get("attribution"):
            lines.append(f"  - Openverse attribution: {r['attribution']}")
        time.sleep(0.3)
    with open(credits, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{got} file(s) in {out}; credits in {credits}")


if __name__ == "__main__":
    main()
