#!/usr/bin/env python3
"""Phone pack: the moments to listen to, as ONE small MP4 to send to a phone (Marsad local addition).

Replaces `listen_page.py serve --lan` (which opened a page to the whole network). Each moment is a short piece of the
finished film, preceded by a 1 s card with its number, so the person can answer "1 ok, 2 too loud, 3 buried..." in chat.

  python scripts/phone_pack.py result/film_sfx.mp4 --at 3.2 --at 10.5 --at 21 [--span 3] [--out result/phone_pack.mp4]
  python scripts/phone_pack.py result/film_sfx.mp4 --at 3.2 --compare work/original.mp4   # A then B for each moment

Take the times from critique.py's listen list. Needs ffmpeg. Video is scaled to 720 px high to stay small.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1200:])


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"cannot read the length of {path}")


FONTS = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]


def font_opt():
    """An explicit font file: Windows builds of ffmpeg often have no fontconfig defaults."""
    for f in FONTS:
        if Path(f).is_file():
            return "fontfile='" + f.replace("\\", "/").replace(":", "\\:") + "':"
    return ""


def card(text, out, w, h):
    """1 s black card with a big number (digits and Latin letters only: no font issues)."""
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:r=30:d=1",
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "1",
         "-vf", f"drawtext={font_opt()}text='{text}':fontcolor=white:fontsize={h // 6}:x=(w-text_w)/2:y=(h-text_h)/2",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2", str(out)])


def piece(src, t, span, out, w, h):
    total = duration(src)
    start = max(0.0, min(t - span / 2, total - span))
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{span:.3f}",
         "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps=30",
         "-af", "aresample=48000", "-ac", "2", "-c:v", "libx264", "-crf", "26", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(out)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("--at", type=float, action="append", required=True, help="a moment's time in seconds (repeat)")
    ap.add_argument("--span", type=float, default=3.0)
    ap.add_argument("--compare", help="another version (e.g. the original); each moment plays A then B")
    ap.add_argument("--out", default="result/phone_pack.mp4")
    a = ap.parse_args()

    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", a.film], capture_output=True, text=True)
    try:
        sw, sh = (int(x) for x in r.stdout.strip().split(",")[:2])
    except ValueError:
        sys.exit(f"{a.film} has no video stream")
    h = 720
    w = int(round(sw * h / sh / 2) * 2)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, t in enumerate(a.at, 1):
            versions = [("", a.film)] if not a.compare else [("A", a.film), ("B", a.compare)]
            for tag, src in versions:
                c = Path(tmp) / f"c{i}{tag}.mp4"
                p = Path(tmp) / f"p{i}{tag}.mp4"
                card(f"{i}{tag}", c, w, h)
                piece(src, t, a.span, p, w, h)
                parts += [c, p]
        lst = Path(tmp) / "list.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
             "-movflags", "+faststart", str(out)])
    print(f"phone pack: {out}  ({len(a.at)} moment(s), {out.stat().st_size / 1e6:.1f} MB)")
    print("send it to the phone and ask for one answer per number (ok / loud / buried / harsh / extra / missing)")


if __name__ == "__main__":
    main()
