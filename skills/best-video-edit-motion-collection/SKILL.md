---
name: best-video-edit-motion-collection
description: "Best Video Edit & Motion Collection: an always-updated bundle of the best AI video editing and motion tools and skills, each credited to its author. Works in any language. A full editing engine (silence removal, talking video to 9:16 reels and ads, word-synced captions, montage, 2-camera podcast, touch studio, collage, audio clean-up, generated scenes), 5 motion styles for videos made from code (HyperFrames, onetake, collage B-roll, hand-drawn cartoon, 43 cinematic looks), real sound effects placed on the frame (sound kit, Openverse, real-sfx, earshot), dubbing into another language or dialect in the speaker's own voice (ElevenLabs). Formerly marwan-video-edit. Use whenever the user wants to edit or make a video, add captions, motion graphics, B-roll, SFX or dubbing, or asks to install this collection or choose which parts to install. Not for carousels or video covers."
---

# Best Video Edit & Motion Collection

One skill that collects the best AI video editing and motion work in one place, and keeps growing: when a good new
tool, skill or workflow appears, it is added here as a new component, with its author credited in `NOTICE.md`.
Formerly `marwan-video-edit`.

**Works in any language.** Reply in the language and dialect the user writes in. Captions, on-screen text and the end
card use the speaker's language. Never force a specific language or dialect.

## Bundled components (read `COMPONENTS.md`)
This skill ships other skills and tools inside it. `COMPONENTS.md` lists every part: what it does, why it matters,
its size, what it needs, and its author and licence.

- **The user asks to install, set up, update or "add" this collection** → follow "Install flow" in `COMPONENTS.md`:
  list the parts, explain each in one line (what it does and why it matters), mark the paid or non-commercial ones,
  and let the user choose **all** or **some**. Install only what they chose. Never install a part they declined.
- **A component folder is missing at work time** → that part was not installed. Say so in one line and offer to add
  it (from the repo or the full zip). Carry on with what is installed.

