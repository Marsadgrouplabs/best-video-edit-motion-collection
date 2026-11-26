#!/usr/bin/env python3
"""قص العلامة الصوتية (الفويس/الووتر مارك) اللي Auphonic بيضيفها في أول/آخر الملف.

الفكرة: الصوت الأصلي (in) والصوت المعالَج (clean) نفس الكلام، بس clean فيه جزء زيادة (العلامة).
بنقارن «منحنى علو الصوت» بينهم عشان نعرف الكلام الحقيقي بيبدأ فين، ونقص clean على طول الأصل بالظبط.
من غير numpy — ffmpeg + بايثون عادي.

الاستخدام:  python auphonic_trim.py <in.wav> <clean.wav> <out.wav>
المخرجات:   out.wav (بنفس طول الأصل) + سطر JSON فيه الإزاحة والجزء المقصوص ودرجة الثقة.
كود الخروج: 0 تمام · 2 مفيش جزء زيادة · 3 مش واثق (العلامة متداخلة أو في النص) ← المستخدم يسمع
"""
import array, json, math, subprocess, sys

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

SR = 8000  # معدّل تحليل خفيف


def decode(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", "-"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        sys.exit("❌ ffmpeg مقدرش يقرا " + path + ": " + p.stderr.decode(errors="ignore")[:200])
    a = array.array("h"); a.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    return a


def envelope(a, hz):
    """log-RMS لكل إطار (hz إطار في الثانية)."""
    n = SR // hz
    out = []
    for i in range(0, len(a) - n + 1, n):
        s = 0
        for v in a[i:i + n]:
            s += v * v
        out.append(math.log10(math.sqrt(s / n) + 1.0))
    return out


def pearson(x, y):
    n = len(x)
    if n < 10:
        return -1.0
    mx = sum(x) / n; my = sum(y) / n
    sxx = sum((v - mx) ** 2 for v in x); syy = sum((v - my) ** 2 for v in y)
    if sxx <= 0 or syy <= 0:
        return -1.0
    return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / math.sqrt(sxx * syy)


def best_offset(ref, tgt, lo, hi):
    """أحسن إزاحة k في [lo,hi] بحيث tgt[k:k+len(ref)] يشبه ref."""
    best = (-2.0, lo)
    for k in range(max(0, lo), hi + 1):
        seg = tgt[k:k + len(ref)]
        if len(seg) < len(ref):
            break
        r = pearson(ref, seg)
        if r > best[0]:
            best = (r, k)
    return best


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    fin, fcl, fout = sys.argv[1:]
    a_in, a_cl = decode(fin), decode(fcl)
    d_in, d_cl = len(a_in) / SR, len(a_cl) / SR
    extra = d_cl - d_in
    res = {"in_sec": round(d_in, 3), "clean_sec": round(d_cl, 3), "extra_sec": round(extra, 3)}
    if extra < 0.15:
        res["status"] = "no_extra"
        print(json.dumps(res, ensure_ascii=False))
        if extra < -0.5:
            print("⚠️ الملف المعالَج أقصر من الأصل — اسمعه قبل ما تكمّل", file=sys.stderr)
        sys.exit(2)

    # بحث خشن 20 إطار/ثانية على كل إزاحة ممكنة (0 .. الزيادة) ثم تظبيط دقيق 200 إطار/ثانية
    hz1 = 20
    e_in, e_cl = envelope(a_in, hz1), envelope(a_cl, hz1)
    r1, k1 = best_offset(e_in, e_cl, 0, int(math.ceil(extra * hz1)) + 2)
    hz2 = 200
    e_in2, e_cl2 = envelope(a_in, hz2), envelope(a_cl, hz2)
    c = int(k1 * hz2 / hz1)
    r2, k2 = best_offset(e_in2, e_cl2, c - 12, c + 12)
    off = k2 / hz2
    off = min(max(off, 0.0), extra)  # الإزاحة مش ممكن تعدّي الزيادة
    head, tail = off, extra - off
    res.update(offset_sec=round(off, 3), head_cut=round(head, 3), tail_cut=round(tail, 3),
               confidence=round(r2, 3))
    if r2 < 0.7:
        res["status"] = "low_confidence"
        print(json.dumps(res, ensure_ascii=False))
        print("⚠️ مش واثق من مكان العلامة (ممكن تكون في نص الصوت أو مدمجة فوق الكلام). "
              "ماقصّيتش حاجة — اسمع الملف المعالَج.", file=sys.stderr)
        sys.exit(3)

    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-t", f"{d_in:.3f}",
                        "-i", fcl, "-c:a", "pcm_s16le", fout], capture_output=True)
    if p.returncode != 0:
        sys.exit("❌ فشل القص: " + p.stderr.decode(errors="ignore")[:200])
    res["status"] = "trimmed"
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
