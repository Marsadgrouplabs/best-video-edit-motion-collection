#!/bin/bash
# فحص وتجهيز الأدوات.  ./00_setup.sh          → يفحص ويقول إيه الناقص
#                      ./00_setup.sh --install → ينزّل الناقص (بعد إذن المستخدم)
# ✏️ معدّل ليشتغل على ويندوز وماك ولينكس. الأصل الماكي محفوظ بـ00_setup.sh.mac-orig
. "$(dirname "$0")/_compat.sh"
INSTALL=0; [ "$1" = "--install" ] && INSTALL=1
MISS=(); OK=(); NOTE=()
have(){ command -v "$1" >/dev/null 2>&1; }
line(){ printf '%s\n' "$1"; }

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  Darwin) OS=mac ;;
  *) OS=linux ;;
esac
SKILL="$(abspath "$(dirname "$0")/..")"
# 🚧 حارس السحابة (8 سبتمبر): من تطبيق كلود بالسحابة (ساندبوكس لينكس) تنزيل موديل وِسبر محجوب وما فيه متصفح للرسم —
#    السكل يشتغل على جهازك (ماك أو ويندوز) عبر Claude Code. نوقف هنا برسالة واضحة بدل خطأ غامض بعدين.
if [ "$OS" = linux ] && { [ -n "$CLAUDE_SANDBOX" ] || [ ! -d /Applications ]; } && ! curl -sI -m 8 https://openaipublic.azureedge.net >/dev/null 2>&1; then
  echo "⛔ السكل ده بيشتغل على جهازك عن طريق Claude Code (ماك أو ويندوز)، مش جوه تطبيق كلود على السحابة."
  echo "   السحابة بتمنع تنزيل موديل التفريغ (openaipublic.azureedge.net) ومفيهاش متصفح للرسم."
  echo "   الحل: افتح Claude Code على جهازك (الوضع المحلي Local) وشغّل نفس الطلب."
  exit 9
fi

# 🔄 النسخة المصري (fork من majedphotos/video-ad-editor): التحديث التلقائي مقفول عن قصد —
#    تحديث الأصل كان بيمسح السكل كله (rsync --delete) ويرجّعه خليجي. هنا بنبلّغ بس لو الأصل نزّل إصدار أحدث.
SKROOT="$(cd "$(dirname "$0")/.." && pwd)"; LOCALV="$(cat "$SKROOT/VERSION" 2>/dev/null || echo 0)"; BASEV="${LOCALV%%-*}"
if [ "$1" = "--update" ]; then
  echo "⛔ التحديث التلقائي مقفول في النسخة المصري عشان مايمسحهاش ويرجّعها خليجي."
  echo "   لو عايز مميزات الإصدار الجديد: اطلب من كلود «حدّث النسخة المصري من السكل الأصلي» ويعمل نسخة مصري جديدة."
  exit 0
fi
LATEST="$(curl -sL -m 5 https://api.github.com/repos/majedphotos/video-ad-editor/releases/latest 2>/dev/null | sed -n 's/.*"tag_name": *"v\([0-9.]*\)".*/\1/p' | head -1)"
if [ -n "$LATEST" ] && [ "$LATEST" != "$BASEV" ] && [ "$(printf '%s\n%s' "$BASEV" "$LATEST" | sort -V | tail -1)" = "$LATEST" ]; then
  echo "ℹ️ السكل الأصلي نزّل إصدار أحدث: v$LATEST (النسخة المصري مبنية على v$BASEV) — مش لازم تعمل حاجة دلوقتي؛ قول للمستخدم بس في آخر الشغل لو يهمه."
fi

have ffmpeg  && OK+=("ffmpeg")  || MISS+=("ffmpeg")
have ffprobe && OK+=("ffprobe") || MISS+=("ffprobe")
"$PY" -c "import whisper" 2>/dev/null && OK+=("whisper") || MISS+=("whisper")
"$PY" -c "import numpy"   2>/dev/null && OK+=("numpy")   || MISS+=("numpy")

