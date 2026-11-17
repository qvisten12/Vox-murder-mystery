# SPEC — The Incredible Story of the Cartel Olympics (Storyline A: The Evidence Board)

GOAL:    the viewer leaves knowing the cartel-games legend was a cover story for a fraud arrest and 18 months in an ordinary prison, and grins at the last line.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps.
TIME:    96.5 s x 30 = 2895 frames. Narrated (Kokoro `am_michael`, local); the voice is the clock (script/timing.json). No music: HeyGen is not signed in (sound.md §3), so effects only.
LOOK:    one medium, an evidence board.
         ground: corrugated kraft cardboard #B4895A with fibre noise (feTurbulence, ~12% opacity) and faint vertical flutes every 14 px.
         paper: photocopy white #F4F1EA cutouts with a 10 px white border, rotation -4..+4 deg, shadow 0 12px 20px rgba(20,12,4,.38).
         ink: #141210 for every illustration and every word that must be read; illustrations are flat black shapes with a 6 px halftone dot pattern in their mid-tones.
         accent: red #D7261E for string, push-pins, the circle marker and stamps (act two). Gold #D4A21F only on the medal.
         type: League Gothic (display, 140-260 px, tracking 0.01em); IBM Plex Mono 600 (typed evidence strips, 38-46 px, never under 34 px); captions Inter 900 54 px, white with 6 px black stroke.
OBJECTS: tattooed wrist (forearm with five-ring outline tattoo); wall calendar page FEB 2023 with a red header; side silhouette of a utility van; street-map scrap; a cell-like room with a mattress and a bucket and no window; a head-and-shoulders silhouette for "Don Paco"; a runner silhouette mid-stride; soccer ball, boxing glove, American football; a betting slip; a coach's play diagram; a scoreboard; a gold medal on a ribbon; an email printout; a clapperboard; a sticky note; a magazine card with eight tally marks; rubber-stamp impressions; prison bars; a vinyl record.
MOTION:  camera = one wrapper (#world) panning across a 3 x 3 board of 1920 x 1080 cells, power2.inOut 0.7-0.8 s, motion blur via one whoosh each; never a cut. Cards drop onto the board (scale 1.18 -> 1, rotation +7 -> r, expo.out 0.4 s) then a pin pops (0.12 s, 2 frames after); strips type in (clip-path steps, 0.03 s a char); paper slides in from the cell edge (power4.out 0.5 s); stamps slam (scale 2.2 -> 1 in 0.1 s power4.in, 6 px board shake 0.15 s); string draws (stroke-dashoffset 0.6 s power2.inOut). Everything holds dead still after it lands.
SHOTS:
  0.0-7.9    (0,0) tattoo card already landing at frame 0; "IF YOU WIN, YOU LIVE." / "IF YOU LOSE, YOU DIE." typed on the words; THE CARTEL OLYMPICS cut-letter title slaps on "Cartel"; red "?" scrawled on "story goes".
  7.9-18.5   (1,0) calendar FEB 9 2023 drops on "February", 9 circled on "ninth"; van slides on "grabbed"; map scrap on "Mexico City"; pan to (2,0): windowless room drops on "windowless".
  18.5-26.3  (2,1) Don Paco silhouette on "Don"; rings-spotted note on "Olympic rings"; runner card on "famous runner".
  26.3-37.5  (1,1) TOURNAMENT header on "secret tournament"; ball / glove / football on each word; betting slip on "bosses bet"; "THE LOSERS DIE." on "losers".
  37.5-45.4  (0,1) play diagram on "flag football team"; scoreboard WIN · OT on "overtime"; gold medal on "gold"; "WALKED HOME AT DAWN" strip on "walked".
  45.4-56.6  (0,2)->(1,2) email "Massive story." on "talent manager"; clapperboard on "Hollywood"; Peña note on "Michael Peña"; sticky condition on "serious magazine"; pan; magazine card on "Atlantic"; eight tally marks on "eight months".
  56.6-65.9  whip to (2,1): NO RECORD stamp on "no record"; runner label torn, ITALIAN RUNNER label pinned on "Italian".
  65.9-76.9  whip to (1,0): 9 re-circled on "ninth"; ARRESTED FOR FRAUD stamp on "arrested"; $700,000 card on the number; fake Beatles record on "fake".
  76.9-87.3  (2,0): bars draw over the room on "18 months"; ORDINARY PRISON label; hit-man card on "reformed hitman"; FELLOW INMATE stamp on "fellow".
  87.3-96.5  pull back to the whole board (scale 1/3) showing every stamp; NEVER HAPPENED stamp on the title on "never"; push into (2,2) clapperboard on "the movie"; BACK ON (REPORTEDLY) stamp on "back on"; source + sound credits hold to the end.
BANNED:  dark void ground; glow; purple/blue gradients; cream-paper ground with serif display; small mono caps labels (every typed strip >= 38 px and is evidence, not decoration); everything fading in; titles drifting after they land; corner HUD; three cards in a row; real faces or likenesses; any claim not in RESEARCH.md; invented scores or numbers.
QA:      t=0.2 (thumbnail: tattoo + board, not empty); t=3.4 (rule readable); t=17.9 (room); t=37.0 (tournament full); t=56.0 (believers chain); t=60.4 (NO RECORD); t=71.0 (ARRESTED stamp); t=86.0 (FELLOW INMATE); t=89.8 (whole board stamped); t=94.5 (end slate + credits).
