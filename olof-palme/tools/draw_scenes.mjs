// Code-drawn B4-inspired scene art for the Olof Palme demo (free route; no image model).
// All art is drawn on a 1280x720 design plane and exported at 1.5x (1920x1080).
// usage: node draw_scenes.mjs OUT_DIR
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire('/home/user/Vox-murder-mystery/.claude/skills/directing-stickman-videos/package.json');
const {createCanvas} = require('@napi-rs/canvas');

const OUT = process.argv[2];
fs.mkdirSync(OUT, {recursive: true});
const S = 1.5, W = 1280, H = 720, INK = '#17181d';

// ---------- deterministic randomness ----------
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

function canvas(w = W, h = H) {
  const c = createCanvas(Math.round(w * S), Math.round(h * S)); const ctx = c.getContext('2d');
  ctx.scale(S, S); ctx.lineJoin = 'round'; ctx.lineCap = 'round'; return [c, ctx];
}
function save(c, name) { fs.writeFileSync(path.join(OUT, name), c.toBuffer('image/png')); console.log('wrote', name); }

// ---------- primitives ----------
function shape(ctx, build, fill, lw = 3.2, stroke = INK) {
  ctx.beginPath(); build(ctx);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (lw) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
}
const rect = (x, y, w, h) => c => c.rect(x, y, w, h);
const poly = pts => c => { c.moveTo(...pts[0]); for (const p of pts.slice(1)) c.lineTo(...p); c.closePath(); };
const circ = (x, y, r) => c => c.arc(x, y, r, 0, Math.PI * 2);
const ell = (x, y, rx, ry, a = 0) => c => c.ellipse(x, y, rx, ry, a, 0, Math.PI * 2);
function line(ctx, pts, lw = 4, color = INK) {
  ctx.beginPath(); ctx.moveTo(...pts[0]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(...pts[i]);
  ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.stroke();
}
function vgrad(ctx, y0, y1, stops) { const g = ctx.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; }
function glow(ctx, x, y, r, color, a = 0.35) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, color.replace('A', a)); g.addColorStop(1, color.replace('A', 0));
  ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2);
}
function snowfall(ctx, seed, n = 140, x0 = 0, x1 = W, y0 = 0, y1 = H, alpha = 0.85) {
  const r = rng(seed); ctx.fillStyle = `rgba(240,246,255,${alpha})`;
  for (let i = 0; i < n; i++) { ctx.beginPath(); ctx.arc(x0 + r() * (x1 - x0), y0 + r() * (y1 - y0), 1 + r() * 2.2, 0, 7); ctx.fill(); }
}

