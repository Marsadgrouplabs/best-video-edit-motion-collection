# المؤثرات الصوتية (SFX) — منين نجيب الصوت ونحطه إزاي

**المشكلة:** إحنا مش بنسمع. لو حطينا الصوت بالتخمين، هييجي في فريم غلط وبمستوى عالي أو واطي. الحل إن الصوت يبقى
صوت حقيقي (مش مولّد إلا لو مفيش بديل)، ويتحط على الفريم بالظبط، وبالمستوى الصح، ويتسجّل مصدره ورخصته.

⛔ قاعدة المحرّك ثابتة: صوت في لحظة ليها معنى بس، مش على كل كلمة، **15 حدث في الدقيقة بالكتير** في فيديو فيه كلام.
وأي صوت مش CC0 لازم يتكتب مصدره في `CREDITS.md` جنب المشروع.

## اختار المصدر (من الأسهل للأقوى)

| المصدر | امتى | التسطيب | الحقوق |
|---|---|---|---|
| 1. `extras/sound-kit/` | كليك · بوب · تيك · كتابة · هبوط — موجودة جاهزة | مفيش | 28 صوت CC0 (Reel Studio، MIT) |
| 2. **Openverse** `extras/sfx/openverse_sfx.py` | محتاج whoosh · impact · riser · كاش · جمهور · أي صوت مش في الكيت | مفيش (Python بس، ومن غير مفتاح) | كل صوت برخصته في `CREDITS.md`. للعملاء: `--license cc0,pdm` |
| 3. **real-sfx** (Clipwing) | فيديو موشن/إعلان/تسجيل شاشة عايز sound design كامل: تحديد اللحظات وتحطيط الأصوات على الفريم ومستويات وتقرير وتقييم | Python + FFmpeg (موجودين) | السكربتات MIT، أصوات uisfx CC0، ومكتبتك برخصتها |
| 4. **earshot** (MCP) | الصوت مش موجود في أي مكتبة («whoosh ناعم 0.8 ثانية»، «3 خطوات على زلط») | MCP server على الجهاز | MIT، والصوت اللي بيطلعه بتاعك |

**الترتيب الافتراضي:** الكيت ← Openverse ← earshot لو لسه ناقص. ولو الفيديو كله محتاج sound design (موشن جرافيكس،
إعلان منتج، HyperFrames) ← real-sfx من الأول.

## 2. Openverse (ببلاش، من غير تسطيب)

```
python extras/sfx/openverse_sfx.py search "whoosh" --license cc0 --max-sec 3
python extras/sfx/openverse_sfx.py get "impact" --license cc0,pdm --max-sec 2 --count 3 --out "<مجلد الشغل>/sfx"
```
- كلمات البحث **بالإنجليزي**: whoosh · swoosh · impact · riser · pop · mouse click · keyboard typing · cash register ·
  camera shutter · crowd cheer · notification.
- `get` بينزّل الملفات ويكتب `CREDITS.md`. لو فيه صوت `by`، ادي المستخدم سطر الائتمان جاهز يحطه في الكابشن.
- الأصوات بتتحط في `sfx.json` بمفتاح `files` زي الكيت بالظبط (`t` الثانية، `g` المستوى 0.3-0.6).
- الحد: حوالي 100 طلب في اليوم من غير مفتاح، فدوّر مرة واحدة واستخدم النتايج.
- نفس الأداة موجودة كـ skill لوحدها اسمها `openverse-sfx`.

## 3. real-sfx (sound design كامل على الفريم)

**لو الـ skill `real-sfx` متسطبة** (`~/.claude/skills/real-sfx`)، استخدمها هي واقرا `SKILL.md` بتاعها كامل (فيها مكتبة الكيت متضافة وجاهزة).
لو مش متسطبة، استخدم النسخة اللي جوه هنا `extras/sfx/real-sfx/` واقرا `GUIDE.md` (هو نفس `SKILL.md` الأصلي). أول مرة: `python scripts/setup.py init --uisfx` و`python scripts/setup.py add-library soundkit "<مسار الكوليكشن>/extras/sound-kit" --tier main --index`.

