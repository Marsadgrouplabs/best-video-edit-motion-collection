# What is inside: components

This collection bundles other people's skills and tools next to our own. Each one keeps its author's credit and
licence (`NOTICE.md`, and the `LICENSE` inside its folder). The machine-readable list is `components.json`; the
installers read it too.

## The parts

**Core (always installed, about 100 KB):** this guide, `SKILL.md`, `NOTICE.md`, the Brand/Reference templates, and the
shared workflow notes (reference and brand, style learning, text QA, publish copy, podcast clips, audio clean-up,
the sound-effects guide). Small, and every other part relies on it.

| ID | Part | What it does | Why it matters | Size | Needs | Author · licence |
|---|---|---|---|---|---|---|
| `engine` | Editing engine (`engine-egy/`) | Full editor: cuts silences, turns talking video into 9:16 reels and ads, word-synced captions, montage, 2-camera podcast, touch studio, collage, audio clean-up, AI scenes | The core of the collection. Almost every video starts here | 30 MB | ffmpeg, Node, Python, Whisper (asks before installing) | Majed Alzaabi, video-ad-editor v3.4 · MIT (Egyptian edition fork) |
| `style-hyperframes` | HyperFrames | Clean motion graphics from HTML: titles, numbers, screens | Tech ads and product launches with no filming | 1.4 MB | Node, Chrome | HeyGen · Apache-2.0 |
| `style-onetake` | onetake | One continuous shot where each scene grows from the last | Eye-catching teasers | 9.4 MB | Node, Chrome | ⚠️ PolyForm Noncommercial: **not for client or paid work** |
| `style-collage` | Collage B-roll | Magazine cut-outs and halftones over scenes | Documentary and history videos | 6.7 MB | ⚠️ paid `GEMINI_API_KEY` | gbro-collage-broll · MIT |
| `style-clawd` | Clawd Animation | Brush-drawn cartoon with a character explaining the idea | Explainers and stories | 0.2 MB | Node, Chrome, ffmpeg | Claude Animation Base · MIT |
| `style-lemo` | Lemo-Opuscar | 43 cinematic looks made in code | Fast cinematic intros and promos | 30 KB + downloads its library on first run | Node, npm, internet (asks first) | Lemo-Opuscar · MIT |
| `sfx-kit` | Sound kit | 28 ready CC0 sounds: click, pop, tick, typing, drop | Instant sounds, no internet, no credit needed | 1 MB | nothing | uisfx, Kenney via Reel Studio · CC0 / MIT |
| `sfx-openverse` | Openverse search | Finds and downloads real free sounds, writes `CREDITS.md` | Whooshes, impacts, crowds… free and legal, no key | 8 KB | Python, internet | Marsad Labs script · MIT; idea by @moatassem.ai; each sound keeps its own licence |
| `sfx-real` | real-sfx | Finds the moments, places sounds on the exact frame, sets levels, rates the mix | Full sound design for motion and ads | 1.2 MB | Python, ffmpeg (optional extras ask first) | Clipwing · MIT, uisfx sounds CC0 |
| `sfx-earshot` | earshot + real-sound | MCP server that makes a sound from a description, plus a licensed-sound design workflow | When no library has the sound you need | 0.5 MB + optional 1.1 GB models | Python venv, MCP setup | Leon Lin · MIT |
| `dub` | Dialect / language dub | The video speaks another language or dialect in the speaker's own voice, with lip sync | Reach new audiences without re-filming | 8 KB | ⚠️ paid ElevenLabs plan, the voice owner's consent | Workflow after Aly Elazab · our own words |

**Recommended set** (`recommended: true` in `components.json`): the engine, HyperFrames, Clawd, Lemo, the sound kit,
Openverse, real-sfx and dub. Ask before onetake (non-commercial), collage (paid key) and earshot (larger setup).

## Install flow (for Claude)
When the user asks to install, set up, update or add this collection:

1. **Find the source**: the cloned repo (`skills/best-video-edit-motion-collection/`) or the unzipped full zip.
   Read `components.json` from there.
2. **Show the menu** in the user's language: one line per part with what it does and why it matters (from the table),
   its size, and a ⚠️ for anything paid, non-commercial or large. Group by engine, styles, sound, voice.
3. **Ask once**: "Install everything, the recommended set, or pick parts?" Wait for the answer. If they pick, take a
   list of IDs or names.
4. **Install**: run the installer with the chosen IDs, or copy the core paths plus each chosen part's `paths` into
   `~/.claude/skills/best-video-edit-motion-collection/` (Codex: `~/.agents/skills/`). Back up an existing copy first.
   ```
   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Components recommended
   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Components engine,sfx-kit,sfx-openverse
   bash install.sh claude all
   bash install.sh claude engine,sfx-kit,dub
   ```
5. **Report**: what was installed, what was skipped, and how to add a part later (same command with that ID).
   Parts with their own setup (earshot MCP, Lemo library, engine downloads) are set up only when first used, with
   the user's approval.

**Adding a part later or updating:** same flow; show only what is new or changed, and keep the parts already installed.
**At work time:** if a part's folder is missing, it was not installed: say so in one line and offer to add it.

## Adding a new component (for maintainers)
1. Put it in its own folder (keep its `LICENSE`; rename a nested `SKILL.md` to `GUIDE.md`).
2. Add a row to the table above and an entry to `components.json`.
3. Add a credit line to `NOTICE.md` (author, link, licence, commit if pinned).
4. Point to it from the right section of `SKILL.md`, then bump the version and the changelog.
