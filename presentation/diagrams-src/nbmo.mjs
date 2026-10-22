// NBMO diagrams for the disjoint / nondisjoint slides.
// For each pi framework: build the Hückel adjacency matrix, diagonalise it (Jacobi),
// take the zero-energy (non-bonding) pair, rotate it to minimise sum_i a_i^2 b_i^2
// (the ZDO on-site exchange, Hubbard K/U), and draw both orbitals on the molecular graph:
// lobe area ~ |c|^2, rose = +, blue = -.  Writes one SVG per molecule to ../figures/diagrams-svg/.
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "..", "figures", "diagrams-svg");
mkdirSync(outDir, { recursive: true });

const C = { bg: "#000000", bond: "#5d5d68", atom: "#ECE8E1", plus: "#FF5D8F", minus: "#7DB9FF",
            text: "#ECE8E1", muted: "#9C9AA6", gold: "#E9B95B", green: "#72DD8F" };

function jacobi(A) {                       // symmetric eigen-decomposition
  const n = A.length, a = A.map(r => r.slice()), V = A.map((_, i) => A.map((_, j) => +(i === j)));
  for (let sweep = 0; sweep < 100; sweep++) {
    let off = 0;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += a[p][q] ** 2;
    if (off < 1e-24) break;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
      if (Math.abs(a[p][q]) < 1e-15) continue;
      const th = 0.5 * Math.atan2(2 * a[p][q], a[q][q] - a[p][p]), c = Math.cos(th), s = Math.sin(th);
      for (let k = 0; k < n; k++) { const akp = a[k][p], akq = a[k][q]; a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq; }
      for (let k = 0; k < n; k++) { const apk = a[p][k], aqk = a[q][k]; a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk; }
      for (let k = 0; k < n; k++) { const vkp = V[k][p], vkq = V[k][q]; V[k][p] = c * vkp - s * vkq; V[k][q] = s * vkp + c * vkq; }
    }
  }
  return { values: a.map((r, i) => r[i]), vectors: V };
}

function nbmoPair(n, edges) {
  const A = Array.from({ length: n }, () => Array(n).fill(0));
  for (const [i, j] of edges) { A[i][j] = 1; A[j][i] = 1; }
  const { values, vectors } = jacobi(A);
  const zero = values.map((x, k) => [Math.abs(x), k]).filter(([x]) => x < 1e-8).map(([, k]) => k);
  if (zero.length !== 2) throw new Error(`expected 2 NBMOs, got ${zero.length}`);
  const u = vectors.map(r => r[zero[0]]), v = vectors.map(r => r[zero[1]]);
  let best = { s: Infinity };
  for (let k = 0; k <= 20000; k++) {
    const th = Math.PI * k / 20000, c = Math.cos(th), s = Math.sin(th);
    const a = u.map((x, i) => c * x + s * v[i]), b = u.map((x, i) => -s * x + c * v[i]);
    const sum = a.reduce((acc, x, i) => acc + x * x * b[i] * b[i], 0);
    if (sum < best.s) best = { s: sum, a, b };
  }
  return best;
}

function svgMolecule(name, pos, edges, orb, label, scale = 70) {
  const xs = pos.map(p => p[0]), ys = pos.map(p => p[1]);
  const pad = 1.0, w = (Math.max(...xs) - Math.min(...xs) + 2 * pad) * scale;
  const h = (Math.max(...ys) - Math.min(...ys) + 2 * pad) * scale;
  const X = x => (x - Math.min(...xs) + pad) * scale, Y = y => (Math.max(...ys) - y + pad) * scale;
  let g = "";
  for (const [i, j] of edges)
    g += `<line x1="${X(pos[i][0])}" y1="${Y(pos[i][1])}" x2="${X(pos[j][0])}" y2="${Y(pos[j][1])}" stroke="${C.bond}" stroke-width="3" stroke-linecap="round"/>`;
  orb.forEach((c, i) => {
    if (Math.abs(c) < 1e-6) return;
    const r = 0.62 * scale * Math.abs(c);
    const col = c > 0 ? C.plus : C.minus;
    g += `<circle cx="${X(pos[i][0])}" cy="${Y(pos[i][1])}" r="${r.toFixed(2)}" fill="${col}" fill-opacity="0.55" stroke="${col}" stroke-width="1.5"/>`;
  });
  pos.forEach(([x, y]) => { g += `<circle cx="${X(x)}" cy="${Y(y)}" r="4" fill="${C.atom}"/>`; });
  return { w, h, body: g, label };
}

