"""Builds film/project.json for the Olof Palme B4 demo (first 25.5 s, shots 0-9)."""
import json, pathlib
F = pathlib.Path('/home/user/Vox-murder-mystery/olof-palme/film')
proj = json.loads((F / 'project.json').read_text())
opening = json.loads((F / 'opening-layers.json').read_text())
AUTHOR = 'claude-code-demo-author'
import math
def rot_keys(world, local, segs, step=0.04):
    """Dense x/y/angle keys rotating a top-left-pivoted image around `local` (layer-box coords) placed at `world`.
    segs: [(t, angle)] anchors; angle interpolated linearly with smoothstep easing per segment."""
    out = []
    for (t0, a0), (t1, a1) in zip(segs, segs[1:]):
        n = max(1, round((t1 - t0) / step))
        for k in range(n + (1 if (t1, a1) == segs[-1] else 0)):
            u = k / n; e = u * u * (3 - 2 * u); a = a0 + (a1 - a0) * e; t = t0 + (t1 - t0) * u
            c, s_ = math.cos(a), math.sin(a)
            out.append({'t': round(t, 4), 'x': round(world[0] - (c * local[0] - s_ * local[1]), 3),
                        'y': round(world[1] - (s_ * local[0] + c * local[1]), 3), 'angle': round(a, 5)})
    return out

def img(i, p, **kw): return {'id': i, 'type': 'image', 'path': f'art/{p}', 'x': 0, 'y': 0, 'w': 1280, 'h': 720, **kw}
def reveal(i, p, t0, t1): return img(i, p, **{'from': t0, 'keys': [{'t': t0, 'alpha': 0}, {'t': t1, 'alpha': 1}]})

shots = [opening['shot']]
pm = [{'shot': 0, 'kind': 'state_reveal', 'intent': 'Hook: the gunman appears in the doorway behind the couple',
       'before': 'Empty lit doorway behind Olof and Lisbet', 'after': 'A dark capped figure stands in the doorway, shadow reaching toward them',
       'layer_ids': ['hook-before', 'hook-after'], 'region': opening['opening']['picture']['region'],
       'times': {'before': 0.9, 'mid': 1.2, 'after': 1.4, 'hold': 1.9}}]

def add(start, end, layers, kind, intent, before, after, ids, region, times, **extra):
    shots.append({'start': start, 'end': end, 'layers': layers})
    pm.append({'shot': len(shots) - 1, 'kind': kind, 'intent': intent, 'before': before, 'after': after,
               'layer_ids': ids, 'region': region, 'times': times, **extra})

# 1 cinema exterior 3.0-5.9: doors open, couple steps out
add(3.0, 5.9, [img('s1-before', 's01-before.png'), reveal('s1-after', 's01-after.png', 1.0, 1.4)],
    'state_reveal', 'Olof and Lisbet leave the cinema', 'Cinema doors closed under the marquee', 'Centre door open, the couple steps out into the snow',
    ['s1-before', 's1-after'], {'x': 560, 'y': 320, 'w': 240, 'h': 250}, {'before': 3.7, 'mid': 4.2, 'after': 4.45, 'hold': 5.0})
# 2 walking 5.9-8.7: bodyguards vanish, then the car
add(5.9, 8.7, [img('s2-before', 's02-before.png'), reveal('s2-mid', 's02-mid.png', 1.0, 1.4), {'id': 's2-after', 'type': 'image', 'path': 'art/s02-car-gone.png', 'x': 800, 'y': 390, 'w': 280, 'h': 110, 'from': 2.0, 'keys': [{'t': 2.0, 'alpha': 0}, {'t': 2.4, 'alpha': 1}]}],
    'state_reveal', 'No bodyguards, no car: the protection that should be there disappears', 'Ghost outlines of two bodyguards and an official car around the couple',
    'Only the couple remain on the empty snowy pavement', ['s2-before', 's2-mid'], {'x': 260, 'y': 400, 'w': 510, 'h': 260},
    {'before': 6.8, 'mid': 7.1, 'after': 7.35, 'hold': 7.7})
# 3 prime minister 8.7-11.0: Swedish flag unfurls behind Palme
add(8.7, 11.0, [img('s3-before', 's03-before.png'), reveal('s3-after', 's03-after.png', 0.6, 1.0)],
    'environment', 'He is the Prime Minister of Sweden', 'Furled flag on the government building behind Palme', 'Swedish flag unfurled above the building',
    ['s3-before', 's3-after'], {'x': 940, 'y': 15, 'w': 140, 'h': 145}, {'before': 9.2, 'mid': 9.5, 'after': 9.75, 'hold': 10.2})
