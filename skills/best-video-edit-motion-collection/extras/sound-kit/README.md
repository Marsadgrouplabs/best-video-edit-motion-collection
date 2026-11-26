# كيت أصوات CC0 (28 صوت قصير)
مأخوذ من مشروع Reel Studio (MIT) — كل الأصوات **CC0 / ملكية عامة**، من غير اسم ولا ائتمان. المصدر والتحقق (SHA-256) لكل ملف في `ledger.json`. مفيش فيها موسيقى ولا whoosh ولا صوت خطأ مزعج.

## إزاي تستخدمها
اختيارية — لو المستخدم عايز صوت "حقيقي" بدل المولّد. حطّ المسار في `sfx.json` (الخطوة 8 في المحرّك) بمفتاح `files`:
```json
{ "files": [ {"f":"<مسار الملف>/extras/sound-kit/pop-minimal.wav", "t":3.1, "g":0.4} ] }
```
`t` الثانية، و`g` المستوى (0.3-0.6 عادةً). ⛔ قاعدة المحرّك ثابتة: صوت في لحظة ليها معنى بس، مش على كل كلمة، 15 حدث في الدقيقة بالكتير.

## الكيت
| الملف | النوع | بيتستخدم فين |
|---|---|---|
| `click-minimal.wav` | click | One dry damped press: a screenshot, a capture, a pressed button. |
| `click-mechanical.wav` | click | A firmer mechanical press for a real product button. |
| `click-snap.wav` | click | A short soft snap when something locks into place. |
| `click-tiny.wav` | click | A very short tick-like click (about 20 ms); stack it under a bigger sound or use it alone at low gain. |
| `click-metal.wav` | click | A small metal latch click for a capture or a confirmed selection. |
| `pop-minimal.wav` | pop | A small pop for a badge, chip or sticker that appears. |
| `pop-rubber.wav` | pop | A rounder pop for a card or highlight that appears. |
| `pop-organic.wav` | pop | A warmer pop for a hand-made element (paper, tape, sticker). |
| `pop-zen.wav` | pop | A light pop with a soft tail for a calm reveal. |
| `pop-select.wav` | pop | A tiny pop (about 60 ms) for a chip or a list item that appears. |
| `chime-minimal.wav` | chime | A short chime after a click: done, confirmed, installed. |
| `chime-zen.wav` | chime | A softer chime for a calm result. |
| `chime-bright.wav` | chime | A short bright confirmation (about 0.3 s). |
| `chime-soft.wav` | chime | A short soft confirmation (about 0.3 s). |
| `tick-minimal.wav` | tick | One step of a counter or a progress bar. |
| `tick-1.wav` | tick | A short counter tick. |
| `tick-2.wav` | tick | A shorter, higher counter tick; alternate with tick-1. |
| `tick-3.wav` | tick | A third counter tick for variation. |
| `type-minimal.wav` | type | One key tap; vary the pick and the gain for a short uneven burst. |
| `type-mechanical.wav` | type | A firmer key tap for a code or terminal line. |
| `type-organic.wav` | type | A softer key tap for a chat or search box. |
| `reject-dull.wav` | reject | A wrong answer or a rejected option: one short dull click at a low gain. |
| `landing-cinematic.wav` | landing | A soft low landing for a stamp or a heavy card (about 0.6 s). |
| `landing-soft-heavy.wav` | landing | A soft heavy thud: a weighted landing or a chapter change. |
| `landing-soft-medium.wav` | landing | A lighter soft thud for a card that settles. |
| `landing-wood.wav` | landing | A dry wooden thud for a stamp or a block that drops. |
| `landing-plank.wav` | landing | A hollow plank knock for a board or a panel that lands. |
| `paper-flip.wav` | paper | A single page turn for the Arabic page-turn move. Paper foley, not a sweep; drop it if you treat page turns as sweeps. |
