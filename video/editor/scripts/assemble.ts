#!/usr/bin/env bun
// Final assembly: every segment (a chapter card, or a scene with its HUD overlay) is encoded once with the same
// x264 settings, the encoded segments are joined without re-encoding, and one continuous narration track is built
// sample-exactly alongside: at 30 fps and 48 kHz a frame is exactly 1600 samples, so each segment's audio is cut or
// padded to frames x 1600 samples and the two tracks cannot drift apart.
//
//   bun scripts/assemble.ts [--crf 12] [--preset slow] [--jobs 4] [--only 0-12] [--out ../../video/build/final/ch5103-explainer.mp4]
//   bun scripts/assemble.ts --scale 2     # the 4K version: scenes4k/, editor4k/, program4k.json, HEVC on the GPU (VAAPI)
//
// Inputs: video/build/program.json (python3 video/tools/program.py --probe), the scene renders
// video/build/scenes/<file>/<Scene>.mp4 (+ .srt), the cards and HUD overlays (bun scripts/render.ts cards / hud).
// Outputs: the MP4, an .srt with every scene's captions shifted to its place in the programme, chapters.txt
// (YouTube-style chapter list) and a verification report.
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const opt = (k: string, d?: string) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : d; };
const APP = path.resolve(import.meta.dir, '..');
const ROOT = path.resolve(APP, '../..');
const BUILD = path.join(ROOT, 'video/build');
const K4 = opt('scale', '1') === '2';
const SFX = K4 ? '4k' : '';
const WORK = path.join(BUILD, `assemble${SFX}`);
const OUTFILE = path.resolve(opt('out', path.join(BUILD, `final/ch5103-explainer${K4 ? '-4k' : ''}.mp4`))!);
// CRF 12: the slides are mostly still, so even this costs ~270 kb/s, and on 1080p scenes x264 runs at the same speed
// at CRF 12 as at 22 (SSIM 0.99994 against the render, vs 0.9995 at 22)
const CRF = opt('crf', '12')!, PRESET = opt('preset', 'slow')!;
// segments encode in parallel: one ffmpeg (decode, HUD overlay, x264 on a mostly still picture) uses only a few cores
const JOBS = Math.max(1, +opt('jobs', K4 ? '2' : '4')!);
const RATE = 48000;

interface Scene { id: string; file: string; frames: number }
interface Chapter { id: string; part: string; title: string; card_frames: number; scenes: Scene[] }
const program: { fps: number; width: number; height: number; total_frames: number; chapters: Chapter[] } =
  JSON.parse(readFileSync(path.join(BUILD, `program${SFX}.json`), 'utf8'));
if (K4) {  // the cards and HUD were laid out from program.json: the 4K renders must have the same frame counts
  const p1 = JSON.parse(readFileSync(path.join(BUILD, 'program.json'), 'utf8'));
  if (JSON.stringify(p1.chapters.map((c: Chapter) => c.scenes.map((s) => s.frames))) !==
      JSON.stringify(program.chapters.map((c) => c.scenes.map((s) => s.frames))))
    throw new Error('4K renders differ in frame counts from the 1080p programme');
}
if ((program as any).provisional) throw new Error('program.json is provisional: run python3 video/tools/program.py --probe');
const FPS = program.fps;
const SPF = RATE / FPS;
if (!Number.isInteger(SPF)) throw new Error(`${RATE} Hz is not a whole number of samples per frame at ${FPS} fps`);

function run(args: string[], quiet = true) {
  const p = Bun.spawnSync(args, { stdout: 'pipe', stderr: 'pipe' });
  if (p.exitCode !== 0) throw new Error(`${args.join(' ')}\n${p.stderr.toString()}`);
  return p.stdout.toString();
}
async function runAsync(args: string[]) {
  const p = Bun.spawn(args, { stdout: 'pipe', stderr: 'pipe' });
  const [code, out, err] = await Promise.all([p.exited, new Response(p.stdout).text(), new Response(p.stderr).text()]);
  if (code !== 0) throw new Error(`${args.join(' ')}\n${err}`);
  return out;
}
const COUNT = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0'];
const countFrames = (f: string) => +run([...COUNT, f]).trim();
const countFramesAsync = async (f: string) => +(await runAsync([...COUNT, f])).trim();