# 4 morning door 11.0-14.0: bodyguards walk away
add(11.0, 14.0, [img('s4-bg', 's04-bg.png'),
                 {'id': 's4-guards', 'type': 'image', 'path': 'art/s04-guards.png', 'x': 600, 'y': 182, 'w': 520,
                  'keys': [{'t': 0, 'x': 600, 'alpha': 1}, {'t': 1.3, 'x': 600, 'alpha': 1}, {'t': 2.5, 'x': 600, 'alpha': 0}]}],
    'local_action', 'Palme waves his security detail home', 'Two bodyguards stand beside Palme at his front door', 'The bodyguards have walked off; Palme is alone at the door',
    ['s4-guards'], {'x': 560, 'y': 160, 'w': 720, 'h': 460}, {'before': 12.3, 'mid': 12.9, 'after': 13.5, 'hold': 13.8})
# 5 cinema interior 14.0-16.4: screen lights up, faces lit
add(14.0, 16.4, [img('s5-before', 's05-before.png'), reveal('s5-after', 's05-after.png', 0.8, 1.2)],
    'environment', 'One normal Friday night at the movies', 'Dark cinema screen, couple in shadow', 'Film playing, couple lit and smiling',
    ['s5-before', 's5-after'], {'x': 200, 'y': 40, 'w': 880, 'h': 640}, {'before': 14.5, 'mid': 15.0, 'after': 15.25, 'hold': 15.7})
# 6 street clock 16.4-19.4: minute hand ticks to 11:21
A19, A20, A21 = 19 / 60 * 6.283185, 20 / 60 * 6.283185, 21 / 60 * 6.283185
add(16.4, 19.4, [img('s6-bg', 's06-bg.png'),
                 {'id': 's6-minute', 'type': 'image', 'path': 'art/s06-minute.png', 'w': 400,
                  'keys': rot_keys((660, 300), (200, 200), [(0, A19), (0.3, A19), (1.15, A21)])}],
    'local_action', 'The street clock ticks to 11:21 p.m.', 'Clock reads 11:19', 'Clock reads 11:21',
    ['s6-minute'], {'x': 480, 'y': 120, 'w': 360, 'h': 360}, {'before': 16.7, 'mid': 17.1, 'after': 17.55, 'hold': 18.0})
# 7 Tunnelgatan corner 19.4-21.8: gunman steps out of the dark behind them
add(19.4, 21.8, [img('s7-bg', 's07-bg.png'),
                 {'id': 's7-gunman', 'type': 'image', 'path': 'art/s07-gunman.png', 'x': 200, 'y': 190, 'w': 260,
                  'keys': [{'t': 0, 'x': 508, 'alpha': 0}, {'t': 0.2, 'x': 508, 'alpha': 0}, {'t': 1.3, 'x': 520, 'alpha': 1}]}],
    'local_action', 'A man steps out of the dark behind Palme', 'Dark passage behind the couple is empty', 'A capped gunman stands in the open behind them',
    ['s7-gunman'], {'x': 450, 'y': 190, 'w': 340, 'h': 430}, {'before': 19.55, 'mid': 20.2, 'after': 20.75, 'hold': 21.2})
# 8 over the shoulder 21.8-24.0: arm raises, one shot
add(21.8, 24.0, [img('s8-bg', 's08-bg.png'),
                 {'id': 's8-arm', 'type': 'image', 'path': 'art/s08-arm.png', 'w': 380,
                  'keys': rot_keys((230, 520), (25.33, 63.33), [(0, 0.55), (0.05, 0.55), (0.55, -0.17)])},
                 {'id': 's8-flash', 'type': 'image', 'path': 'art/s08-flash.png', 'x': 503, 'y': 397, 'w': 110, 'from': 0.58,
                  'keys': [{'t': 0.58, 'alpha': 0}, {'t': 0.61, 'alpha': 1}, {'t': 0.78, 'alpha': 0}]},
                 {'id': 's8-smoke', 'type': 'image', 'path': 'art/s08-smoke.png', 'x': 520, 'y': 360, 'w': 170, 'from': 0.6,
                  'keys': [{'t': 0.6, 'alpha': 0, 'y': 372}, {'t': 0.95, 'alpha': 0.9, 'y': 356}, {'t': 2.15, 'alpha': 0.25, 'y': 320}]}],
    'local_action', 'The gunman raises a revolver to Palme\'s back and fires', 'Gloved hand hangs low by the gunman\'s side', 'Revolver aimed at Palme\'s back, muzzle flash',
    ['s8-arm', 's8-smoke'], {'x': 200, 'y': 300, 'w': 500, 'h': 420}, {'before': 21.83, 'mid': 22.2, 'after': 22.75, 'hold': 23.1})
