"""Generates every scene in compositions/ from script/timing.json and script/map-land.svg.frag.
Cue times are scene-local and taken from the narration's word timings (script/rN.words.json)."""
import json

T = {s['id']: s for s in json.load(open('script/timing.json'))}
LAND = open('script/map-land.svg.frag').read()


def cue(sid, word_index_or_text, nth=1, offset=0.0):
    """Scene-local time of a narration word (by its text, nth occurrence)."""
    s = T[sid]
    lead = s['start'] - s['scene_start']
    n = 0
    for w in s['words']:
        if w['text'].lower().strip('.,?!:') == word_index_or_text.lower():
            n += 1
            if n == nth:
                return round(lead + w['s'] + offset, 3)
    raise KeyError((sid, word_index_or_text))


BASE_CSS = """
    #root { position: absolute; inset: 0; overflow: hidden; color: #1b1b1b; font-family: "Inter", sans-serif; }
    .paper {
      position: absolute; inset: 0; background-color: #ece6da;
      background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' seed='4'/><feColorMatrix values='0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0.16 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>");
    }
    .card { position: absolute; background: #f8f5ee; border-radius: 4px; box-shadow: 0 14px 30px rgba(40, 30, 15, 0.18); padding: 28px 36px; }
    .disp { font-family: "Archivo Black", sans-serif; line-height: 0.95; }
    .mono { font-family: "JetBrains Mono", monospace; font-weight: 600; }
    .lbl { font-family: "JetBrains Mono", monospace; font-weight: 600; font-size: 34px; letter-spacing: 0.04em; color: #55504a; }
    .hl { background: linear-gradient(transparent 12%, #ffd84a 12%, #ffd84a 88%, transparent 88%) no-repeat; background-size: 0% 100%; padding: 0 6px; }
"""

GSAP_HELPERS = """
    const tl = gsap.timeline({ paused: true });
    function inCard(sel, t, extra) {
      tl.fromTo(sel, Object.assign({ opacity: 0, y: 30, scale: 0.97, filter: "blur(8px)" }, (extra && extra.from) || {}),
        Object.assign({ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.8, ease: "expo.out" }, (extra && extra.to) || {}), t);
    }
    function draw(sel, t, d, ease) {
      tl.fromTo(sel, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: ease || "power2.inOut" }, t);
    }
    function swipe(sel, t, d) {
      tl.fromTo(sel, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: d || 0.5, ease: "power2.out" }, t);
    }
"""


def person(i, color="#1b1b1b", size=64):
    return (f'<svg class="pp" id="PFX-p{i}" width="{size}" height="{int(size*1.35)}" viewBox="0 0 64 86">'
            f'<circle cx="32" cy="18" r="15" fill="{color}"/><path d="M6 86 C6 52 18 40 32 40 C46 40 58 52 58 86 Z" fill="{color}"/></svg>')


def nine(prefix, size=64):
    icons = [person(i, '#1b1b1b', size) for i in range(1, 8)] + [person(i, '#2e64a8', size) for i in (8, 9)]
    return ''.join(icons).replace('PFX', prefix)


def scene(cid, dur, css, body, js):
    return f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-layout-allow-overflow data-layout-allow-overlap>
{body}
  </div>
  <script>{GSAP_HELPERS}{js}
    tl.to({{}}, {{ duration: 0.01 }}, {round(dur - 0.02, 3)});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


files = {}

# ---------------------------------------------------------------- S1 hook (black)
r = 'r1'; D = T[r]['scene_dur']
a2 = cue(r, 'in', 1)
files['hook'] = scene('hook', D, """
    #bg { position: absolute; inset: 0; background: #0d0d0d; }
    #alt { position: absolute; left: 0; right: 0; top: 330px; text-align: center; color: #f3efe6; font-size: 230px; letter-spacing: -0.02em; }
    #alt-unit { position: absolute; left: 0; right: 0; top: 590px; text-align: center; color: #9c968b; font-size: 54px; letter-spacing: 0.3em; }
    #watch { position: absolute; left: 1450px; top: 150px; width: 300px; height: 340px; }
    #watch-label { position: absolute; left: 1410px; top: 500px; width: 380px; text-align: center; color: #f3efe6; font-size: 60px; }
""", """
    <div id="bg"></div>
    <div id="alt" class="mono"><span id="alt-num">41,000</span></div>
    <div id="alt-unit" class="mono">FEET</div>
    <svg id="watch" viewBox="0 0 300 340">
      <rect x="125" y="0" width="50" height="30" rx="6" fill="#f3efe6" />
      <circle cx="150" cy="190" r="130" fill="none" stroke="#f3efe6" stroke-width="14" />
      <path id="watch-arc" pathLength="1" d="M150 80 A110 110 0 1 1 149.9 80" fill="none" stroke="#c8372d" stroke-width="26" />
      <line id="watch-hand" x1="150" y1="190" x2="150" y2="92" stroke="#f3efe6" stroke-width="10" stroke-linecap="round" />
    </svg>
    <div id="watch-label" class="mono">≈ 1 MIN</div>
""", f"""
    tl.fromTo("#alt", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "steps(6)" }}, 0.5);
    
    const o = {{ v: 41000 }};
    tl.fromTo(o, {{ v: 41000 }}, {{ v: 1200, duration: {a2 - 1.3:.3f}, ease: "power2.in",
      onUpdate: () => {{ document.querySelector("#alt-num").textContent = (Math.round(o.v / 100) * 100).toLocaleString("en-US"); }} }}, 1.3);
    tl.fromTo(["#watch", "#watch-label"], {{ opacity: 0, scale: 0.96 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {a2:.3f});
    draw("#watch-arc", {a2:.3f}, 0.8, "power2.out");
    tl.fromTo("#watch-hand", {{ rotation: 0, svgOrigin: "150 190" }}, {{ rotation: 360, svgOrigin: "150 190", duration: 0.8, ease: "power2.out" }}, {a2:.3f});
""")