ملخص الطريق السريع (السكربتات بتشتغل من جوه مجلد real-sfx، ومسارات الويندوز بين علامات تنصيص):
```
python scripts/setup.py check
python scripts/look.py "FILM.mp4" --out work/look
python scripts/find_moments.py "FILM.mp4" --out work/moments --fine
python scripts/suggest_cues.py work/moments/moments.json --out work/cues.json
python scripts/mix.py work/cues.json --out result/film_sfx.mp4 --voice-safe      # فيديو فيه كلام
python scripts/critique.py result/film_sfx_resolved_cues.json result/film_sfx_sfx_track.wav
```
- فيديو **فيه كلام** (شغل المحرّكين): `--voice-safe` دايماً، والأصوات في الوقفات مش فوق الكلمة.
- فيديو **فيه مزيكا**: `--duck`.
- الأصوات من مكتبتك: `python scripts/setup.py add-library main "D:/Sounds" --tier main --index`. ممكن تضيف
  مجلد Openverse ومجلد `extras/sound-kit` كمكتبة كمان.
- الناتج: MP4 جديد + ملف WAV للمؤثرات لوحده + تقرير. لو هترجّع الصوت للمحرّك، خد ملف الـ WAV وحطه في المكساج
  الأخير بدل ما تبني الفيديو مرتين.
- ⛔ الإعدادات الإضافية التقيلة (`listen.py install --yes` حوالي 16 ميجا، `hear.py install --yes` حوالي 3.1 جيجا)
  اختيارية: خد موافقة المستخدم الأول.
- **المستخدم يسمع على الموبايل:** خيار `--lan` مقفول في نسختنا (كان بيفتح الصفحة لأي حد على نفس الواي فاي). بداله:
  `python scripts/phone_pack.py result/film_sfx.mp4 --at T1 --at T2 --at T3 --out result/phone_pack.mp4` (الأوقات من
  قايمة الاستماع بتاعة `critique.py`). بيطلع MP4 صغير، كل لحظة قبلها كارت برقم، والمستخدم يبعته لموبايله على واتساب
  أو Drive ويرد «1 تمام، 2 عالي، 3 مش باين». `--compare original.mp4` بيعرض A وبعدين B لكل لحظة.

## 4. earshot (يولّد الصوت بالكود)

الدليل الكامل: `extras/sfx/earshot/GUIDE.md` (نفس skill الـ `earshot`)، وطريقة sound design كاملة بأصوات مرخصة من Freesound
وMixkit مع مكساج وماستر وائتمانات: `extras/sfx/earshot/real-sound/GUIDE.md` (نفس skill الـ `real-sound`). لو الـ skills دي متسطبة
لوحدها استخدمها هي. لو مش متسطبة، استخدم النسخ دي.

لو أدوات `mcp__earshot__*` موجودة في الجلسة:
- `make` بوصف بالإنجليزي: «a soft whoosh, 0.8 s» أو «three variations of a footstep on gravel». الملف بيطلع ومعاه
  مدته ومكان ذروته وعلوه، وحط الصوت بحيث الذروة تيجي على الفريم.
- `build` لو الصوت مش في الكتالوج (بيركّبه من تسجيلات).
- أدوات الاستماع (`describe` · `match` · `critique`) محتاجة موديلات حوالي 1.1 جيجا، **بتتحمل أول مرة تتطلب**.
  خد موافقة المستخدم قبل أول استخدام ليها. `make` و`build` مش محتاجين أي تحميل.
- مش موجودة في الجلسة؟ قول للمستخدم في سطر إن earshot مش متوصل، وكمّل بـ Openverse.

## التسليم
اذكر في ملخص التسليم: كام صوت اتحط، ومنين (كيت / Openverse / real-sfx / earshot)، ومسار `CREDITS.md` لو فيه أصوات
محتاجة ائتمان، وإن **المستخدم لازم يسمع** أول 5 ثواني ولحظة الذروة، لأن الأرقام مش بتسمع.
