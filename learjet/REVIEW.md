# REVIEW: 35,000 feet in about a minute (Learjet 60, Florida)

Built from the person's own script (SCRIPT.md): every [A#] cue is keyed to the narrator's actual word time (script/scenes.py `cue()`), not to the approximate times in the table.

## Calls made
- Six scenes: hook (black) → map (route, then a zoom into South Florida for the storms) → mayday → ground → envelope/tail → NTSB. The map scene covers the script's rows 2 and 3 as one continuous zoom.
- Real geography: coastlines baked from Natural Earth / US Atlas (world-atlas, us-atlas) into a fixed SVG, so the render fetches nothing.
- Voice: Kokoro `af_heart` at 0.95 speed (local; HeyGen voices need Pro or API credits). r5 was split to add the ~1 s of silence the script asks for after "were killed".
- Music: HeyGen catalog. "Serious cinematic documentary, minimal piano and strings, investigative" plays until the MAYDAY, where it cuts out (A10). It stays silent through the crash and the ground scene, then "serious documentary ambient, respectful, subtle strings and piano" carries the explanation and the close. Both at 0.12.
- Sound effects are sparse: a soft tick on the opening number, a whoosh into the zoom, one low hit on MAYDAY, and a tick on the recorder.

## Deviations from the cue sheet (on purpose)
- **A12:** the script says "bar 2 doubles", but the overspeed call is an altitude (20,000 ft), not a descent rate. So the chart shows the two reported rates (10,000 and 22,000 ft/min), and the overspeed is an airspeed needle swinging into the red, labelled "OVERSPEED AT 20,000 FT". No invented number.
- **A15:** the street map is a schematic labelled "not to scale". No NTSB photo is used (none in the project).
- **A23:** "NTSB" is plain type with the case number. The agency logo isn't reproduced.

## Measured vs looked at
- `check`: 0 errors. Kept on purpose: the closing credits line holds 3.5 s on black; `timeline_track_too_dense` (captions file).
- Looked at 22 stills. Fixed the following:
  - the pin not appearing (GSAP overwrote its translate);
  - the 22,000 label and the gauge colliding with the chart title;
  - map labels ballooning in the zoom;
  - storm cells sitting off the route;
  - clipped envelope labels;
  - the pin covering the road name.
- The sound was measured, not heard.

## Before publishing
- The cause is undetermined; the NTSB preliminary report is expected around early December. If it's out, swap the last line (SCRIPT.md, "Optional final line").