# ---------------------------------------------------------------- S2+S3 map (r2 + r3)
r2s, r3s = T['r2'], T['r3']
D = round(r2s['scene_dur'] + r3s['scene_dur'], 3)
off3 = r2s['scene_dur']
c = lambda w, n=1, o=0.0: cue('r2', w, n, o)
c3 = lambda w, n=1, o=0.0: round(off3 + cue('r3', w, n, o), 3)
icons = nine('m', 58)
files['map'] = scene('map', D, """
    #sea { position: absolute; inset: 0; background: #d5dfe0; }
    #mapcam { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    #mapcam svg { position: absolute; inset: 0; }
    .land { fill: #ece6da; stroke: #8f877a; stroke-width: 1.4; vector-effect: non-scaling-stroke; }
    .land.us { fill: #f3eee3; }
    #texture { position: absolute; inset: 0; opacity: 0.55; mix-blend-mode: multiply; }
    .city { font-family: "JetBrains Mono", monospace; font-weight: 600; font-size: 30px; fill: #1b1b1b; }
    #route { fill: none; stroke: #c8372d; stroke-width: 6; stroke-linecap: round; vector-effect: non-scaling-stroke; }
    #jetcard { left: 110px; top: 560px; width: 700px; }
    #icons { display: flex; gap: 10px; margin-top: 18px; align-items: flex-end; }
    #profile { left: 1360px; top: 70px; width: 470px; height: 300px; padding: 22px 26px; }
    #crew { left: 110px; top: 110px; width: 760px; }
    #crew .q { font-size: 50px; font-weight: 800; line-height: 1.25; margin-top: 14px; }
    #frost { position: absolute; inset: 0; pointer-events: none;
      background: radial-gradient(ellipse at center, rgba(220,235,245,0) 55%, rgba(225,238,248,0.75) 100%); }
    #climb { left: 1330px; top: 110px; width: 480px; height: 330px; padding: 22px 26px; }
""", f"""
    <div id="sea"></div>
    <div id="mapcam">
      <svg viewBox="0 0 1920 1080">
        <defs>
          <radialGradient id="storm-y"><stop offset="0" stop-color="#f5c400" stop-opacity="0.85"/><stop offset="0.7" stop-color="#f5c400" stop-opacity="0.35"/><stop offset="1" stop-color="#f5c400" stop-opacity="0"/></radialGradient>
          <radialGradient id="storm-r"><stop offset="0" stop-color="#d8261c" stop-opacity="0.9"/><stop offset="0.6" stop-color="#e8641c" stop-opacity="0.55"/><stop offset="1" stop-color="#f5c400" stop-opacity="0"/></radialGradient>
        </defs>
        <g id="land">{LAND}</g>
        <g id="storms">
          <circle class="cell" cx="1352" cy="582" r="30" fill="url(#storm-y)" />
          <circle class="cell" cx="1392" cy="600" r="24" fill="url(#storm-r)" />
          <circle class="cell" cx="1428" cy="622" r="30" fill="url(#storm-y)" />
          <circle class="cell" cx="1372" cy="636" r="22" fill="url(#storm-r)" />
          <circle class="cell" cx="1450" cy="600" r="18" fill="url(#storm-y)" />
          <circle class="cell" cx="1318" cy="560" r="20" fill="url(#storm-y)" />
        </g>
        <path id="route" pathLength="1" d="M198 332 C700 380 1150 520 1422 611 S1600 690 1663 705" />
        <circle id="dot-aus" cx="198" cy="332" r="9" fill="#1b1b1b" />
        <circle id="dot-ele" cx="1663" cy="705" r="9" fill="#1b1b1b" />
        <text id="t-aus" class="city" x="222" y="322">AUSTIN</text>
        <text id="t-ele" class="city" x="1560" y="760">N. ELEUTHERA</text>
      </svg>
    </div>
    <div id="texture" class="paper"></div>
    <div id="frost"></div>

    <div id="jetcard" class="card">
      <svg id="jet" width="420" height="120" viewBox="0 0 420 120">
        <path d="M20 66 C40 50 120 46 300 48 C350 48 390 54 404 62 C390 70 350 76 300 76 L120 76 C70 76 36 74 20 66 Z" fill="#1b1b1b" />
        <path d="M60 52 L36 10 L64 10 L104 50 Z" fill="#1b1b1b" />
        <path d="M30 14 L86 12 L84 20 L30 22 Z" fill="#1b1b1b" />
        <path d="M200 76 L150 112 L190 112 L250 76 Z" fill="#1b1b1b" />
        <rect x="70" y="40" width="54" height="22" rx="10" fill="#1b1b1b" />
      </svg>
      <div class="disp" style="font-size: 54px; margin-top: 6px">LEARJET 60</div>
      <div class="lbl" style="margin-top: 8px">N722BD · CHARTER FLIGHT</div>
      <div id="icons">{icons}</div>
    </div>

    <div id="profile" class="card">
      <div class="lbl">ALTITUDE, FT</div>
      <svg width="418" height="210" viewBox="0 0 418 210" style="margin-top: 8px">
        <text x="0" y="46" class="mono" font-size="28" fill="#55504a">41k</text>
        <text x="0" y="120" class="mono" font-size="28" fill="#55504a">35k</text>
        <line x1="70" y1="38" x2="410" y2="38" stroke="#c9c1b3" stroke-width="2" stroke-dasharray="6 6" />
        <line x1="70" y1="112" x2="410" y2="112" stroke="#c9c1b3" stroke-width="2" stroke-dasharray="6 6" />
        <path id="prof-cruise" pathLength="1" d="M70 38 H230" fill="none" stroke="#1b1b1b" stroke-width="8" stroke-linecap="round" />
        <path id="prof-desc" pathLength="1" d="M230 38 L280 112 H410" fill="none" stroke="#1b1b1b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>

    <div id="crew" class="card">
      <div class="lbl">CREW REPORTED</div>
      <div class="q"><span id="hl-ice" class="hl">light clear ice</span> and<br/><span id="hl-turb" class="hl">moderate turbulence</span></div>
    </div>
    <div id="climb" class="card">
      <div class="lbl">ASKED TO CLIMB</div>
      <svg width="428" height="240" viewBox="0 0 428 240" style="margin-top: 8px">
        <line x1="10" y1="60" x2="418" y2="60" stroke="#2e64a8" stroke-width="5" stroke-dasharray="14 10" />
        <text x="10" y="44" class="mono" font-size="30" fill="#2e64a8">CLEARED 37,000</text>
        <text x="10" y="226" class="mono" font-size="30" fill="#55504a">~35,000</text>
        <path id="climb-line" pathLength="1" d="M10 190 H190 C260 190 300 110 360 72" fill="none" stroke="#1b1b1b" stroke-width="8" stroke-linecap="round" />
      </svg>
    </div>
""", f"""
    tl.set("#mapcam", {{ transformOrigin: "0px 0px" }}, 0);
    tl.fromTo("#mapcam", {{ x: 0, y: 0, scale: 1 }}, {{ x: -40, y: -20, scale: 1.04, duration: {off3 - 0.7:.2f}, ease: "sine.inOut" }}, 0);
    // A3 jet + tail number
    inCard("#jetcard", {c('learjet', 1, -0.1)}, {{ from: {{ x: -200, y: 0 }}, to: {{ x: 0 }} }});
    // A4 nine people, one by one
    tl.fromTo("#icons .pp", {{ opacity: 0, y: 14, scale: 0.6 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.16 }}, {c('seven')});
    // A5 route draws
    tl.fromTo(["#dot-aus", "#t-aus"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('austin', 1, -0.3)});
    draw("#route", {c('from')}, 1.6, "power2.inOut");
    tl.fromTo(["#dot-ele", "#t-ele"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('bahamas', 1, 0.1)});
    // A6 altitude profile steps 41k -> 35k
    inCard("#profile", {c('cruised')});
    draw("#prof-cruise", {c('41,000')}, 0.8, "power2.out");
    draw("#prof-desc", {c('then')}, 1.1, "power2.inOut");
    // out with the overview cards, zoom into South Florida
    tl.to(["#jetcard", "#profile"], {{ opacity: 0, y: 20, duration: 0.45, ease: "power2.in" }}, {off3 - 0.9:.3f});
    tl.to("#mapcam", {{ x: 960 - 1405 * 3.4, y: 540 - 630 * 3.4, scale: 3.4, duration: 1.9, ease: "power3.inOut" }}, {off3 - 0.6:.3f});
    tl.to(["#t-aus", "#dot-aus", "#t-ele"], {{ opacity: 0, duration: 0.4 }}, {off3 - 0.6:.3f});
    // A7 storms bloom and pulse along the route
    tl.fromTo("#storms .cell", {{ scale: 0, transformOrigin: "50% 50%", opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 1.2, ease: "expo.out", stagger: 0.12 }}, {c3('thunderstorms', 1, -0.2)});
    tl.to("#storms .cell", {{ scale: 1.18, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: 5, stagger: 0.18 }}, {c3('thunderstorms', 1, 1.2)});
    // A8 transcript card + highlighter + frost
    inCard("#crew", {c3('reported', 1, -0.2)});
    swipe("#hl-ice", {c3('light')}, 0.7);
    swipe("#hl-turb", {c3('moderate')}, 0.7);
    tl.fromTo("#frost", {{ opacity: 0 }}, {{ opacity: 1, duration: 2.6, ease: "power1.inOut" }}, {c3('ice')});
    // A9 asked to climb -> cleared 37,000
    inCard("#climb", {c3('asked', 1, -0.1)});
    draw("#climb-line", {c3('cleared', 1, 0.2)}, 1.4, "power2.inOut");
""")