// ---------- characters ----------
// Glove: compact rounded white cartoon glove with readable thumb.
function glove(ctx, x, y, s = 1, ang = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
  shape(ctx, ell(5 * s, -7 * s, 4 * s, 6 * s, -0.5), '#fbfbf7', 2.6);   // thumb
  shape(ctx, ell(0, 0, 9.5 * s, 8.5 * s), '#fbfbf7', 2.8);
  line(ctx, [[-3 * s, -6 * s], [-3 * s, -1 * s]], 1.6); line(ctx, [[1.5 * s, -6.5 * s], [1.5 * s, -1.5 * s]], 1.6);
  ctx.restore();
}
function head(ctx, x, y, r, o = {}) {
  const {hair = null, look = 0, eyes = 'dot', mouth = 'flat', shade = null} = o;
  if (hair === 'palme') { // thin swept-back hair with receding hairline
    shape(ctx, c => { c.moveTo(x - r * .95, y - r * .05); c.quadraticCurveTo(x - r * 1.05, y - r * .95, x - r * .1, y - r * 1.08); c.quadraticCurveTo(x + r * .55, y - r * 1.1, x + r * .62, y - r * .78); c.quadraticCurveTo(x - r * .1, y - r * .85, x - r * .55, y - r * .45); c.closePath(); }, '#8a7a68', 2.6);
  }
  if (hair === 'lisbet') {
    shape(ctx, c => { c.moveTo(x - r * 1.1, y + r * .35); c.quadraticCurveTo(x - r * 1.25, y - r * 1.15, x, y - r * 1.15); c.quadraticCurveTo(x + r * 1.25, y - r * 1.15, x + r * 1.1, y + r * .35); c.quadraticCurveTo(x + r * .9, y - r * .45, x, y - r * .6); c.quadraticCurveTo(x - r * .9, y - r * .45, x - r * 1.1, y + r * .35); }, '#7b4f33', 2.6);
  }
  shape(ctx, circ(x, y, r), '#fcfcf8', 3.2);
  if (shade) { ctx.save(); ctx.beginPath(); ctx.arc(x, y, r - 1.5, 0, 7); ctx.clip(); ctx.fillStyle = shade; ctx.fillRect(x - r, y - r * .2, r * 2, r * 2); ctx.restore(); }
  if (hair === 'palme') shape(ctx, c => { c.moveTo(x - r * .9, y - r * .35); c.quadraticCurveTo(x - r * .55, y - r * 1.02, x + r * .25, y - r * .98); c.quadraticCurveTo(x - r * .2, y - r * .78, x - r * .62, y - r * .25); c.closePath(); }, '#8a7a68', 2.2);
  if (hair === 'lisbet') shape(ctx, c => { c.moveTo(x - r * .95, y - r * .1); c.quadraticCurveTo(x - r * .6, y - r * 1.05, x + r * .4, y - r * .95); c.quadraticCurveTo(x - r * .1, y - r * .62, x - r * .7, y + r * .1); c.closePath(); }, '#7b4f33', 2.2);
  if (hair === 'cap') { // gunman's dark flat cap
    shape(ctx, c => { c.moveTo(x - r * 1.05, y - r * .25); c.quadraticCurveTo(x - r * .9, y - r * 1.2, x + r * .2, y - r * 1.1); c.quadraticCurveTo(x + r * 1.05, y - r * .95, x + r * 1.0, y - r * .35); c.closePath(); }, '#2b2a2c', 2.8);
    shape(ctx, c => { c.moveTo(x + r * .2, y - r * .38); c.quadraticCurveTo(x + r * 1.1, y - r * .52, x + r * 1.45, y - r * .3); c.quadraticCurveTo(x + r * .9, y - r * .18, x + r * .2, y - r * .25); c.closePath(); }, '#232224', 2.4);
  }
  const ex = x + look * r * .35, ey = y + r * .02, gap = r * .32;
  ctx.fillStyle = INK;
  if (eyes === 'dot') { for (const d of [-1, 1]) { ctx.beginPath(); ctx.ellipse(ex + d * gap, ey, r * .075, r * .12, 0, 0, 7); ctx.fill(); } }
  if (eyes === 'wide') { for (const d of [-1, 1]) { shape(ctx, circ(ex + d * gap, ey - r * .02, r * .17), '#fff', 2); ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(ex + d * gap, ey - r * .02, r * .07, 0, 7); ctx.fill(); } }
  if (eyes === 'calm') { for (const d of [-1, 1]) line(ctx, [[ex + d * gap - r * .1, ey + r * .02], [ex + d * gap, ey - r * .06], [ex + d * gap + r * .1, ey + r * .02]], 2.4); }
  if (eyes === 'shadow') { for (const d of [-1, 1]) { ctx.fillStyle = '#f2e6b8'; ctx.beginPath(); ctx.ellipse(ex + d * gap, ey, r * .07, r * .05, 0, 0, 7); ctx.fill(); } }
  const mx = x + look * r * .3, my = y + r * .42;
  if (mouth === 'flat') line(ctx, [[mx - r * .13, my], [mx + r * .13, my]], 2.4);
  if (mouth === 'smile') { ctx.beginPath(); ctx.arc(mx, my - r * .1, r * .17, .3, Math.PI - .3); ctx.strokeStyle = INK; ctx.lineWidth = 2.4; ctx.stroke(); }
  if (mouth === 'o') shape(ctx, ell(mx, my + r * .04, r * .1, r * .15), '#4a1e22', 2.2);
  if (mouth === 'frown') { ctx.beginPath(); ctx.arc(mx, my + r * .12, r * .15, Math.PI + .4, -.4); ctx.strokeStyle = INK; ctx.lineWidth = 2.4; ctx.stroke(); }
}
// Full figure. (x, y) = point between the feet on the ground. Coat drawn over the stick torso.
// arms: [[elbowDx, elbowDy, handDx, handDy], ...] relative to shoulder; legs: [kneeDx, footDx] pairs.
function figure(ctx, x, y, o = {}) {
  const s = o.s || 1, r = 25 * s, hip = [x, y - 74 * s], sh = [x, y - 138 * s], hd = [x + (o.headDx || 0) * s, y - 138 * s - r - 6 * s];
  const legs = o.legs || [[-6, -14], [6, 14]];
  const arms = o.arms || [[-12, 34, -16, 66], [12, 34, 16, 66]];
  // back arm & leg first
  const drawLeg = ([kx, fx]) => { const knee = [x + kx * s, y - 38 * s], foot = [x + fx * s, y - 3 * s]; line(ctx, [hip, knee, foot], 5 * s); shape(ctx, ell(foot[0] + (o.face || 1) * 5 * s, foot[1], 8 * s, 4.5 * s), INK, 0); };
  const drawArm = ([ex, ey, hx, hy], i) => { const el = [sh[0] + ex * s, sh[1] + ey * s], hand = [sh[0] + hx * s, sh[1] + hy * s]; line(ctx, [[sh[0] + (i ? 6 : -6) * s, sh[1] + 4 * s], el, hand], 5 * s); glove(ctx, hand[0], hand[1], s * 1.05, o.gloveAng?.[i] || 0); };
  drawLeg(legs[0]); if (!o.coat) drawArm(arms[0], 0);
  drawLeg(legs[1]);
  line(ctx, [sh, hip], 5.5 * s);
  if (o.coat) { // knee-length winter coat over the stick torso
    const [cf, cs] = o.coat, top = sh[1] - 4 * s, bot = y - 44 * s;
    shape(ctx, poly([[x - 17 * s, top], [x + 17 * s, top], [x + 25 * s, bot], [x - 25 * s, bot]]), cf, 3.2);
    shape(ctx, poly([[x + 3 * s, top + 2 * s], [x + 17 * s, top], [x + 25 * s, bot], [x + 6 * s, bot]]), cs, 0);
    line(ctx, [[x, top + 6 * s], [x, bot - 2 * s]], 2);
    shape(ctx, poly([[x - 17 * s, top], [x + 17 * s, top], [x + 25 * s, bot], [x - 25 * s, bot]]), null, 3.2);
    if (o.scarf) shape(ctx, c => { c.moveTo(x - 15 * s, top - 2 * s); c.lineTo(x + 15 * s, top - 2 * s); c.lineTo(x + 12 * s, top + 8 * s); c.lineTo(x - 12 * s, top + 8 * s); c.closePath(); }, o.scarf, 2.4);
    drawArm(arms[0], 0);
  }
  line(ctx, [[sh[0], sh[1]], [hd[0], hd[1] + r]], 5 * s);
  head(ctx, hd[0], hd[1], r, o.head || {});
  drawArm(arms[1], 1);
  return {head: hd, shoulder: sh, hip};
}

