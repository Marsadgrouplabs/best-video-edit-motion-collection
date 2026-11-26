<!-- Same content as the standalone skill `elevenlabs-dialect-dub`. Keep both in sync. -->

# One take, every dialect (ElevenLabs)

Film once in your own language. Selected moments of the same take then play in other dialects or languages, in
the speaker's own voice, with the mouth redrawn to the new words. Workflow credit: Aly Elazab (growwithazab), see the skill's `NOTICE.md`.

Reply in the same language and dialect the user writes in.

## Before you start (say these once)

- **Paid ElevenLabs plan needed.** Voice cloning and lip sync use credits. A reference project: about 30 s of
  switched video used about 52,000 credits (Creator plan level). One 9 s lip-sync clip cost about 7,400 credits.
  Hover the price in ElevenLabs before generating, and test the hardest clip first.
- **Consent.** Clone only the user's own voice, or a voice whose owner gave written permission. Never clone a
  client or a public figure without it. For client videos, the client must approve the final dialect lines.
- **Disclosure.** If the platform or the client asks for AI disclosure, label the switched parts as AI-dubbed.

## The core rule: the new line must fit the old body

Lip sync moves only the mouth. Hands, shoulders, head and pauses stay exactly as filmed. So each new line needs the
same phrases, in the same order, at about the same length as the original (within about 15%). Then a shrug still lands
on the right word and nobody sees the seam.

## Workflow

| Stage | Exactly how |
|---|---|
| 1. Pick the moments | 4 to 6 sections of 4 to 10 s each, mouth clearly visible. Write each section phrase by phrase with what the hands do on each phrase. Switch on the line AFTER the one that names the language ("I always wanted to speak French" stays in the original). |
| 2. Clone the voice | ElevenLabs → Voices → Add a new voice → Instant Voice Clone. 1 to 2 minutes of the speaker alone: no music, no echo, no second voice. Extract it with ffmpeg: `ffmpeg -i take.mp4 -ss START -t 120 -vn -ac 1 -ar 44100 clone.wav` |
| 3. Rewrite the lines | Phrase for phrase, same order, length within about 15%. Use the words a native spots instantly (table below). A native speaker checks every line before any credits are spent. |
| 4. Make the audio | Text to Speech, the clone, model **Eleven v4** (v3 sounded less like the speaker in the reference project). Put a comma or "…" between phrases. Generate 3 or 4 takes and let the user pick by ear. A word that keeps coming out wrong: use a synonym. Lay it over the clip and nudge the speed 0.9 to 1.15x until the words land on the gestures. |
| 5. Sync the lips | Export each section as **MP4** (a .mov can be rejected): `ffmpeg -i edit.mp4 -ss S -t D -c:v libx264 -crf 16 -c:a aac sec01.mp4`. ElevenLabs → Image & Video → Lip sync → model Sync 3, clip as Video, the new audio as Speech. Check the price, run the hardest clip first. |
| 6. Put it back | Swap each synced clip in for the original section and cut right after the last word. Keep captions in the language actually spoken in each section, add a flag or dialect label per section, and show the untouched take once in a small box with its real sound. That reveal is what makes viewers believe it. |

If an ElevenLabs connector or MCP is available in the session, use it for text to speech and voice listing.
Voice cloning and lip sync are usually done in the ElevenLabs web app: give the user the exact clicks above,
then continue with the files they download.

## Signature words per dialect (a starting list, a native still checks)

| Dialect | Words that make it obvious |
|---|---|
| Saudi (Najdi / white) | «هالمقطع»، «وش»، «أبي»، «زين»، «مرّة» (very)، «يعطيك العافية» |
| Emirati / Kuwaiti (Khaleeji) | «شو»، «وايد»، «عساك»، «هالشي»، «يالله» |
| Lebanese | «هيدا/هيدي»، «عم بحكي»، «كتير»، «شو في»، «هلّق» |
| Moroccan | «بزاف»، «كنهضر»، «واخا»، «دابا»، «مزيان» |
| Egyptian | «دلوقتي»، «أوي»، «إزاي»، «عايز»، «كده» |
| Levantine (Syrian / Jordanian) | «هلأ»، «كتير»، «شو»، «بدّي»، «منيح» |

## When it looks wrong

| You see | Fix |
|---|---|
| Lips move, body frozen | The new line is longer: shorten it so it ends where the real speech ended |
| Gestures do not match the words | Rewrite phrase by phrase, then time each phrase onto its gesture |
| The dialect sounds generic | Add the dialect's signature words; ask a native to rewrite one phrase |
| The voice does not sound like the speaker | Longer, cleaner clone sample; try Eleven v4; or a Professional Voice Clone |
| One word is always mispronounced | Synonym, or spell it phonetically in Arabic letters |

## Better voice: Professional Voice Clone

At least 30 minutes of the speaker alone, Creator plan or higher, a few hours of training. Record in one sitting,
same mic, same spot, talking to one friend. Change the mood every few minutes (calm, teaching, excited, telling a
story, laughing, serious, surprised). End with the usual hooks and calls to action, each said twice.

## Delivery

- The final MP4, the list of switched sections with their timecodes and dialects, and the exact lines used.
- Credits spent, if the user shared them. Any line a native has not checked is flagged.
- Inside best-video-edit-motion-collection: do the dub on the cut timeline FIRST (after silence removal, before captions), then hand
  the synced clips back to the chosen engine for captions (in the language actually spoken), motion and export.