# ---------------------------------------------------------------- S4 mayday
r = 'r4'; D = T[r]['scene_dur']; c = lambda w, n=1, o=0.0: cue(r, w, n, o)
files['mayday'] = scene('mayday', D, """
    #left { position: absolute; left: 0; top: 0; width: 900px; height: 1080px; background: #e4ddcf; }
    #mayday { position: absolute; left: 150px; top: 120px; padding: 18px 40px 14px; background: #c8372d; color: #fff; font-size: 120px; z-index: 5; }
    #jetfront { position: absolute; left: 160px; top: 420px; width: 580px; height: 300px; }
    #bank-label { position: absolute; left: 260px; top: 760px; font-size: 70px; }
    #chart { position: absolute; left: 990px; top: 150px; width: 560px; height: 760px; }
    .bar { position: absolute; bottom: 120px; width: 190px; background: #1b1b1b; transform-origin: 50% 100%; }
    .bval { position: absolute; width: 230px; text-align: center; font-size: 40px; }
    .bcap { position: absolute; bottom: 30px; width: 230px; text-align: center; font-size: 30px; color: #55504a; }
    #gauge { position: absolute; left: 1580px; top: 330px; width: 250px; height: 250px; }
""", f"""
    <div class="paper"></div>
    <div id="left"></div>
    <div id="mayday" class="disp">MAYDAY</div>
    <svg id="jetfront" viewBox="0 0 580 300">
      <g id="jet-roll">
        <rect x="20" y="138" width="540" height="22" rx="10" fill="#1b1b1b" />
        <circle cx="290" cy="150" r="54" fill="#1b1b1b" />
        <path d="M282 96 L298 96 L300 18 L280 18 Z" fill="#1b1b1b" />
        <rect x="200" y="12" width="180" height="14" rx="6" fill="#1b1b1b" />
        <circle cx="290" cy="150" r="22" fill="#e4ddcf" />
      </g>
      <path id="protractor" pathLength="1" d="M440 150 A150 150 0 0 0 365 20" fill="none" stroke="#c8372d" stroke-width="8" stroke-dasharray="1" />
      <line x1="140" y1="150" x2="440" y2="150" stroke="#8f877a" stroke-width="3" stroke-dasharray="10 8" />
    </svg>
    <div id="bank-label" class="disp" style="opacity: 0">60° BANK</div>
    <div id="chart">
      <div class="lbl" style="position: absolute; left: 0; top: -80px; white-space: nowrap">REPORTED DESCENT, FT/MIN</div>
      <div style="position: absolute; left: 0; right: 0; top: 70px; bottom: 120px; border-left: 4px solid #1b1b1b; border-bottom: 4px solid #1b1b1b"></div>
      <div id="b1" class="bar" style="left: 60px; height: 260px"></div>
      <div id="b1v" class="bval mono" style="left: 40px; bottom: 395px">10,000</div>
      <div class="bcap mono" style="left: 40px">1ST CALL</div>
      <div id="b3" class="bar" style="left: 330px; height: 572px; background: #c8372d"></div>
      <div id="b3v" class="bval mono" style="left: 300px; bottom: 712px; color: #c8372d; background: #ece6da">22,000</div>
      <div class="bcap mono" style="left: 310px">LATER CALL</div>
    </div>
    <svg id="gauge" viewBox="0 0 250 250">
      <circle cx="125" cy="125" r="112" fill="#f8f5ee" stroke="#1b1b1b" stroke-width="8" />
      <path d="M125 125 L 212 72 A100 100 0 0 1 222 150 Z" fill="#c8372d" opacity="0.85" />
      <line id="needle" x1="125" y1="125" x2="125" y2="35" stroke="#1b1b1b" stroke-width="9" stroke-linecap="round" />
      <circle cx="125" cy="125" r="12" fill="#1b1b1b" />
    </svg>
    <div id="gauge-label" class="card mono" style="left: 1560px; top: 610px; font-size: 36px; padding: 14px 22px; text-align: center">OVERSPEED<br/>AT 20,000 FT</div>
""", f"""
    // A10 jolt + MAYDAY slams
    tl.fromTo("#mayday", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "power4.in" }}, {c('may', 1, -0.12)});
    tl.fromTo("#root", {{ x: 14, y: -10 }}, {{ x: 0, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {c('may', 1, 0.04)});
    tl.fromTo("#jetfront", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {c('may', 1, 0.3)});
    tl.fromTo("#chart", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {c('crew', 1, -0.2)});
    // A11 bar 1
    tl.fromTo("#b1", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.9, ease: "power3.out" }}, {c('10,000')});
    tl.fromTo("#b1v", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('10,000', 1, 0.6)});
    // A12 overspeed: airspeed needle swings into the red
    tl.fromTo(["#gauge", "#gauge-label"], {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {c('over', 1, -0.2)});
    tl.fromTo("#needle", {{ rotation: -40, svgOrigin: "125 125" }}, {{ rotation: 78, svgOrigin: "125 125", duration: 1.0, ease: "power2.inOut" }}, {c('over')});
    // A13 bar 3 punches past the top of the chart
    tl.fromTo("#b3", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.7, ease: "power4.out" }}, {c('22,000')});
    tl.fromTo("#b3v", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('22,000', 1, 0.5)});
    // A14 60-degree roll + protractor
    tl.fromTo("#jet-roll", {{ rotation: 0, svgOrigin: "290 150" }}, {{ rotation: -60, svgOrigin: "290 150", duration: 1.0, ease: "power2.inOut" }}, {c('60', 1, -0.15)});
    draw("#protractor", {c('60', 1, 0.1)}, 0.7, "power2.out");
    tl.fromTo("#bank-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('degree')});
""")