function writePanel(file, title, panels, footer, footColor) {
  const gap = 30, W = panels.reduce((s, p) => s + p.w, 0) + gap * (panels.length - 1), H = Math.max(...panels.map(p => p.h)) + 100;
  let x = 0, body = "";
  for (const p of panels) {
    body += `<g transform="translate(${x},70)">${p.body}<text x="${p.w / 2}" y="-12" text-anchor="middle" font-family="Libertinus Serif" font-style="italic" font-size="22" fill="${C.text}">${p.label}</text></g>`;
    x += p.w + gap;
  }
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<rect width="100%" height="100%" fill="${C.bg}"/>
<text x="0" y="22" font-family="Libertinus Serif" font-size="22" fill="${C.gold}">${title}</text>
${body}
<text x="${W / 2}" y="${H - 8}" text-anchor="middle" font-family="Libertinus Serif" font-size="19" fill="${footColor}">${footer}</text>
</svg>`;
  writeFileSync(join(outDir, file), svg);
}

const hex = k => [Math.cos(Math.PI / 2 - k * Math.PI / 3), Math.sin(Math.PI / 2 - k * Math.PI / 3)];
const molecules = {
  cbd: { title: "cyclobutadiene (D₄h)", pos: [[0, 0], [1.3, 0], [1.3, 1.3], [0, 1.3]], edges: [[0, 1], [1, 2], [2, 3], [3, 0]] },
  tme: { title: "tetramethyleneethane", pos: [[-0.6, 0], [0.6, 0], [-1.3, 1.0], [-1.3, -1.0], [1.3, 1.0], [1.3, -1.0]],
         edges: [[0, 1], [0, 2], [0, 3], [1, 4], [1, 5]] },
  tmm: { title: "trimethylenemethane", pos: [[0, 0], [0, 1.25], [1.08, -0.62], [-1.08, -0.62]], edges: [[0, 1], [0, 2], [0, 3]] },
  // ring atoms 0-5, exocyclic CH2 carbons 6 and 7 placed radially outward from ring atoms 0 and 2
  mx: { title: "m-xylylene", pos: [...[0, 1, 2, 3, 4, 5].map(hex), hex(0).map(x => 2 * x), hex(2).map(x => 2 * x)],
        edges: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [0, 6], [2, 7]] },
};

const summary = {};
for (const [key, m] of Object.entries(molecules)) {
  const { s, a, b } = nbmoPair(m.pos.length, m.edges);
  const disjoint = s < 1e-6;
  summary[key] = s;
  const sub = t => `<tspan baseline-shift="sub" font-size="70%">${t}</tspan>`;
  const sup = t => `<tspan baseline-shift="super" font-size="70%">${t}</tspan>`;
  const pa = svgMolecule(key, m.pos, m.edges, a, `φ${sub("a")}`);
  const pb = svgMolecule(key, m.pos, m.edges, b, `φ${sub("b")}`);
  const foot = disjoint
    ? `disjoint:  Σ a${sub("i")}${sup("2")} b${sub("i")}${sup("2")} = 0   ⇒   K${sub("ab")} = 0`
    : `nondisjoint:  min Σ a${sub("i")}${sup("2")} b${sub("i")}${sup("2")} = ${s.toFixed(4)}   ⇒   K${sub("ab")} &gt; 0`;
  writePanel(`nbmo_${key}.svg`, m.title, [pa, pb], foot, disjoint ? C.green : C.gold);
}
console.log(JSON.stringify(summary));
