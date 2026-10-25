#!/usr/bin/env bun
// Final assembly: every segment (a chapter card, or a scene with its HUD overlay) is encoded once with the same
// x264 settings, the encoded segments are joined without re-encoding, and one continuous narration track is built
// sample-exactly alongside: at 30 fps and 48 kHz a frame is exactly 1600 samples, so each segment's audio is cut or
// padded to frames x 1600 samples and the two tracks cannot drift apart.
//
//   bun scripts/assemble.ts [--crf 22] [--preset slow] [--only 0-12] [--out ../../video/build/final/ch5103-explainer.mp4]
//
// Inputs: video/build/program.json (python3 video/tools/program.py --probe), the scene renders
// video/build/scenes/<file>/<Scene>.mp4 (+ .srt), the cards and HUD overlays (bun scripts/render.ts cards / hud).
// Outputs: the MP4, an .srt with every scene's captions shifted to its place in the programme, chapters.txt
// (YouTube-style chapter list) and a verification report.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const opt = (k: string, d?: string) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : d; };
const APP = path.resolve(import.meta.dir, '..');
const ROOT = path.resolve(APP, '../..');
const BUILD = path.join(ROOT, 'video/build');
const WORK = path.join(BUILD, 'assemble');
const OUTFILE = path.resolve(opt('out', path.join(BUILD, 'final/ch5103-explainer.mp4'))!);
const CRF = opt('crf', '22')!, PRESET = opt('preset', 'slow')!;
const RATE = 48000;

interface Scene { id: string; file: string; frames: number }
interface Chapter { id: string; part: string; title: string; card_frames: number; scenes: Scene[] }
const program: { fps: number; width: number; height: number; total_frames: number; chapters: Chapter[] } =
  JSON.parse(readFileSync(path.join(BUILD, 'program.json'), 'utf8'));
if ((program as any).provisional) throw new Error('program.json is provisional: run python3 video/tools/program.py --probe');
const FPS = program.fps;
const SPF = RATE / FPS;
if (!Number.isInteger(SPF)) throw new Error(`${RATE} Hz is not a whole number of samples per frame at ${FPS} fps`);

function run(args: string[], quiet = true) {
  const p = Bun.spawnSync(args, { stdout: 'pipe', stderr: 'pipe' });
  if (p.exitCode !== 0) throw new Error(`${args.join(' ')}\n${p.stderr.toString()}`);
  return p.stdout.toString();
}
const countFrames = (f: string) => +run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
  'stream=nb_read_frames', '-of', 'csv=p=0', f]).trim();

type Seg = { kind: 'card' | 'scene'; label: string; frames: number; src: string; hud?: string; srt?: string; chapter: number };
const segs: Seg[] = [];
const hudFiles = existsSync(path.join(BUILD, 'editor/hud')) ? readdirSync(path.join(BUILD, 'editor/hud')).sort() : [];
let si = 0;
program.chapters.forEach((ch, ci) => {
  segs.push({ kind: 'card', label: `${ch.part}: ${ch.title}`, frames: ch.card_frames, src: path.join(BUILD, `editor/cards/${ch.id}.mkv`), chapter: ci });
  for (const s of ch.scenes) {
    const mp4 = path.join(BUILD, `scenes/${s.file}/${s.id}.mp4`);
    const hud = hudFiles[si] ? path.join(BUILD, 'editor/hud', hudFiles[si]!) : undefined;
    if (!hud || !hud.endsWith(`_${s.id}.png`)) throw new Error(`HUD overlay ${si} is not for ${s.id}: run bun scripts/render.ts hud`);
    segs.push({ kind: 'scene', label: `${s.file}:${s.id}`, frames: s.frames, src: mp4, hud, srt: mp4.replace(/\.mp4$/, '.srt'), chapter: ci });
    si++;
  }
});
for (const g of segs) if (!existsSync(g.src)) throw new Error(`missing ${g.src}`);

const [lo, hi] = (opt('only') ?? `0-${segs.length - 1}`).split('-').map(Number) as [number, number];
mkdirSync(WORK, { recursive: true });
mkdirSync(path.dirname(OUTFILE), { recursive: true });

// 1. video: one encode per segment (scenes get their HUD overlaid on every frame), checked frame by frame count
const x264 = ['-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-tune', 'animation', '-pix_fmt', 'yuv420p',
  '-profile:v', 'high', '-level', '4.1', '-r', String(FPS), '-g', String(FPS * 10), '-bf', '3', '-an'];
