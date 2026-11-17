"""Generates compositions/captions.html and the audio section of index.html from script/timing.json."""
import json, re
T = json.load(open('script/timing.json'))
FIX = {'ships': 'chips', "NVIDIA's": "Nvidia's", 'NVIDIA': 'Nvidia', 'Officials': 'officials', 'Hwang': 'Huang', 'stuck,': 'stuck:', 'wrote,': 'wrote.', 'compromised,': 'compromised.', 'it,': 'it.'}
END = 102.0

# ---- caption groups -------------------------------------------------------
groups = []
for s in T:
    sent = []
    for w in s['words']:
        txt = FIX.get(w['text'], w['text'])
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
    text = {'I was unfaithful to': '“I was unfaithful to', 'my wife,': 'my wife,”', 'there is no excuse': '“There is no excuse', 'for what I did.': 'for what I did.”',
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
# camera moves
for t, d in [(4.7, 1.7), (17.6, 1.6), (20.6, 1.7), (26.0, 1.8), (41.9, 1.6), (44.3, 1.5), (53.0, 1.5), (57.1, 1.6), (66.3, 1.6), (76.4, 1.9), (89.2, 1.9)]:
    add('whoosh', t + d * 0.5, 0.22)
for t in [9.25, 14.3, 19.4, 21.6, 27.8, 31.0, 37.0, 38.1, 40.2, 45.3, 53.9, 59.1, 60.3, 62.3, 67.2, 77.4, 82.6, 86.1]:
    add('tack', t + 0.05, 0.28)
for t in [48.8, 51.3]:
    add('type', t, 0.25)
for t in [34.6, 69.4]:
    add('stamp', t + 0.2, 0.5)
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
voices = [f'      <audio id="vo-{s["id"]}" class="clip" src="assets/voice/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="10" data-volume="1"></audio>' for s in T]
idx = open('index.html').read()
music = [
    '      <audio id="music-act1" class="clip" src="assets/music/act1-explainer.mp3" data-start="0" data-duration="26.6" data-media-start="4.0" data-track-index="11" data-volume="0.13" data-fade-in="0.6" data-fade-out="1.4"></audio>',
    '      <audio id="music-act2" class="clip" src="assets/music/act2-tension.mp3" data-start="26.0" data-duration="71.4" data-media-start="0.6" data-track-index="12" data-volume="0.13" data-fade-in="1.0" data-fade-out="3.0"></audio>',
]
block = '\n'.join(['      <!-- AUDIO:BEGIN (generated by script/build.py) -->'] + voices + music + lines + ['      <!-- AUDIO:END -->'])
idx = re.sub(r'      <!-- AUDIO:BEGIN.*?AUDIO:END -->', lambda m: block, idx, flags=re.S)
open('index.html', 'w').write(idx)
print(len(caps), 'captions,', len(fx), 'effects')