type Seg = { kind: 'card' | 'scene'; label: string; frames: number; src: string; hud?: string; srt?: string; chapter: number };
const segs: Seg[] = [];
const ED = path.join(BUILD, `editor${SFX}`);
const hudFiles = existsSync(path.join(ED, 'hud')) ? readdirSync(path.join(ED, 'hud')).sort() : [];
let si = 0;
program.chapters.forEach((ch, ci) => {
  segs.push({ kind: 'card', label: `${ch.part}: ${ch.title}`, frames: ch.card_frames, src: path.join(ED, `cards/${ch.id}.mkv`), chapter: ci });
  for (const s of ch.scenes) {
    const mp4 = path.join(BUILD, `scenes${SFX}/${s.file}/${s.id}.mp4`);
    const hud = hudFiles[si] ? path.join(ED, 'hud', hudFiles[si]!) : undefined;
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
// 1080p: x264 on the CPU; 4K: HEVC on the GPU (VAAPI; a CPU encode of ~380k 4K frames would take most of a day)
const x264 = K4
  ? ['-c:v', 'hevc_vaapi', '-rc_mode', 'CQP', '-qp', opt('qp', '20')!, '-r', String(FPS), '-g', String(FPS * 10), '-tag:v', 'hvc1', '-an']
  : ['-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-tune', 'animation', '-pix_fmt', 'yuv420p',
     '-profile:v', 'high', '-level', '4.1', '-r', String(FPS), '-g', String(FPS * 10), '-bf', '3', '-an'];
const HW = K4 ? ['-vaapi_device', '/dev/dri/renderD128'] : [];
const UP = K4 ? ',format=nv12,hwupload' : '';
// a segment is reused only if it was encoded from the same inputs with the same settings (a stamp beside it)
const stampOf = (g: Seg) => JSON.stringify({ args: x264, frames: g.frames,
  inputs: [g.src, g.hud].filter(Boolean).map((f) => { const st = statSync(f!); return [f, st.size, st.mtimeMs]; }) });
async function encode(g: Seg, k: number) {
  const out = path.join(WORK, `v${String(k).padStart(3, '0')}.mp4`);
  const stampFile = out.replace(/\.mp4$/, '.json'), stamp = stampOf(g);
  if (existsSync(out) && existsSync(stampFile) && readFileSync(stampFile, 'utf8') === stamp
      && await countFramesAsync(out) === g.frames) return; // resumable
  const t0 = performance.now();
  if (g.kind === 'card') await runAsync(['ffmpeg', '-y', '-loglevel', 'error', ...HW, '-i', g.src, '-vf', `format=yuv420p${UP}`,
    '-frames:v', String(g.frames), ...x264, out]);
  else await runAsync(['ffmpeg', '-y', '-loglevel', 'error', ...HW, '-i', g.src, '-loop', '1', '-i', g.hud!, '-filter_complex',
    `[0:v][1:v]overlay=0:0:shortest=1:format=auto,format=yuv420p${UP}[v]`, '-map', '[v]', '-frames:v', String(g.frames), ...x264, out]);
  const n = await countFramesAsync(out);
  if (n !== g.frames) throw new Error(`${g.label}: encoded ${n} frames, expected ${g.frames}`);
  writeFileSync(stampFile, stamp);
  console.log(`v ${k}/${segs.length - 1} ${g.label}: ${n} frames in ${((performance.now() - t0) / 1000).toFixed(1)} s`);
}
const todo = segs.map((g, k) => [g, k] as const).filter(([, k]) => k >= lo && k <= hi);
let next = 0;
const tEnc = performance.now();
await Promise.all(Array.from({ length: JOBS }, async () => { while (next < todo.length) { const [g, k] = todo[next++]!; await encode(g, k); } }));
console.log(`video: ${todo.length} segments with ${JOBS} encoders in ${((performance.now() - tEnc) / 60000).toFixed(1)} min`);
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
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(WORK, 'audio.txt'), '-c:a', 'pcm_s16le', path.join(WORK, 'narration_raw.wav')]);
// two-pass EBU R128 loudness normalisation to -16 LUFS: measure, then apply one linear gain (speech dynamics kept)
const meas = Bun.spawnSync(['ffmpeg', '-hide_banner', '-i', path.join(WORK, 'narration_raw.wav'), '-af',
  'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], { stdout: 'pipe', stderr: 'pipe' }).stderr.toString();
const L = JSON.parse(meas.slice(meas.lastIndexOf('{'), meas.lastIndexOf('}') + 1));
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path.join(WORK, 'narration_raw.wav'), '-af',
  `loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=${L.input_i}:measured_TP=${L.input_tp}:measured_LRA=${L.input_lra}:measured_thresh=${L.input_thresh}:offset=${L.target_offset}:linear=true,aresample=${RATE}`,
  '-c:a', 'pcm_s16le', path.join(WORK, 'narration.wav')]);
console.log(`narration loudness ${L.input_i} LUFS -> -16 LUFS (true peak ${L.input_tp} dBTP)`);

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