// ---------- shared environment pieces ----------
function nightSky(ctx, y1 = 420) { ctx.fillStyle = vgrad(ctx, 0, y1, [[0, '#18233b'], [1, '#33456a']]); ctx.fillRect(0, 0, W, y1); }
function building(ctx, x, y, w, h, base, shade, seed, lit = .5) {
  shape(ctx, rect(x, y, w, h), base, 3);
  shape(ctx, rect(x + w * .78, y, w * .22, h), shade, 0);
  shape(ctx, rect(x - 4, y - 10, w + 8, 12), shade, 2.6);
  const r = rng(seed), cols = Math.max(2, Math.floor(w / 46)), rows = Math.floor((h - 30) / 58);
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
    const wx = x + 14 + i * (w - 28) / cols, wy = y + 22 + j * 58;
    shape(ctx, rect(wx, wy, (w - 28) / cols - 14, 34), r() < lit ? '#f2c66d' : '#26324c', 2.2);
  }
  shape(ctx, rect(x, y, w, h), null, 3);
}
function snowGround(ctx, y0, y1 = H) {
  ctx.fillStyle = vgrad(ctx, y0, y1, [[0, '#9fb0cf'], [1, '#c9d6ec']]); ctx.fillRect(0, y0, W, y1 - y0);
  line(ctx, [[0, y0], [W, y0]], 3);
}
function lamp(ctx, x, top, ground, side = 1) {
  line(ctx, [[x, ground], [x, top]], 7, INK); line(ctx, [[x, ground], [x, top]], 3.5, '#4b5160');
  line(ctx, [[x, top], [x + 34 * side, top - 6]], 5);
  shape(ctx, poly([[x + 22 * side, top - 4], [x + 48 * side, top - 9], [x + 44 * side, top + 6], [x + 26 * side, top + 9]]), '#ffe7a3', 2.6);
  glow(ctx, x + 36 * side, top + 40, 120, 'rgba(255,214,140,A)', .22);
}
function volvo(ctx, x, y, color, shade) { // boxy 1980s sedan
  shape(ctx, poly([[x, y], [x + 230, y], [x + 236, y - 44], [x + 190, y - 50], [x + 165, y - 92], [x + 62, y - 92], [x + 40, y - 52], [x - 4, y - 46]]), color, 3.2);
  shape(ctx, poly([[x + 70, y - 84], [x + 112, y - 84], [x + 112, y - 54], [x + 52, y - 54]]), '#5e7192', 2.6);
  shape(ctx, poly([[x + 120, y - 84], [x + 160, y - 84], [x + 178, y - 54], [x + 120, y - 54]]), '#5e7192', 2.6);
  shape(ctx, rect(x - 4, y - 46, 240, 10), shade, 2.4);
  shape(ctx, poly([[x + 40, y - 92], [x + 170, y - 92], [x + 165, y - 98], [x + 62, y - 98]]), '#eef3fb', 2.2); // snow on roof
  for (const wx of [x + 48, x + 186]) { shape(ctx, circ(wx, y, 22), '#1e1f24', 3); shape(ctx, circ(wx, y, 9), '#8c919c', 2.2); }
}

