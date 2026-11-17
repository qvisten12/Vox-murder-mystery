"""Generates compositions/captions.html and the audio section of index.html from script/timing.json."""
import json, re
T = json.load(open('script/timing.json'))
FIX = {'May': 'mayday.', 'Day.': '', 'over': 'overspeed', 'speed': '', 'NTSB': 'NTSB'}
END = 103.3
_T = {x['id']: x for x in T}

# ---- caption groups -------------------------------------------------------
groups = []
for s in T:
    sent = []
    for w in s['words']:
        txt = FIX.get(w['text'], w['text'])
        if not txt: continue
        sent.append((txt, s['start'] + w['s'], s['start'] + w['e']))
        if re.search(r'[.?!]$', txt):
            n = len(sent)
            # balanced split, nudged to break after a comma when one is close
            i = 0
            while i < n:
                rem = n - i; size = -(-rem // -(-rem // 6))
                j = min(n, i + size)
                for c in (j - 1, j, j - 2, j + 1):
                    if i + 2 <= c < n - 1 and c - i <= 6 and sent[c - 1][0].endswith(','):
                        j = c; break
                groups.append(sent[i:j]); i = j
            sent = []
    if sent: groups.append(sent)
out = groups
caps = []
for i, g in enumerate(out):
    start = g[0][1] - 0.05
    end = g[-1][2] + 0.15
    if i + 1 < len(out):
        end = min(end + 0.25, out[i + 1][0][1] - 0.07)
    text = ' '.join(x[0] for x in g).replace('Then the New York', 'Then The New York').replace('behind them,', 'behind them:')
    text = text.replace('little overspeed a', 'little over a').replace('but South', 'But South').replace('nose down', 'nose-down').replace('60 degree', '60-degree')
    text = {'XX to': '“I was unfaithful to', 'my wife,': 'my wife,”', 'there is no excuse': '“There is no excuse', 'for what I did.': 'for what I did.”',
            'but the threads kept pulling.': 'But the threads kept pulling.', 'and officials still haven\'t said whether': 'And officials still haven\'t said whether'}.get(text, text)
    caps.append((f'cap{i:02d}', text, round(start, 3), round(end, 3)))

html = ['<template>', '''  <style>
    #root { position: absolute; inset: 0; pointer-events: none; }
    .cap {
      position: absolute; left: 0; right: 0; bottom: 92px; text-align: center;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 54px; line-height: 1.1;
      color: #ffffff; -webkit-text-stroke: 12px #141210; paint-order: stroke fill;
      letter-spacing: 0.005em; overflow: visible;
    }
  </style>''', '  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">']
for cid, txt, a, b in caps:
    html.append(f'    <div id="{cid}" class="cap clip" data-start="{a}" data-duration="{round(b-a,3)}">{txt}</div>')
html.append('  </div>\n  <script>\n    const tl = gsap.timeline({ paused: true });\n    const caps = ' +
            json.dumps([[c[0], c[2], c[3]] for c in caps]) + ''';
    for (const [id, a, b] of caps) {
      tl.fromTo("#" + id, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, a);
      tl.to("#" + id, { opacity: 0, duration: 0.08, ease: "none" }, b - 0.08);
      tl.set("#" + id, { opacity: 0 }, b);
    }
    tl.to({}, { duration: 0.01 }, ''' + str(END - 0.1) + ''');
    window.__timelines["captions"] = tl;
  </script>
</template>''')
open('compositions/captions.html', 'w').write('\n'.join(html) + '\n')

# ---- sound effects (visual time, sound peak offset) -----------------------
PEAK = {'stamp': 0.086, 'tack': 0.011, 'pin': 0.373, 'whoosh': 0.491, 'shutter': 0.189, 'type': 0.033, 'paper': 0.30}
fx = []
def add(name, t, vol=0.5): fx.append((name, t, vol))
# effects: kept sparse and quiet for a respectful film
def at(sid, word, o=0.0):
    x = _T[sid]; w = [w for w in x['words'] if w['text'].lower().strip('.,?!:') == word][0]
    return x['start'] + w['s'] + o
add('type', at('r1', 'on', 0.0), 0.25)
add('whoosh', _T['r2']['scene_start'] + _T['r2']['scene_dur'] - 0.1, 0.18)
add('stamp', at('r4', 'may', -0.05), 0.45)
add('tack', at('r7', 'recorder'), 0.3)
fx.sort(key=lambda x: x[1])
lines = []
lane_end = {13: -1, 14: -1, 15: -1}
for i, (n, t, v) in enumerate(fx):
    ms = 2.6 if n == 'paper' else 0
    dur = {'paper': 1.2, 'whoosh': 1.2, 'stamp': 0.62, 'tack': 0.9, 'pin': 0.9, 'shutter': 0.34, 'type': 0.9}[n]
    st = max(0.0, round(t + 1 / 30 - PEAK[n], 3))
    extra = f' data-media-start="{ms}"' if ms else ''
    lane = next(l for l in (13, 14, 15) if lane_end[l] <= st); lane_end[lane] = st + dur
    lines.append(f'      <audio id="fx{i:02d}" class="clip" src="assets/sfx/{n}.mp3" data-start="{st}" data-duration="{dur}"{extra} data-track-index="{lane}" data-volume="{v}"></audio>')
voices0 = [f'      <audio id="vo-{s["id"]}" class="clip" src="assets/voice/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="10" data-volume="1"></audio>' for s in T]
voices = [v for v in voices0 if 'vo-r5' not in v]
r5 = _T['r5']
voices.append(f'      <audio id="vo-r5a" class="clip" src="assets/voice/r5a.wav" data-start="{r5["start"]}" data-duration="7.4" data-track-index="10" data-volume="1"></audio>')
voices.append(f'      <audio id="vo-r5b" class="clip" src="assets/voice/r5b.wav" data-start="{r5["start"] + 8.4:.3f}" data-duration="{r5["dur"] - 8.4:.3f}" data-track-index="10" data-volume="1"></audio>')
scenes = ''.join(f'      <div id="{h}" data-composition-id="{h}" data-composition-src="compositions/{h}.html" data-start="{x["scene_start"]}" data-duration="{x["scene_dur"] if h != "map" else round(_T["r2"]["scene_dur"] + _T["r3"]["scene_dur"], 3)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>\n'
                 for h, x in [('hook', _T['r1']), ('map', _T['r2']), ('mayday', _T['r4']), ('ground', _T['r5']), ('envelope', _T['r6']), ('ntsb', _T['r7'])])
idx = open('index.html').read()
idx = re.sub(r'      <!-- SCENES:BEGIN.*?SCENES:END -->', lambda m: '      <!-- SCENES:BEGIN (generated) -->\n' + scenes + '      <!-- SCENES:END -->', idx, flags=re.S)
import json as _j
_T = {x['id']: x for x in T}
MAYDAY = _T['r4']['start'] + [w for w in _T['r4']['words'] if w['text'] == 'May'][0]['s']
music = [
    f'      <audio id="music-act1" class="clip" src="assets/music/act1-investigative.mp3" data-start="0.2" data-duration="{MAYDAY - 0.2:.2f}" data-media-start="0.7" data-track-index="11" data-volume="0.12" data-fade-in="1.2" data-fade-out="0.25"></audio>',
    f'      <audio id="music-act2" class="clip" src="assets/music/act2-respectful.mp3" data-start="{_T["r6"]["scene_start"] + 0.3:.2f}" data-duration="{END - _T["r6"]["scene_start"] - 0.6:.2f}" data-media-start="0" data-track-index="12" data-volume="0.12" data-fade-in="2.0" data-fade-out="4.0"></audio>',
]
block = '\n'.join(['      <!-- AUDIO:BEGIN (generated by script/build.py) -->'] + voices + music + lines + ['      <!-- AUDIO:END -->'])
idx = re.sub(r'      <!-- AUDIO:BEGIN.*?AUDIO:END -->', lambda m: block, idx, flags=re.S)
open('index.html', 'w').write(idx)
print(len(caps), 'captions,', len(fx), 'effects')