# ---------------------------------------------------------------- S5 ground
r = 'r5'; D = T[r]['scene_dur']; c = lambda w, n=1, o=0.0: cue(r, w, n, o)
icons5 = nine('g', 72)
files['ground'] = scene('ground', D, """
    #streets { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    #icons { position: absolute; left: 120px; top: 760px; display: flex; gap: 14px; align-items: flex-end; }
    #place { left: 120px; top: 90px; width: 760px; }
    #hurt { position: absolute; left: 1330px; top: 600px; white-space: nowrap; }
""", f"""
    <div class="paper"></div>
    <div id="streetcam" style="position: absolute; inset: 0">
      <svg id="streets" viewBox="0 0 1920 1080">
        <g stroke="#cfc6b6" stroke-width="18" fill="none">
          <path d="M0 230 H1920" /><path d="M0 820 H1920" /><path d="M520 0 V1080" /><path d="M1700 0 V1080" />
        </g>
        <path d="M1110 0 V1080" stroke="#8f877a" stroke-width="54" />
        <path d="M0 520 H1920" stroke="#a69d8f" stroke-width="34" />
        <text x="1142" y="600" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#55504a" transform="rotate(90 1142 600)">MILITARY TRAIL</text>
        <text x="40" y="490" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#55504a">10TH AVE N</text>
        <g transform="translate(1110 470)"><g id="pin">
          <path d="M0 0 C-34 -48 -46 -66 -46 -88 A46 46 0 1 1 46 -88 C46 -66 34 -48 0 0 Z" fill="#c8372d" />
          <circle cx="0" cy="-90" r="17" fill="#f8f5ee" />
        </g></g>
        <g id="hurt-dot"><circle cx="1290" cy="560" r="30" fill="#ffd84a" opacity="0.65" /><circle cx="1290" cy="560" r="12" fill="#1b1b1b" /></g>
      </svg>
    </div>
    <div id="place" class="card">
      <div class="disp" style="font-size: 52px">PALM BEACH COUNTY, FLA.</div>
      <div class="lbl" style="margin-top: 10px">GREENACRES AREA · SCHEMATIC, NOT TO SCALE</div>
    </div>
    <div id="icons">{icons5}</div>
    <div id="hurt" class="card mono" style="font-size: 36px; padding: 14px 22px">1 HURT ON THE GROUND</div>
""", f"""
    tl.set("#streetcam", {{ transformOrigin: "1110px 470px" }}, 0);
    inCard("#place", 0.3);
    // A15 slow push-in, pin drops (no crash animation)
    tl.fromTo("#streetcam", {{ scale: 1 }}, {{ scale: 1.12, duration: {D - 0.5:.2f}, ease: "sine.inOut" }}, 0);
    tl.fromTo("#pin", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, ease: "power3.out" }}, {c('nose', 1, -0.1)});
    // A16 the nine fade to grey, one at a time; then about a second of silence
    tl.fromTo("#icons", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.out" }}, {c('all', 1, -0.6)});
    tl.to("#icons .pp path, #icons .pp circle", {{ fill: "#b7afa2", duration: 0.5, ease: "power1.inOut", stagger: 0.09 }}, {c('all')});
    // A17 one soft highlight off the pin
    tl.fromTo("#hurt-dot", {{ opacity: 0, scale: 0.6, transformOrigin: "1290px 560px" }}, {{ opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }}, {c('remarkably', 1, 0.6)});
    inCard("#hurt", {c('person', 1, 0.0)});
""")