# 9 fall 24.0-25.5: Palme falls, Lisbet turns in shock
add(24.0, 25.5, [img('s9-before', 's09-bg-before.png'), reveal('s9-after', 's09-bg-after.png', 0.45, 0.75),
                 {'id': 's9-palme', 'type': 'image', 'path': 'art/s09-palme.png', 'w': 400,
                  'keys': rot_keys((600, 590), (200, 390), [(0, 0), (0.1, 0), (0.7, -1.45)])}],
    'local_action', 'Palme collapses into the snow as Lisbet turns', 'Palme upright beside Lisbet', 'Palme lies in the snow; Lisbet recoils in shock',
    ['s9-before', 's9-after', 's9-palme'], {'x': 330, 'y': 200, 'w': 700, 'h': 450}, {'before': 24.08, 'mid': 24.4, 'after': 24.75, 'hold': 25.1})

# semantic captions (regrouped by meaning against the actual word times)
caps = [(0.0, 2.54, 'February 28th, 1986.'), (2.87, 3.68, 'Stockholm.'), (3.96, 5.69, 'A man walks home from the cinema'),
        (5.74, 6.51, 'with his wife.'), (6.90, 7.78, 'No bodyguards.'), (7.84, 8.57, 'No car.'), (8.89, 10.75, 'He is the Prime Minister of Sweden.'),
        (10.99, 12.46, 'That morning, Olof Palme'), (12.50, 14.21, 'sent his security detail home.'), (14.59, 16.22, 'He wanted one normal Friday night.'),
        (16.54, 18.11, 'At 11:21 p.m.,'), (18.23, 19.31, 'on Sveavägen,'), (19.55, 21.47, 'a man steps out of the dark behind him.'),
        (21.79, 22.59, 'One shot.'), (22.87, 23.66, 'In the back.'), (23.91, 25.20, 'At point-blank range.')]
proj.update({
    'voice': {'path': 'narration.wav', 'lead': 0, 'tail': 0, 'name': 'Brian', 'id': 'nPczCjzI2devNBz1zQrb'},
    'captions': [{'start': a, 'end': b, 'text': t} for a, b, t in caps],
    'shots': shots,
    'picture_motion': {'author_id': AUTHOR, 'shots': pm},
    'opening': opening['opening'],
    'typography': {'author_id': AUTHOR},
    'music': {'path': 'audio/music-decisions.mp3', 'gain': 0.07},
    'ambience': [{'path': 'audio/sfx/amb-night-street.ogg', 'start': 0, 'end': 14.0, 'gain': 0.06, 'fadeOut': 0.3},
                 {'path': 'audio/sfx/amb-night-street.ogg', 'start': 16.4, 'end': 25.5, 'gain': 0.06, 'offset': 8, 'fadeIn': 0.3}],
    'audio_cuts': [{'start': 14.0, 'end': 16.4, 'reason': 'Inside the cinema the street bed drops away; only narration and the film score carry the warm interior',
                    'return_trigger': 'Cut to the street clock at 16.4 s restores the night street bed'}],
    'sfx': ([{'kind': 'file', 'path': f'audio/sfx/footstep_snow_00{i % 4}.ogg', 'time': round(4.5 + i * 0.45, 2), 'gain': 0.22} for i in range(9)]
            + [{'kind': 'file', 'path': 'audio/sfx/door.ogg', 'time': 3.95, 'gain': 0.35},
               {'kind': 'file', 'path': 'audio/sfx/clock-tick.ogg', 'time': 16.85, 'gain': 0.45},
               {'kind': 'file', 'path': 'audio/sfx/clock-tick.ogg', 'time': 17.4, 'gain': 0.45},
               {'kind': 'file', 'path': 'audio/sfx/clock-tick.ogg', 'time': 17.95, 'gain': 0.45}]
            + [{'kind': 'file', 'path': f'audio/sfx/footstep_snow_00{i % 4}.ogg', 'time': round(19.7 + i * 0.32, 2), 'gain': 0.3} for i in range(4)]
            + [{'kind': 'file', 'path': 'audio/sfx/gunshot-synth.wav', 'time': 22.4, 'gain': 0.8},
               {'kind': 'file', 'path': 'audio/sfx/body-fall.ogg', 'time': 24.65, 'gain': 0.5}]),
})
proj['voice']['user_override'] = 'n/a: Brian (ElevenLabs nPczCjzI2devNBz1zQrb) is the B4 default and was used'
proj['voice'].pop('user_override')
(F / 'project.json').write_text(json.dumps(proj, indent=2, ensure_ascii=False))
print('shots', len(shots), 'captions', len(caps))
