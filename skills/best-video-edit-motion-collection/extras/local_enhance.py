#!/usr/bin/env python3
"""فلترة صوت محلية (من غير رفع لأي خدمة) — بديل Auphonic للحالات الخفيفة والمتوسطة.

بتستخدم DeepFilterNet (نموذج ذكاء اصطناعي لإزالة الدوشة من الكلام) + ffmpeg للتسوية والضغط.
من غير numpy ولا تنزيلات إضافية — الأدوات في  ~/.local/tools/audio-clean/  (أو  $AUDIO_CLEAN_DIR):
    deep-filter.exe  (DeepFilterNet v0.5.6)

الاستخدام:
    python local_enhance.py <in.wav|mp4|mov> <out.wav> [--profile clean|noisy|hum] [--atten DB] [--lufs -16|none]

البروفايلات:
    clean  (الافتراضي)  دوشة خفيفة لمتوسطة — الصوت يفضل طبيعي (بيخفّض الدوشة لحد 24 ديسيبل)
    noisy               دوشة عالية (شارع · كافيه · مروحة) — أقصى تقليل + post-filter
    hum                 همهمة كهربا 50 هرتز + دوشة — فلتر قطع للهمهمة قبل التنظيف
⚠️ مش بيشيل الصدى (reverb) — الصدى حالة Auphonic (`--deverb-amount`) أو تسجيل أحسن.
الإخراج: wav 48kHz مونو (جاهز لـ02b_enhance_audio.sh أو دمج ffmpeg).
"""
import argparse, os, shutil, subprocess, sys, tempfile

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

TOOLS = os.environ.get("AUDIO_CLEAN_DIR") or os.path.join(os.path.expanduser("~"), ".local", "tools", "audio-clean")
DFN = os.path.join(TOOLS, "deep-filter.exe" if os.name == "nt" else "deep-filter")


def run(cmd, what, cwd=None):
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if p.returncode != 0:
        sys.exit(f"❌ {what} فشل:\n" + (p.stderr or p.stdout)[-400:])
    return p


def ff_escape(path):
    # ffmpeg filter: نقطتين المسار (C:) لازم تتهرّب
    return path.replace("\\", "/").replace(":", "\\:")


def main():
    ap = argparse.ArgumentParser(description="local speech enhance", add_help=True)
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--profile", choices=["clean", "noisy", "hum"], default="clean")
    ap.add_argument("--atten", type=float, help="حدّ تقليل الدوشة بالديسيبل (يغلب على البروفايل)")
    ap.add_argument("--lufs", default="-16", help="معايرة الصوت الناتج (الافتراضي -16؛ المحرّك بيعايره -14 في الآخر). 'none' = من غير معايرة")
    a = ap.parse_args()
    if not os.path.isfile(a.inp):
        sys.exit("❌ مفيش ملف: " + a.inp)
    if shutil.which("ffmpeg") is None:
        sys.exit("❌ ffmpeg مش موجود في الـPATH")
    if not os.path.isfile(DFN):
        sys.exit(f"❌ مش لاقي DeepFilterNet في {DFN} — استخدم Auphonic أو الطريق القديم (02b --local)، أو نزّله بعد موافقة المستخدم")

    tmp = tempfile.mkdtemp(prefix="locenh_")
    try:
        # 1) مونو 48k + هامش أمان -3dB (DeepFilterNet بيحذّر من القطع لو الصوت عالي)
        pre = os.path.join(tmp, "pre.wav")
        pre_af = ["volume=-3dB"]
        if a.profile == "hum":
            pre_af = ["bandreject=f=50:w=2", "bandreject=f=100:w=2", "bandreject=f=150:w=2"] + pre_af
        run(["ffmpeg", "-v", "error", "-y", "-i", a.inp, "-vn", "-ac", "1", "-ar", "48000",
             "-af", ",".join(pre_af), "-c:a", "pcm_s16le", pre], "التحضير")

        # 2) إزالة الدوشة
        if True:
            atten = a.atten if a.atten is not None else (100.0 if a.profile == "noisy" else 24.0)
            cmd = [DFN, "-a", str(atten), "-o", os.path.join(tmp, "dfn")]
            if a.profile == "noisy":
                cmd.append("--pf")
            run(cmd + [pre], "DeepFilterNet")
            den = os.path.join(tmp, "dfn", "pre.wav")
            if not os.path.isfile(den):
                sys.exit("❌ DeepFilterNet ما طلّعش ملف")

        # 3) تنضيف الواطي + تسوية (leveler) + ضغط خفيف (+ معايرة اختيارية)
        post = ["highpass=f=70", "dynaudnorm=f=250:g=15:p=0.9:m=10",
                "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150"]
        if str(a.lufs).lower() != "none":
            post.append(f"loudnorm=I={float(a.lufs)}:TP=-1.5:LRA=11")
        run(["ffmpeg", "-v", "error", "-y", "-i", den, "-af", ",".join(post), "-ar", "48000",
             "-c:a", "pcm_s16le", a.out], "التسوية")
        print(f"✅ {a.out}  (profile={a.profile}" + (f", atten={a.atten}" if a.atten is not None else "") + ")")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