# كروم: نفس ترتيب البحث اللي بالسكربتات
find_chrome(){
  [ -n "$CHROME_PATH" ] && [ -f "$CHROME_PATH" ] && { echo "$CHROME_PATH"; return 0; }
  local c
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "${ProgramFiles:-C:/Program Files}/Google/Chrome/Application/chrome.exe" \
           "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
           "${LOCALAPPDATA:-}/Google/Chrome/Application/chrome.exe" \
           "${ProgramFiles:-C:/Program Files}/Microsoft/Edge/Application/msedge.exe" \
           /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do
    [ -f "$c" ] && { echo "$c"; return 0; }
  done; return 1
}
CHROME="$(find_chrome)" && OK+=("chrome") || MISS+=("chrome")

# puppeteer-core: بندوّر عليه في مجلد السكل نفسه (هناك بينزل)
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null \
  && OK+=("puppeteer-core") || MISS+=("puppeteer-core")

line "النظام: $OS · بايثون: $PY"
[ -n "$CHROME" ] && line "كروم: $CHROME"
line "الجاهز: ${OK[*]:-ولا حاجة}"
if have npm; then line "المحرّك الثاني (ريموشن): متاح لو اتطلب — 04b_remotion.sh setup بينزّله (~500 ميجا)"
else line "المحرّك الثاني (ريموشن): محتاج npm — مش متاح، والخفيف كفاية"; fi
[ "$OS" = mac ] || NOTE+=("مؤثّر «الكلام ورا الشخص» (11_behind_text.js) بيشتغل على ماك بس — باقي السكل شغال عادي")

if [ ${#MISS[@]} -eq 0 ]; then
  line "✅ كله جاهز — نقدر نبدأ."
  [ ${#NOTE[@]} -gt 0 ] && printf 'ℹ️  %s\n' "${NOTE[@]}"
  exit 0
fi
line "الناقص: ${MISS[*]}"
if [ $INSTALL -eq 0 ]; then line "شغّل: $0 --install"; exit 10; fi

pipi(){ "$PY" -m pip install --quiet "$@" || "$PY" -m pip install --quiet --break-system-packages "$@"; }
for m in "${MISS[@]}"; do
  case "$m" in
    ffmpeg|ffprobe)
      [ "$m" = ffprobe ] && continue
      line "⏬ ffmpeg…"
      if   [ "$OS" = win ] && have winget; then winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements || NOTE+=("ffmpeg فشل — نزّله من ffmpeg.org وضيفه للـPATH")
      elif have brew;  then brew install ffmpeg || NOTE+=("ffmpeg فشل")
      elif have apt;   then sudo apt install -y ffmpeg || NOTE+=("ffmpeg فشل")
      else NOTE+=("نزّل ffmpeg بإيدك من ffmpeg.org وضيفه للـPATH"); fi ;;
    whisper) line "⏬ openai-whisper… (الموديل بينزل أول مرة، 1.5 جيجا تقريباً)"
      pipi openai-whisper || NOTE+=("whisper فشل") ;;
    numpy)   pipi numpy || NOTE+=("numpy فشل") ;;
    puppeteer-core) line "⏬ puppeteer-core…"
      ( cd "$SKILL" && npm i --silent puppeteer-core ) || NOTE+=("puppeteer-core فشل") ;;
    chrome) NOTE+=("كروم مش متسطّب — نزّله من google.com/chrome أو حدّد CHROME_PATH") ;;
  esac
done

FAIL=0
have ffmpeg || FAIL=1
"$PY" -c "import whisper,numpy" 2>/dev/null || FAIL=1
find_chrome >/dev/null || FAIL=1
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null || FAIL=1
[ ${#NOTE[@]} -gt 0 ] && printf '⚠️  %s\n' "${NOTE[@]}"
[ $FAIL -eq 0 ] && line "✅ كله جاهز دلوقتي." || { line "❌ لسه فيه حاجات ناقصة — شوف الملاحظات اللي فوق."; exit 11; }