## 0) Reference and brand first → `extras/00-reference-and-brand.md`
**Read it before picking a style or starting work.** Look for a **Reference** folder (videos, images, links, notes the
user likes) and a **Brand** file or folder (colours, fonts, logo, handle, tone, don'ts). Strongly recommended, not
required:
- Found them → read them, summarise in two sentences, follow them.
- Not found → ask **one question, once**: "Do you have a Reference folder or a Brand file?" Continue with defaults if
  not, and tell them it works better with them (templates in `templates/`).
- Priority: **the user's explicit words → brand file → reference → this skill's suggestions.**
- Analyse a reference video with `extras/style-learning.md` (learn the style, never copy shots).

## 0.5) Token mode: ask at the start (same message as the reference question, once)
Visual review (reading frames and images) is what uses the most of the user's limit. Ask one simple question:

> "Should I work with **fewer** or **more** tokens? The difference is review:
> • **Fewer (saver)**: I do the work and the numeric checks (safe zone, sync, loudness, size); you watch the video and
>   tell me what to change. Much cheaper.
> • **More (full review)**: I also check frames myself and review text and motion frame by frame. More precise, uses
>   more of your limit."

- **Default if no answer:** saver. "Doesn't matter" → saver. Don't ask again in the same session.
- ⚠️ **Saver still checks:** the numeric checks (safe zone, sync, LUFS, size) always run; they print a few
  numbers and cost little.

| | Saver 🪙 | Full review 🔍 |
|---|---|---|
| Numeric checks | ✅ | ✅ |
| Contact sheet | **Don't read it**: save it and hand it to the user | Read it yourself (one sheet, 6 frames) |
| Single frames / frame-by-frame motion check | ❌ | ✅ on the hardest part |
| Text QA (`extras/review-and-arabic-qa.md` §3, adapt to the language) | Short list for the user + automatic checks | Full, on frames |
| Reference analysis (`style-learning.md`) | 3 samples + questions about pace | Full check with evidence |
| Preview | Send a short preview (6-10 s) or the studio for them to review | Show the sheet after you reviewed it |
| Your replies | Two lines, no images | Two lines, an image when needed |

**In saver mode the eye review is human:** tell them exactly what to look at ("open the video: first 3 seconds,
captions not on the face, text reads correctly, audio is clear") and what you checked by numbers. Write
"Eye review: by the user" in the delivery summary instead of claiming you did it.

## 1) The editing engine
| Engine | Folder | Instructions | Best for |
|---|---|---|---|
| **Engine A** (fork of video-ad-editor v3.4, Egyptian edition) | `engine-egy/` | `engine-egy/ENGINE.md` | Any language. Silence removal, reels, captions, montage, podcast, touch studio, collage, audio clean-up, generated scenes |

⛔ Every `scripts/…` or `references/…` path inside the engine file is relative to the engine's folder. Run scripts from inside it (e.g. `bash engine-egy/scripts/00_setup.sh`).

Read `engine-egy/ENGINE.md` in full and follow it. If files conflict, the engine file wins, then this file. If `engine-egy/` is missing, it was not installed: say so and offer to add it (see `COMPONENTS.md`).

### Speech in any language
The engine files were written in Arabic and default to Arabic speech. For any other language:
- Transcribe in the speaker's language: replace `--language ar` / `language="ar"` with the speaker's code (`en`, `fr`,
  `es`, `de`, `tr`, `hi`, `ur`…) or leave it out for auto-detect. Skip `eg_prompt.txt` (it is an Egyptian Arabic
  vocabulary prompt); write a short prompt with the speaker's names and terms instead.
- Captions, end card and publish copy in the speaker's language. Never translate unless asked.
- Left-to-right languages: set `dir="ltr"` and the right `lang` on the compose/studio HTML copy for this job. Pick a
  font that covers the script (Latin, Cyrillic, Devanagari, CJK…).
- `extras/review-and-arabic-qa.md`: apply its checks to the language at hand (broken letters, wrong direction,
  missing glyphs, words cut mid-line); skip the Arabic-only items.
- Western digits stay the default unless the brand file says otherwise.

## 2) What the engine does
| Feature | Where |
|---|---|
| Montage of clips with no speech (cafe, food, product) | `references/montage.md` |
| Podcast with two or more cameras | `references/podcast.md` |
| Touch editing studio (timeline from phone or browser) | `references/studio.md` |
| Collage, faded background, voice enhancement, word animations, screen recording | engine references |
| Audio filtering with Auphonic (a different filter per audio case) | `extras/auphonic-audio.md` |
| AI-generated scenes via `FAL_KEY` | `references/gen-scenes.md` |

## 2.5) Motion styles: a suggestion, not a rule (videos made from code, not editing filmed footage)
If the user wants a **video made with code or motion** (ad, explainer, short film, teaser):
- They have enough **reference or brand** → **don't list the styles** (mention in one line they exist).
- No reference and no style named → list these five briefly, say they can pick one or go without, and wait.
- Named a style → go straight to it. "No style" or "something simple" → respect that.
Brand colours and fonts apply to any style. Filmed talking footage to cut (silences, captions, reel) → that is the
engines above, not the styles.

| # | Style | Instructions | Idea | Notes |
|---|---|---|---|---|
| 1 | HyperFrames (HeyGen) | `styles/hyperframes/STYLE.md` | Clean motion graphics: titles, numbers, screens; video from HTML | Tech ads, launches. Apache 2.0 |
| 2 | onetake | `styles/onetake/STYLE.md` | One continuous shot, each scene grows out of the last | ⚠️ **Non-commercial licence (PolyForm Noncommercial)**: warn before any client work |
| 3 | Collage B-roll | `styles/collage-broll/STYLE.md` | Magazine cut-outs and halftones layered in front of scenes | Documentary, history. Needs `GEMINI_API_KEY` (paid); written for Codex, in Chinese |
| 4 | Clawd Animation | `styles/clawd-animation/STYLE.md` | Brush-drawn cartoon with a character explaining the idea | Story or explainer. Needs Node + Chrome + ffmpeg |
| 5 | Lemo-Opuscar | `styles/lemo-opuscar/STYLE.md` | 43 cinematic looks in code (`styles/lemo-opuscar/styles-list.md`) | Downloads its library from GitHub and npm packages on first run: ask first |

After choosing: **read that style's `STYLE.md` in full and follow it**; its `scripts/…` and `references/…` paths are
relative to the style folder. Styles run on the computer (Claude Code) only; in Claude chat, plan and script only.

## 2.7) Shared extras (`extras/`): open a file only when needed
| File | Open when |
|---|---|
| `extras/00-reference-and-brand.md` | **Always at the start** (§0) |
| `extras/style-learning.md` | The user names a reference video or says "learn this style / make it like this" |
| `extras/review-and-arabic-qa.md` | Before delivering any video with captions or drawn text (adapt to the language) |
| `extras/publish-pack.md` | The user wants a caption, description or hashtags for publishing |
| `extras/auphonic-audio.md` | Audio needs cleaning (noise, echo, hum, phone mic, "improve the sound") → **local first** (`extras/local_enhance.py`, DeepFilterNet, free, nothing uploaded); **Auphonic for echo and hard cases** (uploads audio to an outside service and uses credits: ask before uploading). |
| `extras/podcast-clips.md` | A long recording → several short reels |
| `extras/sfx/README.md` | **Any sound effects** (whoosh, impact, click, full sound design). Four sources: `extras/sound-kit/` (28 CC0 sounds) → **Openverse** (real free sounds with their licence, `extras/sfx/openverse_sfx.py`) → **real-sfx** (Clipwing: places sounds on the exact frame, then rates the mix) → **earshot** (Leon Lin, MCP that makes a sound when none exists). `CREDITS.md` for any sound that needs credit |
| `extras/dialect-dub.md` | "Make the video speak another language or dialect **in my voice**" → ElevenLabs (voice clone + Eleven v4 + lip sync). Paid ElevenLabs plan and the voice owner's consent. Dub after cutting silences and before captions, then return to the engine |
| `templates/` | `BRAND.example.md` and `REFERENCE-README.example.md` for the user |

## 3) Shared rules
- **Style:** you prepare everything, not the user. No command lists, no jargon, one thing at a time, say where you
  are and how long is left.
- **Step 0 always:** `00_setup.sh` in the engine folder. If downloads are missing (ffmpeg, Whisper, Chrome…), say in
  one line what will be downloaded and get approval before `--install`. **Never run `--update`** in Engine A.
- **Runs on the user's computer only** (local Claude Code), not in the cloud or Claude chat. Windows: `python` not
  `python3`, paths `C:/…` (`engine-egy/references/windows.md`).
- **No colour grading** of the person's footage, **colours from `theme.json` only**, **no publishing or scheduling**:
  delivery is a file.
- **Never invent words that were not said** (not in captions, not on the end card).
- **Verify before delivery** with the engine's checklist (safe zone, sync, audio, eye, size).
- **Short replies and token saving:** one contact sheet for preview; open `references/` only when needed.

## 4) Delivery summary
Show the final file, duration, how much silence was removed, number of scenes, final loudness, plus `.srt` and
`.txt`. Last line: which components were used.