// ---------- SHOT 0: opening, Sveavägen wide, figure emerges behind the couple ----------
function sveavagenWide(ctx, st) {
  nightSky(ctx, 470);
  building(ctx, -10, 40, 300, 440, '#3f4a66', '#323b54', 1, .55);
  building(ctx, 290, 110, 220, 370, '#56506b', '#463f59', 2, .45);
  building(ctx, 510, 70, 260, 410, '#3c5470', '#30455c', 3, .5);
  building(ctx, 770, 130, 230, 350, '#5a4a5e', '#4a3c4e', 4, .35);
  building(ctx, 1000, 60, 300, 420, '#40506a', '#344158', 5, .4);
  // dark recessed corner/doorway where the figure waits (right of couple)
  shape(ctx, rect(1040, 290, 140, 190), '#2b3654', 3);
  glow(ctx, 1110, 300, 90, 'rgba(255,214,140,A)', .18);
  shape(ctx, rect(1040, 290, 140, 18), '#1a2238', 2.4);
  snowGround(ctx, 480);
  // sidewalk edge + curb snow
  shape(ctx, rect(0, 560, W, 12), '#e9f0fb', 2.6);
  lamp(ctx, 760, 250, 560, -1); lamp(ctx, 250, 240, 560, 1);
  // footprints trail behind couple
  const r = rng(9); ctx.fillStyle = 'rgba(70,85,120,.55)';
  for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.ellipse(820 + i * 32, 538 + (i % 2) * 10, 7, 3.5, 0, 0, 7); ctx.fill(); }
  // couple walking away from camera, toward the left-centre
  figure(ctx, 790, 560, {s: 1.0, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: -1}, legs: [[-6, -14], [8, 16]], face: -1});
  figure(ctx, 725, 560, {s: .93, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: -1}, legs: [[-4, -12], [6, 12]], face: -1});
  snowfall(ctx, 3, 160);
  if (st === 'after') {
    // the gunman's silhouette in the doorway + long shadow toward the couple
    ctx.fillStyle = 'rgba(8,10,18,.55)';
    ctx.beginPath(); ctx.moveTo(1090, 480); ctx.lineTo(1135, 480); ctx.lineTo(860, 600); ctx.lineTo(815, 594); ctx.closePath(); ctx.fill();
    figure(ctx, 1110, 478, {s: .95, coat: ['#121216', '#08080a'], head: {hair: 'cap', look: -1, eyes: 'shadow', mouth: null, shade: 'rgba(20,22,32,.55)'}, legs: [[-4, -10], [4, 10]], arms: [[-10, 34, -12, 64], [10, 34, 12, 64]]});
  }
}

// ---------- SHOT 1: Grand cinema exterior ----------
function cinema(ctx, st) {
  nightSky(ctx, 470);
  building(ctx, -20, 20, 330, 460, '#40506a', '#344158', 11, .45);
  building(ctx, 960, 30, 340, 450, '#4a4562', '#3c3852', 12, .4);
  // cinema facade
  shape(ctx, rect(300, 60, 670, 420), '#6b3a3a', 3.2); shape(ctx, rect(860, 60, 110, 420), '#5a2f30', 0); shape(ctx, rect(300, 60, 670, 420), null, 3.2);
  // vertical neon blade sign (lamps only, no letters)
  shape(ctx, rect(330, 70, 58, 250), '#2a1416', 3);
  for (let i = 0; i < 7; i++) { shape(ctx, circ(359, 96 + i * 33, 11), '#ff6b5d', 2.2); }
  glow(ctx, 359, 195, 160, 'rgba(255,90,80,A)', .25);
  // marquee canopy with bulbs
  shape(ctx, poly([[400, 250], [940, 250], [970, 300], [370, 300]]), '#d6a24a', 3.2);
  shape(ctx, rect(370, 300, 600, 16), '#9c6b26', 2.6);
  for (let i = 0; i < 24; i++) shape(ctx, circ(388 + i * 25, 308, 4), '#fff1b0', 1.4);
  glow(ctx, 670, 330, 320, 'rgba(255,214,140,A)', .25);
  // doors
  for (let i = 0; i < 3; i++) {
    const dx = 520 + i * 100;
    shape(ctx, rect(dx, 330, 90, 150), st === 'after' && i === 1 ? '#f6dca0' : '#2c3548', 3);
    if (!(st === 'after' && i === 1)) { line(ctx, [[dx + 45, 330], [dx + 45, 480]], 2.4); shape(ctx, rect(dx + 34, 400, 6, 20), '#c9a34a', 1.6); shape(ctx, rect(dx + 50, 400, 6, 20), '#c9a34a', 1.6); }
  }
  // poster frames (no text)
  shape(ctx, rect(410, 340, 80, 120), '#2f3b5c', 3); shape(ctx, circ(450, 385, 20), '#d76b55', 2.4);
  shape(ctx, rect(850, 340, 80, 120), '#2f3b5c', 3); shape(ctx, poly([[860, 450], [890, 360], [920, 450]]), '#e2b84f', 2.4);
  snowGround(ctx, 480);
  shape(ctx, rect(0, 600, W, 12), '#e9f0fb', 2.6);
  volvo(ctx, 990, 640, '#8e3a34', '#6d2a26');
  snowfall(ctx, 13, 120);
  if (st === 'after') {
    // light spilling out of the open door, couple stepping out
    ctx.fillStyle = 'rgba(255,224,160,.35)'; ctx.beginPath(); ctx.moveTo(620, 480); ctx.lineTo(710, 480); ctx.lineTo(760, 560); ctx.lineTo(580, 560); ctx.closePath(); ctx.fill();
    figure(ctx, 690, 535, {s: .82, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .4, mouth: 'smile'}, arms: [[-12, 34, -16, 66], [16, 30, 26, 58]]});
    figure(ctx, 640, 535, {s: .76, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: .4, mouth: 'smile'}, arms: [[-12, 34, -16, 66], [18, 30, 30, 58]]});
  }
}