segs.forEach((g, k) => {
  if (k < lo || k > hi) return;
  const out = path.join(WORK, `v${String(k).padStart(3, '0')}.mp4`);
  if (existsSync(out) && countFrames(out) === g.frames) return; // resumable
  const t0 = performance.now();
  if (g.kind === 'card') run(['ffmpeg', '-y', '-loglevel', 'error', '-i', g.src, '-frames:v', String(g.frames), ...x264, out]);
  else run(['ffmpeg', '-y', '-loglevel', 'error', '-i', g.src, '-loop', '1', '-i', g.hud!, '-filter_complex',
    `[0:v][1:v]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]`, '-map', '[v]', '-frames:v', String(g.frames), ...x264, out]);
  const n = countFrames(out);
  if (n !== g.frames) throw new Error(`${g.label}: encoded ${n} frames, expected ${g.frames}`);
  console.log(`v ${k}/${segs.length - 1} ${g.label}: ${n} frames in ${((performance.now() - t0) / 1000).toFixed(1)} s`);
});
if (lo !== 0 || hi !== segs.length - 1) { console.log('partial run: segments encoded, nothing joined'); process.exit(0); }

// 2. audio: each segment's narration as 48 kHz stereo PCM, exactly frames x 1600 samples (cards: silence)
const pcm: string[] = [];
segs.forEach((g, k) => {
  const out = path.join(WORK, `a${String(k).padStart(3, '0')}.wav`);
  const samples = g.frames * SPF;
  if (g.kind === 'card') run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', `anullsrc=r=${RATE}:cl=stereo`,
    '-af', `atrim=end_sample=${samples}`, '-c:a', 'pcm_s16le', out]);
  else run(['ffmpeg', '-y', '-loglevel', 'error', '-i', g.src, '-vn', '-af',
    `aresample=${RATE},aformat=channel_layouts=stereo,apad=whole_len=${samples},atrim=end_sample=${samples}`, '-c:a', 'pcm_s16le', out]);
  pcm.push(out);
});
writeFileSync(path.join(WORK, 'audio.txt'), pcm.map((f) => `file '${f}'`).join('\n') + '\n');
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(WORK, 'audio.txt'), '-c:a', 'pcm_s16le', path.join(WORK, 'narration.wav')]);

// 3. join the encoded segments without re-encoding, add the narration as AAC
const vids = segs.map((_, k) => path.join(WORK, `v${String(k).padStart(3, '0')}.mp4`));
writeFileSync(path.join(WORK, 'video.txt'), vids.map((f) => `file '${f}'`).join('\n') + '\n');
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(WORK, 'video.txt'),
  '-i', path.join(WORK, 'narration.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
  '-metadata', 'title=CH5103: correlation and spin states, explained and checked', '-movflags', '+faststart', OUTFILE]);

// 4. captions and chapters on the programme clock
const ts = (f: number) => { const ms = Math.round((f / FPS) * 1000); const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
const parseTs = (s: string) => { const [h, m, r] = s.split(':'); const [sec, ms] = r!.split(','); return (+h! * 3600 + +m! * 60 + +sec!) + +ms! / 1000; };
let start = 0, n = 0;
const srt: string[] = [], chapters: string[] = [];
segs.forEach((g) => {
  if (g.kind === 'card') {
    const ts2 = ts(start).slice(0, 8);
    chapters.push(`${ts2} ${g.label}`);
  } else if (g.srt && existsSync(g.srt)) {
    for (const block of readFileSync(g.srt, 'utf8').trim().split(/\n\s*\n/)) {
      const lines = block.split('\n');
      const tl = lines.find((l) => l.includes('-->'));
      if (!tl) continue;
      const [a, b] = tl.split('-->').map((x) => parseTs(x.trim()));
      const text = lines.slice(lines.indexOf(tl) + 1).join('\n');
      srt.push(`${++n}\n${ts(start + a! * FPS)} --> ${ts(start + Math.min(b!, g.frames / FPS) * FPS)}\n${text}\n`);
    }
  }
  start += g.frames;
});
writeFileSync(OUTFILE.replace(/\.mp4$/, '.srt'), srt.join('\n'));
writeFileSync(OUTFILE.replace(/\.mp4$/, '.chapters.txt'), chapters.join('\n') + '\n');

// 5. verification: frame count, both durations, size
const frames = countFrames(OUTFILE);
const dur = (sel: string) => +run(['ffprobe', '-v', 'error', '-select_streams', sel, '-show_entries', 'stream=duration', '-of', 'csv=p=0', OUTFILE]).trim();
const vd = dur('v:0'), ad = dur('a:0');
const report = [
  `output ${OUTFILE}`,
  `frames ${frames} (program ${start}) ${frames === start ? 'OK' : 'MISMATCH'}`,
  `video ${vd.toFixed(3)} s, audio ${ad.toFixed(3)} s, difference ${(ad - vd).toFixed(3)} s ${Math.abs(ad - vd) < 1.5 / FPS + 0.03 ? 'OK' : 'MISMATCH'}`,
  `size ${(Bun.file(OUTFILE).size / 2 ** 30).toFixed(2)} GiB`,
  `captions ${n}, chapters ${chapters.length}`,
];
writeFileSync(OUTFILE.replace(/\.mp4$/, '.report.txt'), report.join('\n') + '\n');
console.log(report.join('\n'));
