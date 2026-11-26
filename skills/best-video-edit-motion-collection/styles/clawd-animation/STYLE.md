---
name: style-clawd-animation
description: "Hand-brushed cartoon animation style (Claude Animation Base): a character (Clawd) moves, acts and explains an idea in painted p5.js + p5.brush scenes with boiling linework, brush-stroke transitions and handmade feel, rendered to MP4. Use when the user wants a cartoon / hand-drawn / animated character video that explains a story or idea, or picks this style from the video style menu."
---

# Clawd Animation (hand-brushed cartoon)

Source: github.com/JohnHeibel/ClaudeAnimationBase (MIT). This folder is the starter kit.

## How to use
1. Read `ANIMATION_GUIDE.md` fully first. It holds the rules (handmade, alive, one piece, no text, transitions always, something happens in every scene), the workflow and the full API.
2. Storyboard before coding, then build shot by shot in `src/scenes/` (copy the demo as an example), render contact sheets to check your own work, and write `out/video.mp4`.
3. Ask the user for the story or idea and the length; do not invent claims they did not make.

## Running it (local Claude Code only)
Needs Node.js, Google Chrome and ffmpeg.
```bash
npm install
node render.mjs --clip --out=out/video.mp4
```
Open `studio.html` in Chrome to scrub. If Chrome is not in a standard place pass `--chrome=<path>` or set `CHROME_PATH`. No dedicated GPU: avoid p5.brush watercolour fills, they render slowly. `gpu_probe.mjs <chrome path>` shows which renderer works.

In claude.ai chat this skill can only plan: storyboard, shot list and script. It cannot render.

## Files
`ANIMATION_GUIDE.md` rules and API · `src/clawd.js` character · `src/core.js` painting/timing/camera · `src/timeline.js` shots and transitions · `src/config.js` length and tempo · `src/scenes/` the video · `render.mjs` headless renderer.