// ---------- SHOT 2: walking, no bodyguards, no car ----------
function walking(ctx, st) { // st: 'before' (ghost guards + car) | 'mid' (car only) | 'after' (empty)
  nightSky(ctx, 420);
  building(ctx, -20, 30, 420, 390, '#3c4b66', '#303d55', 21, .5);
  building(ctx, 400, 80, 380, 340, '#56506b', '#463f59', 22, .4);
  building(ctx, 780, 40, 520, 380, '#3f5570', '#32465d', 23, .45);
  snowGround(ctx, 420);
  // road strip behind curb
  shape(ctx, rect(0, 420, W, 70), '#5d6a86', 2.6); line(ctx, [[0, 455], [W, 455]], 3, '#e8ecf4');
  shape(ctx, rect(0, 488, W, 12), '#e9f0fb', 2.6);
  lamp(ctx, 1080, 170, 500, -1);
  // the couple, mid shot, walking left
  figure(ctx, 560, 650, {s: 1.05, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: -.6}, legs: [[-8, -18], [8, 18]], face: -1, arms: [[-10, 34, -14, 64], [-20, 30, -38, 52]]});
  figure(ctx, 470, 650, {s: .97, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: -.6}, legs: [[-6, -16], [6, 16]], face: -1, arms: [[-10, 34, -14, 64], [20, 30, 40, 50]]});
  snowfall(ctx, 23, 120);
  if (st === 'before' || st === 'mid') {
    if (st === 'before') { // ghost outlines of the absent bodyguards (dashed, translucent)
      ctx.save(); ctx.globalAlpha = .55; ctx.setLineDash([8, 7]);
      for (const gx of [720, 300]) {
        ctx.strokeStyle = '#d7e3ff'; ctx.lineWidth = 3;
        ctx.fillStyle = 'rgba(205,220,255,.42)';
        ctx.beginPath(); ctx.arc(gx, 440, 24, 0, 7); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(gx - 18, 470); ctx.lineTo(gx + 18, 470); ctx.lineTo(gx + 24, 580); ctx.lineTo(gx - 24, 580); ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(gx - 8, 580); ctx.lineTo(gx - 12, 650); ctx.moveTo(gx + 8, 580); ctx.lineTo(gx + 12, 650); ctx.stroke();
      }
      ctx.restore();
    }
    // ghost of the official car at the curb
    ctx.save(); ctx.globalAlpha = .5; ctx.setLineDash([9, 7]); ctx.strokeStyle = '#d7e3ff'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(820, 488); ctx.lineTo(1060, 488); ctx.lineTo(1066, 444); ctx.lineTo(1020, 438); ctx.lineTo(995, 400); ctx.lineTo(880, 400); ctx.lineTo(858, 440); ctx.lineTo(816, 446); ctx.closePath(); ctx.fillStyle = 'rgba(205,220,255,.42)'; ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.arc(868, 488, 20, 0, 7); ctx.moveTo(1032, 488); ctx.arc(1012, 488, 20, 0, 7); ctx.stroke(); ctx.restore();
  }
}

// ---------- SHOT 3: Palme close-up, flag rises behind ----------
function primeMinister(ctx, st) {
  ctx.fillStyle = vgrad(ctx, 0, H, [[0, '#1a2540'], [1, '#2f4366']]); ctx.fillRect(0, 0, W, H);
  // Rosenbad-style government building (turreted corner) behind
  shape(ctx, rect(640, 150, 560, 420), '#c9b48f', 3.2); shape(ctx, rect(1080, 150, 120, 420), '#ae9873', 0); shape(ctx, rect(640, 150, 560, 420), null, 3.2);
  shape(ctx, rect(780, 70, 120, 100), '#c9b48f', 3); shape(ctx, poly([[770, 72], [840, 10], [910, 72]]), '#3f6b63', 3);
  for (let i = 0; i < 5; i++) for (let j = 0; j < 4; j++) shape(ctx, rect(670 + i * 105, 190 + j * 90, 50, 56), (i + j) % 3 ? '#f2c66d' : '#33405c', 2.2);
  line(ctx, [[960, 150], [960, 30]], 4); // flagpole
  if (st === 'after') { // Swedish flag unfurled
    shape(ctx, c => { c.moveTo(962, 34); c.quadraticCurveTo(1010, 24, 1060, 38); c.lineTo(1060, 96); c.quadraticCurveTo(1010, 84, 962, 92); c.closePath(); }, '#2d6db5', 3);
    shape(ctx, rect(986, 30, 14, 64), '#f2c933', 0); shape(ctx, c => { c.moveTo(962, 56); c.quadraticCurveTo(1010, 48, 1060, 60); c.lineTo(1060, 72); c.quadraticCurveTo(1010, 62, 962, 70); c.closePath(); }, '#f2c933', 0);
    shape(ctx, c => { c.moveTo(962, 34); c.quadraticCurveTo(1010, 24, 1060, 38); c.lineTo(1060, 96); c.quadraticCurveTo(1010, 84, 962, 92); c.closePath(); }, null, 3);
  } else shape(ctx, poly([[962, 120], [978, 116], [978, 150], [962, 150]]), '#2d6db5', 2.6); // furled
  shape(ctx, rect(0, 600, W, 120), '#9fb0cf', 3);
  snowfall(ctx, 33, 90, 0, W, 0, 600, .7);
  // Palme, large, three-quarter view, left of frame
  figure(ctx, 380, 960, {s: 3.0, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .35, eyes: 'dot', mouth: 'flat'}, arms: [[-12, 34, -16, 66], [12, 34, 16, 66]]});
}