# ---------------------------------------------------------------- S6 envelope + tail
r = 'r6'; D = T[r]['scene_dur']; c = lambda w, n=1, o=0.0: cue(r, w, n, o)
files['envelope'] = scene('envelope', D, """
    #env { position: absolute; left: 160px; top: 90px; width: 1600px; height: 820px; }
    #q { position: absolute; left: 160px; top: 80px; font-size: 64px; }
    #tail { position: absolute; left: 140px; top: 120px; width: 1000px; height: 700px; }
    #side { position: absolute; left: 1220px; top: 300px; width: 560px; height: 300px; }
    #tail-cap { position: absolute; left: 180px; top: 70px; }
""", f"""
    <div class="paper"></div>
    <div id="q" class="disp">HOW DOES A JET FALL LIKE THAT?</div>
    <svg id="env" viewBox="0 0 1600 820">
      <line x1="120" y1="740" x2="1560" y2="740" stroke="#1b1b1b" stroke-width="5" />
      <line x1="120" y1="740" x2="120" y2="140" stroke="#1b1b1b" stroke-width="5" />
      <text x="1560" y="796" text-anchor="end" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#55504a">SPEED →</text>
      <text x="70" y="620" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#55504a" transform="rotate(-90 70 620)">ALTITUDE →</text>
      <path id="corridor" d="M300 740 C520 520 700 330 830 200 L870 200 C1000 330 1180 520 1420 740 Z" fill="#ffd84a" opacity="0.45" />
      <path id="stall" pathLength="1" d="M300 740 C520 520 700 330 830 200" fill="none" stroke="#2e64a8" stroke-width="10" stroke-linecap="round" />
      <path id="over" pathLength="1" d="M1420 740 C1180 520 1000 330 870 200" fill="none" stroke="#c8372d" stroke-width="10" stroke-linecap="round" />
      <text id="t-stall" x="150" y="470" font-family="Inter" font-weight="800" font-size="40" fill="#2e64a8">too slow (stall)</text>
      <text id="t-over" x="1165" y="470" font-family="Inter" font-weight="800" font-size="40" fill="#c8372d">too fast (overspeed)</text>
      <text id="t-narrow" x="850" y="170" text-anchor="middle" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#1b1b1b">HIGH UP: A NARROW GAP</text>
      <circle id="dot" cx="850" cy="250" r="16" fill="#1b1b1b" />
    </svg>
    <div id="tail-cap" class="lbl">LEARJET 60 TAIL · FROM ABOVE</div>
    <svg id="tail" viewBox="0 0 1000 700">
      <path d="M470 700 L470 300 C470 260 530 260 530 300 L530 700 Z" fill="#1b1b1b" />
      <path d="M500 330 L120 470 L130 520 L500 440 L870 520 L880 470 Z" fill="#3a3733" />
      <path id="elev-r" d="M560 452 L870 520 L866 560 L560 492 Z" fill="#6b655c" />
      <path id="elev-l" d="M440 452 L130 520 L134 560 L440 492 Z" fill="#6b655c" />
      <path id="elev-l-hl" pathLength="1" d="M440 452 L130 520 L134 560 L440 492 Z" fill="none" stroke="#ffd84a" stroke-width="14" stroke-linejoin="round" />
      <path id="elev-ghost" d="M440 452 L130 520 L134 560 L440 492 Z" fill="none" stroke="#1b1b1b" stroke-width="5" stroke-dasharray="14 10" />
      <text id="elev-label" x="140" y="630" font-family="Inter" font-weight="800" font-size="44" fill="#1b1b1b">left elevator</text>
      <text id="elev-q" x="60" y="420" font-family="Archivo Black" font-size="90" fill="#c8372d">?</text>
    </svg>
    <svg id="side" viewBox="0 0 560 300">
      <g id="side-jet">
        <path d="M30 150 C60 130 160 126 400 128 C460 128 510 136 530 146 C510 156 460 164 400 164 L160 164 C90 164 50 160 30 150 Z" fill="#1b1b1b" />
        <path d="M70 136 L44 70 L76 70 L120 134 Z" fill="#1b1b1b" />
        <path id="side-elev" d="M36 74 L96 72 L94 82 L36 84 Z" fill="#ffd84a" stroke="#1b1b1b" stroke-width="3" />
      </g>
    </svg>
""", f"""
    inCard("#q", 0.3);
    tl.fromTo("#env", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {c('at', 1, -0.3)});
    // A18 two lines: stall and overspeed
    draw("#stall", {c('gap')}, 1.2);
    draw("#over", {c('gap', 1, 0.2)}, 1.2);
    tl.fromTo(["#t-stall", "#t-over"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, stagger: 0.3 }}, {c('slow')});
    // A19 corridor narrows toward the top
    tl.fromTo("#corridor", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 1.4, ease: "power2.inOut" }}, {c('very', 1, -0.4)});
    tl.fromTo("#t-narrow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {c('narrow')});
    // A20 the dot gets pushed toward both edges
    tl.fromTo("#dot", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('ice', 1, -0.2)});
    tl.to("#dot", {{ keyframes: [{{ x: -34, duration: 0.35 }}, {{ x: 30, duration: 0.4 }}, {{ x: -40, duration: 0.4 }}, {{ x: 38, duration: 0.4 }}, {{ x: -18, duration: 0.35 }}, {{ x: 0, duration: 0.3 }}], ease: "sine.inOut" }}, {c('ice')});
    // to the tail
    tl.to(["#env", "#q"], {{ opacity: 0, x: -120, filter: "blur(6px)", duration: 0.6, ease: "power2.in" }}, {c('investigators', 1, -0.2)});
    // A21 tail cutaway rotates in, left elevator outlined
    tl.fromTo(["#tail", "#tail-cap"], {{ opacity: 0, rotation: -12, scale: 0.9 }}, {{ opacity: 1, rotation: 0, scale: 1, duration: 1.1, ease: "expo.out" }}, {c('evidence', 1, -0.3)});
    draw("#elev-l-hl", {c('left')}, 0.8, "power2.out");
    tl.fromTo("#elev-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('elevator')});
    // A22 the elevator pitches the nose; then a dashed outline drifts away with "?"
    tl.fromTo("#side", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }}, {c('surface', 1, -0.3)});
    tl.to("#side-jet", {{ keyframes: [{{ rotation: -8, duration: 0.6 }}, {{ rotation: 7, duration: 0.8 }}, {{ rotation: 0, duration: 0.6 }}], svgOrigin: "280 146", ease: "sine.inOut" }}, {c('pitches')});
    tl.set("#elev-ghost", {{ opacity: 0 }}, 0);
    tl.set("#elev-q", {{ opacity: 0 }}, 0);
    tl.to("#elev-ghost", {{ opacity: 1, duration: 0.2 }}, {c('may', 1, 0.0)});
    tl.to("#elev-ghost", {{ x: -150, y: 90, rotation: -14, svgOrigin: "290 500", duration: 1.6, ease: "power2.inOut" }}, {c('may', 1, 0.2)});
    tl.to("#elev-l", {{ opacity: 0.25, duration: 0.8 }}, {c('separated')});
    tl.to("#elev-q", {{ opacity: 1, x: -110, y: 90, duration: 1.0, ease: "power2.out" }}, {c('separated', 1, 0.2)});
""")

