# Pinned install (Marsad)

- Source: https://github.com/Clipwing/skills, folder `skills/real-sfx`
- Commit: `edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e` (2026-10-21)
- Bundled into best-video-edit-motion-collection 2026-11-21 (without vendor/, tests/, evals/). Run `python scripts/setup.py init --uisfx` once for the 78 UI cues, or add a library.
  all false positives (exec/env/--no-check patterns in tests and normal options; no outbound data, no remote code).
- Licence: scripts MIT, bundled uisfx sounds CC0 (see README "Licences"). Author: Clipwing.

## Do not auto-update
Update only on purpose: clone the new commit into an empty folder, run SkillSpector, read the diff against the commit
above, then replace this folder and update the commit line.

## Local changes (re-apply after an update)
1. `scripts/listen_page.py`: `serve --lan` is disabled; the server binds to 127.0.0.1 only.
2. `scripts/phone_pack.py` (new): builds one small MP4 of the moments to listen to, to send to a phone.
3. `SKILL.md`, `README.md`: the `--lan` lines point to `phone_pack.py`.