// ---------- SHOT 4: morning, security detail sent home (background + guards sprite) ----------
function morningDoor(ctx) {
  ctx.fillStyle = vgrad(ctx, 0, 460, [[0, '#9cc3e8'], [1, '#d9e8f5']]); ctx.fillRect(0, 0, W, 460);
  // old-town facade (Västerlånggatan): ochre and red narrow houses
  const cols = [['#d9a24f', '#bf8a3d'], ['#b8503f', '#9c4033'], ['#e4c27a', '#c9a862'], ['#7f8f5a', '#6b7a4a']];
  cols.forEach(([c1, c2], i) => building(ctx, -10 + i * 330, 30 + (i % 2) * 30, 330, 460, c1, c2, 40 + i, .15));
  // front door
  shape(ctx, rect(540, 300, 130, 190), '#5a3a28', 3.2); shape(ctx, c => c.arc(605, 300, 65, Math.PI, 0), '#5a3a28', 3.2);
  shape(ctx, rect(600, 300, 70, 190), '#4a2f20', 0); line(ctx, [[605, 300], [605, 490]], 2.4); shape(ctx, circ(620, 400, 5), '#d4a84a', 1.6);
  snowGround(ctx, 490);
  shape(ctx, rect(0, 560, W, 10), '#f2f6fc', 2.4);
  // Palme at the door, glove raised: "go on home"
  figure(ctx, 470, 600, {s: 1.05, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .6, mouth: 'smile'}, arms: [[-12, 34, -16, 66], [26, 10, 44, -18]], gloveAng: [0, -.4]});
}
function guardsSprite(ctx) { // two plain-clothes bodyguards, drawn on transparent canvas (520x420 design)
  for (const [gx, sc] of [[150, 1.02], [330, 1.0]]) {
    figure(ctx, gx, 400, {s: sc, coat: ['#3b3d44', '#2c2e34'], head: {look: -.7, eyes: 'dot', mouth: 'flat'}, legs: [[4, 12], [-6, -14]], face: 1});
    // earpiece wire
    line(ctx, [[gx - 6 * sc, 400 - 165 * sc], [gx - 2 * sc, 400 - 130 * sc]], 1.6, '#c9c9c9');
  }
}

// ---------- SHOT 5: cinema interior, screen lights up ----------
function cinemaInside(ctx, st) {
  ctx.fillStyle = '#121626'; ctx.fillRect(0, 0, W, H);
  // screen
  shape(ctx, rect(200, 40, 880, 330), st === 'after' ? '#e8eef8' : '#2a3044', 4);
  if (st === 'after') { ctx.fillStyle = 'rgba(200,220,255,.18)'; ctx.beginPath(); ctx.moveTo(200, 370); ctx.lineTo(1080, 370); ctx.lineTo(1280, 720); ctx.lineTo(0, 720); ctx.closePath(); ctx.fill();
    // a simple scene on the screen: two cartoon brothers' silhouettes (comedy), no text
    shape(ctx, rect(200, 300, 880, 70), '#c7d3e6', 0); shape(ctx, circ(560, 210, 40), '#9fb3d1', 3); shape(ctx, circ(720, 210, 40), '#9fb3d1', 3);
    line(ctx, [[560, 250], [560, 320]], 6, '#7d8fb0'); line(ctx, [[720, 250], [720, 320]], 6, '#7d8fb0'); }
  shape(ctx, rect(170, 30, 940, 18), '#7a2a2e', 3); shape(ctx, rect(150, 30, 60, 380), '#8a2f33', 3); shape(ctx, rect(1070, 30, 60, 380), '#8a2f33', 3);
  // rows of seats
  for (let row = 0; row < 2; row++) for (let i = 0; i < 9; i++) {
    const sx = 40 + i * 140 + row * 60, sy = 470 + row * 120;
    shape(ctx, c => { c.roundRect(sx, sy, 120, 110, 16); }, row ? '#6e2228' : '#7e2a30', 3);
  }
  // the couple seated (heads and shoulders above the front row), seen from behind/side, faces lit
  const lit = st === 'after';
  figure(ctx, 660, 820, {s: 1.9, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .3, mouth: lit ? 'smile' : 'flat', shade: lit ? null : 'rgba(30,36,60,.55)'}});
  figure(ctx, 500, 820, {s: 1.78, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: .3, mouth: lit ? 'smile' : 'flat', shade: lit ? null : 'rgba(30,36,60,.55)'}});
  shape(ctx, c => c.roundRect(300, 600, 560, 140, 18), '#5c1b21', 3);
}

