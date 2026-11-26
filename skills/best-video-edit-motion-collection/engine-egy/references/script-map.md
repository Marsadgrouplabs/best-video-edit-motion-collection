<!-- مرجع لسكل video-ad-editor-masri — بيتقري وقت الحاجة بس (توفير توكنز) -->

# خريطة السكربتات والملفات

| | بيعمل إيه | المحرّك |
|---|---|---|
| `00_setup.sh` | بيفحص الأدوات وينزّل الناقص · `--update` مقفول في النسخة المصري | مشترك |
| `01_cut_plan.py` | بيقيس السكتات ويطلّع مقاطع الكلام | مشترك |
| `02_captions.py` | توقيت كل كلمة على التايم-لاين الجديد · 🇪🇬 الكلمة `""` بتندمج في اللي قبلها | مشترك |
| `eg_prompt.txt` | 🇪🇬 جملة العامية المصري اللي بتتبعت لوِسبر (`--initial_prompt`) | مشترك |
| `02b_enhance_audio.sh` | تحسين الصوت على الجهاز (`references/audio-enhance.md`) | مشترك |
| `03_cut_zoom.py` | القص + زوم لكل مقطع + وسم bt709 + محوّل HDR | مشترك |
| `04_render_frames.js` | بيرسم الفريمات (استكمال + نافذة + معاينة) · بيطبع أخطاء المشاهد بـ`[compose]` | الخفيف |
| `04b_remotion.sh` | بيجهّز/يفتح/يرندر مشروع ريموشن (`references/remotion.md`) | ريموشن |
| `05_sfx.py` | المؤثرات الصوتية من `sfx.json` | مشترك |
| `06_encode.sh` | بيجمّع الفريمات + الصوت | الخفيف |
| `06b_master.sh` | ‎-14 LUFS + ملف صوتي في الخلفية بيوطى أوتوماتيك | مشترك |
| `07_contact_sheet.sh` | ورقة لقطات واحدة: 3 عواميد × صفّين (6 بالكتير) | مشترك |
| `08_safe_check.js` | المنطقة الآمنة + الهوك (نفس حمولة 04: theme + studio + behind) | الخفيف |
| `09_srt.py` | ملف ترجمة + نص الكابشن | مشترك |
| `10_script_edit.py` | `show` (بيطبع النص والجمل المتكررة) · `drop` · `keep` · `undo` · 🇪🇬 بيفهم الكلمات المصري الفاضية | مشترك |
| `11_behind_text.js` + `personmask.swift` | أنماط القص التلاتة (`references/cut-styles.md`) | الخفيف (ماك) |
| `12_montage.py` | **وضع المونتاج** (`references/montage.md`) | مستقل |
| `13_collage.js` · `13_collage_sfx.py` · `collage.TEMPLATE.html` | أسلوب الكولاج (`references/collage.md`) · 🇪🇬 كلمات مصري في المخطِّط | مستقل |
| `13_assets.py` | صورة من ويكيميديا (رخصة حرة) مع قص خلفية اختياري | مشترك |
| `14_backdrop.py` | خلفية باهتة (`references/backdrop.md`) | الخفيف |
| `15_podcast.py` · `16_render_pod.js` · `compose.PODCAST.html` · `facetrack.swift` | **وضع البودكاست** (`references/podcast.md`) | مستقل (ماك) |
| `17_gen_scenes.py` | مشاهد مولّدة (`references/gen-scenes.md`) | الخفيف |
| `compose.REFERENCE.html` | المحرّك: الفيديو · الكابشن · ورا الراس · بي-رول · مولّد · ستيكرز · كرت النهاية (🇪🇬 فاضي افتراضياً) | الخفيف |
| `compose.EXAMPLES.js` | مشاهد المثال القديم للقراية — **مش بيتحمّل افتراضياً** | — |
| `studio/studio.py` | الاستوديو — تايملاين باللمس فوق نفس الملفات والراسم (`references/studio.md`) | الخفيف |

## ملفات فولدر الشغل
`src.mov` · `a.json` (وِسبر) · `fixes.json` · `cut.json` · `caps.json` · `theme.json` · `studio.json` (فيه `outro`) · `sfx.json` · `behind.json` · `safe.json` (اختياري) · `vfr/` (فريمات المصدر) · `out/` (فريمات الرسم) · `prev/` (معاينة) · `ad-final.mp4` · `ad-master.mp4/.srt/.txt`.
**احفظ `caps.json` و`cut.json`** — أي تعديل بعدين مش محتاج إعادة تفريغ.
