# REVIEW: The Chip in the Middle

## Creative calls
- Built storyline **A**: one map world, with a GPU at the centre and a silhouette standing behind it. Red threads run from Washington, China, the suspected-asset report and the fallout to the man. They tighten as the pressure builds and go slack when he resigns, and the film ends on the chip alone.
- Not built: **B: Nine Days** and **C: The Empty Jacket** (STORYLINES.md).
- Voice: the person chose the free local **Kokoro `af_heart`**. HeyGen's Jennifer was refused because the HyperFrames Free plan doesn't include HeyGen voices, and the HeyGen API key has no API credits. Nothing was charged.
- Music: HeyGen catalog "informative documentary explainer" (0-26.6 s), then "low, rhythmic, tense investigative" from the New York Times report onwards, both at 0.13 under the voice.
- Smoothness: root `data-motion-blur="on"`; camera moves of 1.5-1.9 s on `power3.inOut`/`expo.inOut`; cards arrive on 0.8 s `expo.out` with a blur-to-sharp; no bounces. The opening holds a slow 4.6 s `sine.inOut` push.
- Accuracy: Alice Huang is always "suspected", with "no public proof" and "officials haven't said" on screen. The employees in the later reports are not named. Quotes are verbatim from Huang's letter, the board statement and China's foreign ministry. Sources are credited at the end.

## Measured vs looked at
- `check`: 0 errors. Warnings kept on purpose:
  - `text_below_floor`: only in the 0.5x / 0.72x wide shots.
  - `line_unread`: "EXPORT RULES" passes by during a camera pan.
  - `composition_file_too_large` / `timeline_track_too_dense`: one continuous-camera world.
- Looked at 14 QA stills, then fixed the following:
  - a duplicate `#world` id that left the frame empty;
  - the head cropped at the reveal;
  - the stamp covering Alice Huang's name;
  - "HOW CLOSE?" colliding with labels;
  - fallout cards under the captions in the wide shot;
  - a cluttered ending.
- The sound was measured, not heard.

## Weakest shot / with more time
- The wide fallout shot (57-66 s) is dense at 0.5x; it would read better split into two closer moves.
- The voice: HeyGen Jennifer (needs HyperFrames Pro or HeyGen API credits) would be smoother than Kokoro. Re-timing is automated (script/build.py).
- The news moves fast: re-check RESEARCH.md against current reporting before publishing.