// ---------- SHOT 6: street clock 11:20 -> 11:21 (background + minute-hand sprite) ----------
function streetClock(ctx) {
  nightSky(ctx, H);
  building(ctx, -20, 60, 520, 700, '#3c4b66', '#303d55', 61, .5);
  building(ctx, 860, 30, 440, 720, '#56506b', '#463f59', 62, .4);
  // lamp-post clock
  line(ctx, [[660, 720], [660, 470]], 14); line(ctx, [[660, 720], [660, 470]], 8, '#3b4e46');
  shape(ctx, circ(660, 300, 190), '#2f4a40', 4); shape(ctx, circ(660, 300, 165), '#f7f1df', 3.5);
  for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2, r1 = i % 5 ? 152 : 138; line(ctx, [[660 + Math.sin(a) * r1, 300 - Math.cos(a) * r1], [660 + Math.sin(a) * 158, 300 - Math.cos(a) * 158]], i % 5 ? 2 : 5); }
  // hour hand pointing just past 11
  const ha = (11 + 21 / 60) / 12 * Math.PI * 2; line(ctx, [[660, 300], [660 + Math.sin(ha) * 90, 300 - Math.cos(ha) * 90]], 11);
  glow(ctx, 660, 300, 260, 'rgba(255,230,170,A)', .12);
  snowfall(ctx, 63, 130);
}
function minuteHand(ctx) { // 400x400 design canvas, pivot at centre (200,200), hand pointing straight up (12)
  line(ctx, [[200, 220], [200, 62]], 13, '#f7f1df'); shape(ctx, circ(200, 200, 15), '#f7f1df', 0);
  line(ctx, [[200, 220], [200, 62]], 7); shape(ctx, circ(200, 200, 12), INK, 0); shape(ctx, circ(200, 200, 4), '#d6b25a', 0);
}

// ---------- SHOT 7: corner of Tunnelgatan, gunman steps out (bg + gunman sprite + wall occluder) ----------
function tunnelCorner(ctx) {
  nightSky(ctx, 470);
  building(ctx, 520, 40, 420, 440, '#4a4562', '#3c3852', 71, .3);
  building(ctx, 940, 90, 360, 390, '#3f5570', '#32465d', 72, .35);
  // Tunnelgatan: dark passage and stairs going up at the back-left
  shape(ctx, rect(150, 200, 330, 290), '#0e1220', 3.2);
  for (let i = 0; i < 9; i++) shape(ctx, rect(190 + i * 6, 430 - i * 24, 260 - i * 12, 22), '#232a3c', 2);
  snowGround(ctx, 480);
  shape(ctx, rect(0, 560, W, 12), '#e9f0fb', 2.6);
  lamp(ctx, 1130, 230, 560, -1);
  // couple in foreground right, walking away from camera
  figure(ctx, 930, 610, {s: 1.0, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .6}, legs: [[-6, -14], [8, 16]]});
  figure(ctx, 1015, 610, {s: .93, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: .6}, legs: [[-6, -14], [6, 14]]});
  snowfall(ctx, 73, 130);
}
function cornerWall(ctx) { // occluding wall on the left edge: 520x720 design canvas, transparent right side
  shape(ctx, rect(-10, 0, 560, 720), null, 0);
  shape(ctx, poly([[0, 0], [520, 0], [520, 480], [480, 500], [0, 500]]), '#5d566f', 3.2);
  shape(ctx, rect(440, 0, 80, 500), '#4b445c', 0);
  for (let j = 0; j < 4; j++) shape(ctx, rect(60, 60 + j * 105, 120, 70), '#26324c', 2.2);
  shape(ctx, poly([[0, 0], [520, 0], [520, 480], [480, 500], [0, 500]]), null, 3.2);
  shape(ctx, rect(0, 500, 520, 220), '#b3c2dd', 0); line(ctx, [[0, 500], [480, 500]], 3);
}
function gunmanSprite(ctx) { // 260x420 design canvas; feet at (130, 405)
  figure(ctx, 130, 405, {s: 1.05, coat: ['#1d1d22', '#141418'], head: {hair: 'cap', look: 1, eyes: 'shadow', mouth: null, shade: 'rgba(20,22,32,.6)'}, legs: [[8, 18], [-6, -14]], arms: [[-12, 34, -16, 66], [12, 34, 18, 64]]});
}

