# SPEC: The Chip in the Middle (Jensen Huang scandal explainer)

GOAL:    the viewer understands why one CEO's affair became a US-China security story and cost him Nvidia, without the film claiming more than the reporting does.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps, motion blur on (root `data-motion-blur="on"`).
TIME:    100 s x 30 = 3000 frames. The narration (Kokoro `af_heart`, local; the HeyGen voice needs Pro or API credits) is the clock: script/timing.json.
         Music: HeyGen catalog "informative documentary explainer" (0-26.4 s), then "low, rhythmic, tense investigative" (26.4 s-end), at 0.13.
LOOK:    a single map world, 5760 x 3240 (3 x 3 cells), seen through one camera.
         ground: stone-grey paper #DCDAD2 with 8% fibre noise and a faint 120 px map grid (#15171A at 5%).
         cards: #F7F6F2, radius 6, shadow 0 18px 36px rgba(21,23,26,.18).
         ink: #15171A. accent: Nvidia green #76B900, only on the chip die and the $4.5T figure. Threads and stamps: red #D8322A.
         type: Archivo Black for display (90-170 px world), Inter 600/800 for body (>= 40 px world, >= 56 px on cards seen at 0.5 scale), JetBrains Mono 600 for dates (>= 40 px).
OBJECTS: a GPU package (graphite substrate, gold contact pads, green die grid); a head-and-shoulders silhouette in a leather jacket (no likeness);
         the Capitol dome; two chips of different sizes (H20, H200); a news-report card (text only, no masthead mimicry); a woman's silhouette card;
         a letter on paper; a desk nameplate; a falling share-price arrow (no numbers); a petition sheet with a rolling counter.
MOTION:  smooth above all. Camera moves: 1.3-1.7 s, `power3.inOut`; a pull-back is `expo.inOut` 1.6 s. Cards arrive on `expo.out` 0.8 s
         (y 40 -> 0, scale 0.97 -> 1, blur 8 -> 0 px, opacity 0 -> 1). Exits run 0.4 s `power2.in`. Threads draw over 1.0 s `power2.inOut`
         and tighten (sag -> straight) over 1.2 s `power3.inOut`. Numbers roll over 1.4 s `power2.out`. Nothing bounces, and every landed title holds still.
SHOTS:
  0-8.8     tight on the chip die (scale 1.5, slow push); pull back on "one man" to reveal the silhouette standing behind it.
  8.8-16.9  labels flow into the chip (DATA CENTERS / AI MODELS / CLOUD) on "AI boom"; $4.5 TRILLION rolls up on "trillion".
  16.9-26.4 glide to Washington: Capitol and "WHO MAY BUY WHICH CHIP" card on "decides"; long pan to China: H20 -> H200 grows on "far stronger"; threads to the chip.
  26.4-45.0 fly to the report node: report card on "Times", Alice Huang card on "Alice", SUSPECTED ASSET tag on "asset"; NO RELATION / NO PUBLIC PROOF tags; China quote; the camera eases out as the thread to the silhouette draws, "HOW CLOSE?".
  45.0-53.8 the letter: NOV 8 header, the two quoted lines blur in on the words.
  53.8-67.0 the fallout node: board quote card; pull back to 0.5 scale on "threads kept pulling", every thread tightens; SHARES FELL, CONGRESS, NEW REPORTS cards.
  67.0-77.2 the nameplate: JENSEN HUANG / CEO struck on "resigned"; RESIGNED NOV 12 stamp; the COLETTE KRESS / INTERIM CEO plate slides in on "Colette". The silhouette leaves the centre.
  77.2-90.0 pass the empty centre to the petition: 170,000+ rolls, BOARD: NOT CONSIDERING IT (REPORTEDLY), SPY? NO CONCLUSION.
  90.0-100  back to the chip, tight, no one behind it; sources line at the end.
BANNED:  dark void ground; glow, neon, lens flare; purple/blue gradients; cream paper with serif; everything centred; fade-and-slide-up on every element;
         bouncy springs; titles drifting after landing; real faces; fake mastheads or logos; any claim not in RESEARCH.md; naming the employees in the later reports.
QA:      t=0.3, 7.6, 15.6, 24.8, 35.8, 43.6, 52.9, 62.0, 70.5, 74.0, 81.0, 88.4, 95.0, 99.0.