# ---------------------------------------------------------------- S7 NTSB
r = 'r7'; D = T[r]['scene_dur']; c = lambda w, n=1, o=0.0: cue(r, w, n, o)
icons7 = nine('n', 60)
files['ntsb'] = scene('ntsb', D, """
    #ntsb { position: absolute; left: 140px; top: 110px; font-size: 120px; }
    #ntsb-sub { position: absolute; left: 146px; top: 240px; }
    #cvr { position: absolute; left: 160px; top: 340px; width: 520px; height: 380px; }
    #cal { left: 820px; top: 150px; width: 460px; padding: 0; overflow: hidden; }
    #timeline { position: absolute; left: 1340px; top: 360px; width: 2000px; height: 160px; }
    #icons { position: absolute; left: 820px; top: 680px; display: flex; gap: 12px; align-items: flex-end; }
    #black { position: absolute; inset: 0; background: #0d0d0d; z-index: 30; }
    #credits { position: absolute; left: 0; right: 0; top: 470px; text-align: center; color: #cfc9be; font-size: 30px; line-height: 1.5; z-index: 31; }
""", f"""
    <div class="paper"></div>
    <div id="ntsb" class="disp">NTSB</div>
    <div id="ntsb-sub" class="lbl">CASE ERA27MA026</div>
    <svg id="cvr" viewBox="0 0 520 380">
      <rect x="60" y="80" width="380" height="240" rx="18" fill="#e8641c" />
      <rect x="60" y="80" width="380" height="240" rx="18" fill="none" stroke="#1b1b1b" stroke-width="6" />
      <g stroke="#1b1b1b" stroke-width="10"><line x1="90" y1="120" x2="410" y2="120" /><line x1="90" y1="280" x2="410" y2="280" /></g>
      <text x="250" y="190" text-anchor="middle" font-family="Archivo Black" font-size="34" fill="#1b1b1b">COCKPIT VOICE</text>
      <text x="250" y="232" text-anchor="middle" font-family="Archivo Black" font-size="34" fill="#1b1b1b">RECORDER</text>
      <g id="check"><circle cx="440" cy="90" r="58" fill="#1f8a4c" /><path id="check-path" pathLength="1" d="M412 92 L434 114 L472 70" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" /></g>
    </svg>
    <div id="cal" class="card">
      <div style="background: #c8372d; color: #fff; text-align: center; padding: 14px 0 8px; font-size: 64px" class="disp"><span id="cal-m1">NOVEMBER</span></div>
      <div id="cal-m2" style="position: absolute; left: 0; right: 0; top: 0; background: #1b1b1b; color: #fff; text-align: center; padding: 14px 0 8px; font-size: 64px" class="disp">DECEMBER</div>
      <div class="lbl" style="text-align: center; padding: 26px 0 30px; font-size: 38px; color: #1b1b1b">PRELIMINARY REPORT</div>
      <svg style="position: absolute; left: 30px; top: -10px; width: 400px; height: 120px; overflow: visible" viewBox="0 0 400 120">
        <path id="cal-circle" pathLength="1" d="M200 14 C340 10 396 40 390 64 C380 102 260 112 170 108 C60 104 4 90 10 60 C16 30 90 12 230 16" fill="none" stroke="#ffd84a" stroke-width="10" stroke-linecap="round" />
      </svg>
    </div>
    <svg id="timeline" viewBox="0 0 2000 160">
      <path id="tl-line" pathLength="1" d="M0 80 H2000" stroke="#1b1b1b" stroke-width="8" />
      <circle cx="0" cy="80" r="16" fill="#1b1b1b" />
      <text x="0" y="40" font-family="JetBrains Mono" font-weight="600" font-size="32" fill="#55504a">NOW</text>
      <text id="tl-year" x="300" y="140" font-family="JetBrains Mono" font-weight="600" font-size="34" fill="#1b1b1b">FULL ANSWER: A YEAR OR MORE →</text>
    </svg>
    <div id="icons">{icons7}</div>
    <div id="black"></div>
    <div id="credits">Sources: NTSB (ERA27MA026), GlobalAir, CBS12/WSET, AIN, AvWeb · reporting as of mid-November 2026<br/>Music: HeyGen · SFX: InspectorJ (Freesound, CC BY) · Voice: Kokoro</div>
""", f"""
    inCard(["#ntsb", "#ntsb-sub"], 0.2);
    // A23 recorder drops in with a check
    tl.fromTo("#cvr", {{ y: -260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }}, {c('recovered', 1, -0.5)});
    tl.fromTo("#check", {{ opacity: 0, scale: 0.4, transformOrigin: "440px 90px" }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, {c('recorder')});
    draw("#check-path", {c('recorder', 1, 0.15)}, 0.35, "power2.out");
    // A24 calendar flips to December and gets circled
    inCard("#cal", {c('its', 1, -0.2)});
    tl.fromTo("#cal-m2", {{ rotationX: -90, transformOrigin: "50% 0%", opacity: 0 }}, {{ rotationX: 0, opacity: 1, duration: 0.7, ease: "power3.out" }}, {c('preliminary', 1, 0.3)});
    draw("#cal-circle", {c('weeks', 1, -0.4)}, 0.7, "power2.out");
    // A25 a timeline stretches off-screen; the nine return; fade to black
    draw("#tl-line", {c('full', 1, -0.2)}, 2.6, "power2.inOut");
    tl.fromTo("#tl-year", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {c('year', 1, -0.4)});
    tl.fromTo("#icons", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.2, ease: "power1.inOut" }}, {c('likely')});
    tl.set("#icons .pp path, #icons .pp circle", {{ fill: "#b7afa2" }}, 0);
    tl.fromTo("#black", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.8, ease: "power1.inOut" }}, {c('more', 1, 0.8)});
    tl.fromTo("#credits", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8 }}, {c('more', 1, 2.0)});
""")

for k, v in files.items():
    open(f'compositions/{k}.html', 'w').write(v)
print('wrote', ', '.join(files))