// ---------- SHOT 8: over the gunman's shoulder; arm raises (bg + arm sprite + flash) ----------
function behindPalme(ctx) {
  nightSky(ctx, 430);
  building(ctx, -20, 40, 420, 390, '#3c4b66', '#303d55', 81, .45);
  building(ctx, 400, 90, 420, 340, '#56506b', '#463f59', 82, .35);
  building(ctx, 820, 50, 480, 380, '#3f5570', '#32465d', 83, .4);
  snowGround(ctx, 430);
  lamp(ctx, 220, 160, 520, 1);
  // Palme's back, mid-distance, Lisbet beside
  figure(ctx, 640, 600, {s: 1.2, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: 0, eyes: null, mouth: null}, legs: [[-6, -14], [8, 16]]});
  figure(ctx, 760, 600, {s: 1.1, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: 0, eyes: null, mouth: null}, legs: [[-6, -14], [6, 14]]});
  snowfall(ctx, 83, 110);
  // gunman's dark shoulder & capped head, foreground left (cut by frame)
  shape(ctx, poly([[-20, 720], [-20, 470], [120, 440], [250, 470], [300, 720]]), '#1b1b20', 3.2);
  head(ctx, 120, 380, 95, {hair: 'cap', look: 1, eyes: null, mouth: null, shade: 'rgba(15,16,24,.75)'});
}
function gunArm(ctx) { // 600x200 design canvas; shoulder pivot at (40,100); arm extended to the right, horizontal
  line(ctx, [[40, 100], [250, 104], [430, 100]], 34, '#6c7898');
  line(ctx, [[40, 100], [250, 104], [430, 100]], 26, INK); line(ctx, [[40, 100], [250, 104], [430, 100]], 18, '#1d1d22');
  glove(ctx, 452, 102, 2.2, .1);
  // revolver
  shape(ctx, poly([[452, 78], [560, 74], [560, 92], [470, 96]]), '#2a2b30', 3);
  shape(ctx, c => c.roundRect(468, 70, 34, 34, 8), '#3a3b40', 3);
  shape(ctx, poly([[452, 96], [470, 96], [462, 132], [440, 128]]), '#4a3226', 3);
}
function muzzleFlash(ctx) { // 160x160 design canvas
  const pts = []; for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2, r = i % 2 ? 34 : 74; pts.push([80 + Math.cos(a) * r, 80 + Math.sin(a) * r]); }
  shape(ctx, poly(pts), '#ffd76a', 3); shape(ctx, circ(80, 80, 26), '#fff6d0', 0);
}

function gunSmoke(ctx) { // 260x180 design canvas: drifting grey cordite puff
  for (const [x, y, r] of [[60, 120, 34], [105, 95, 42], [160, 105, 38], [200, 75, 30], [130, 60, 30]]) shape(ctx, circ(x, y, r), '#b9c0cc', 2.6, '#5c6372');
  for (const [x, y, r] of [[95, 100, 22], [150, 95, 20]]) shape(ctx, circ(x, y, r), '#d5dae3', 0);
}

// ---------- SHOT 9: Palme falls; Lisbet turns in shock ----------
function fallScene(ctx, st) {
  nightSky(ctx, 430);
  building(ctx, -20, 40, 520, 390, '#3c4b66', '#303d55', 91, .45);
  building(ctx, 500, 70, 400, 360, '#56506b', '#463f59', 92, .35);
  building(ctx, 900, 30, 400, 400, '#3f5570', '#32465d', 93, .4);
  snowGround(ctx, 430);
  lamp(ctx, 1150, 150, 520, -1);
  // Lisbet, turning back in shock
  figure(ctx, 820, 640, {s: 1.25, coat: ['#d9c39c', '#bfa57a'], head: {hair: 'lisbet', look: -.8, eyes: st === 'after' ? 'wide' : 'dot', mouth: st === 'after' ? 'o' : 'flat'},
    arms: st === 'after' ? [[-30, 10, -50, -20], [30, 10, 36, -16]] : [[-12, 34, -16, 66], [12, 34, 16, 66]], legs: [[-8, -16], [8, 18]]});
  snowfall(ctx, 93, 110);
}
function palmeFallSprite(ctx) { // 400x400 design canvas; feet pivot at (200, 390)
  figure(ctx, 200, 390, {s: 1.25, coat: ['#24324f', '#1a2540'], scarf: '#9a2f2f', head: {hair: 'palme', look: .3, eyes: 'calm', mouth: 'flat'}, legs: [[-6, -14], [8, 16]]});
}

// ---------- export ----------
const jobs = [
  ['s00-before.png', c => sveavagenWide(c, 'before')], ['s00-after.png', c => sveavagenWide(c, 'after')],
  ['s01-before.png', c => cinema(c, 'before')], ['s01-after.png', c => cinema(c, 'after')],
  ['s02-before.png', c => walking(c, 'before')], ['s02-mid.png', c => walking(c, 'mid')], ['s02-after.png', c => walking(c, 'after')],
  ['s03-before.png', c => primeMinister(c, 'before')], ['s03-after.png', c => primeMinister(c, 'after')],
  ['s04-bg.png', c => morningDoor(c)],
  ['s05-before.png', c => cinemaInside(c, 'before')], ['s05-after.png', c => cinemaInside(c, 'after')],
  ['s06-bg.png', c => streetClock(c)],
  ['s07-bg.png', c => tunnelCorner(c)],
  ['s08-bg.png', c => behindPalme(c)],
  ['s09-bg-before.png', c => fallScene(c, 'before')], ['s09-bg-after.png', c => fallScene(c, 'after')],
];
for (const [name, fn] of jobs) { const [c, ctx] = canvas(); fn(ctx); save(c, name); }
const sprites = [
  ['s04-guards.png', 520, 420, guardsSprite], ['s06-minute.png', 400, 400, minuteHand],
['s07-gunman.png', 260, 420, gunmanSprite],
  ['s08-arm.png', 600, 200, gunArm], ['s08-flash.png', 160, 160, muzzleFlash], ['s08-smoke.png', 260, 180, gunSmoke], ['s09-palme.png', 400, 400, palmeFallSprite],
];
for (const [name, w, h, fn] of sprites) { const [c, ctx] = canvas(w, h); fn(ctx); save(c, name); }
