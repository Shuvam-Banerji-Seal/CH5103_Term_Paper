#!/usr/bin/env bun
// Offline renderer for the editorial layer, adapted from pdoom-video-sbs/app/scripts/render.ts (MIT): drives the
// editor page in headless Chromium (?export=1) and streams frames over a WebSocket into ffmpeg.
//   cards:  bun scripts/render.ts cards [--only ch03_two_electrons,...]  -> video/build/editor/cards/<chapter>.mkv
//   hud:    bun scripts/render.ts hud                                   -> video/build/editor/hud/<NNN>_<Scene>.png
//   stills: bun scripts/render.ts stills [--cards 0,6] [--k 45]         -> video/build/editor/stills/*.png
// Needs video/build/program.json (python3 video/tools/program.py --probe). Uses the Vite dev server at --url
// (default http://localhost:5174); starts a private one if unreachable.
import { chromium, type Page } from 'playwright-core';
import { mkdirSync } from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const mode = argv[0] ?? 'stills';
const opt = (k: string, d?: string) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : d; };
const APP = path.resolve(import.meta.dir, '..');
const ROOT = path.resolve(APP, '../..');
const OUT = path.join(ROOT, 'video/build/editor');
const CHROMIUM = opt('chromium', process.env.CHROMIUM ?? '/usr/bin/chromium')!;

async function reachable(url: string) {
  try { const r = await fetch(url, { signal: AbortSignal.timeout(1500) }); return r.ok; } catch { return false; }
}

async function ensureServer(): Promise<{ url: string; stop: () => void }> {
  const url = opt('url', 'http://localhost:5174')!;
  if (await reachable(url)) return { url, stop: () => {} };
  const port = 5300 + Math.floor(Math.random() * 500);
  const proc = Bun.spawn(['bunx', 'vite', '--port', String(port), '--strictPort'], { cwd: APP, stdout: 'ignore', stderr: 'ignore' });
  const u = `http://localhost:${port}`;
  for (let i = 0; i < 200 && !(await reachable(u)); i++) await Bun.sleep(100);
  return { url: u, stop: () => proc.kill() };
}

async function openPage(url: string) {
  // Linux: the system Chromium with software rendering (the layer is 2D canvas; pdoom's channel 'chrome' with
  // ANGLE-on-Metal is macOS-only)
  const browser = await chromium.launch({
    executablePath: CHROMIUM, headless: true,
    args: ['--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'],
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const logs: string[] = [];
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') logs.push(`[${m.type()}] ${m.text()}`); });
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  await page.goto(`${url}/?export=1`);
  await page.waitForFunction(() => (window as any).__edit?.ready || (window as any).__edit?.error, null, { timeout: 120000 });
  const err = await page.evaluate(() => (window as any).__edit.error);
  if (err) throw new Error(`editor failed to boot:\n${err}\n${logs.join('\n')}`);
  return { browser, page, logs };
}

async function savePng(page: Page, file: string) {
  await Bun.write(file, Buffer.from(await page.evaluate(() => (window as any).__edit.png()), 'base64'));
}

async function cards(page: Page) {
  const program = await page.evaluate(() => (window as any).__edit.program);
  const only = opt('only')?.split(',');
  const dir = path.join(OUT, 'cards');
  mkdirSync(dir, { recursive: true });
  for (let ci = 0; ci < program.chapters.length; ci++) {
    const ch = program.chapters[ci];
    if (only && !only.includes(ch.id)) continue;
    const out = path.join(dir, `${ch.id}.mkv`);
    // lossless intermediate; the assembler encodes every segment once, with the final settings
    const ff = Bun.spawn(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', `${program.width}x${program.height}`,
      '-r', String(program.fps), '-i', 'pipe:0', '-c:v', 'libx264rgb', '-qp', '0', '-preset', 'ultrafast', out],
      { stdin: 'pipe', stdout: 'inherit', stderr: 'inherit' });
    let frames = 0;
    const server = Bun.serve({
      port: 0,
      fetch(req, srv) { return srv.upgrade(req) ? undefined : new Response('ws only', { status: 400 }); },
      websocket: {
        maxPayloadLength: program.width * program.height * 4 + 1024,
        async message(ws, msg) {
          ff.stdin.write(msg as Uint8Array);
          await ff.stdin.flush();
          frames++;
          ws.send(String(frames));
        },
      },
    });
    const n: number = await page.evaluate(([ci, url]) => (window as any).__edit.streamCard(ci, url), [ci, `ws://localhost:${server.port}`] as const);
    while (frames < n) await Bun.sleep(10);
    ff.stdin.end();
    await ff.exited;
    server.stop();
    console.log(`${out}  ${frames} frames`);
  }
}

async function hud(page: Page) {
  const lay = await page.evaluate(() => (window as any).__edit.layout);
  const dir = path.join(OUT, 'hud');
  mkdirSync(dir, { recursive: true });
  for (let si = 0; si < lay.scenes.length; si++) {
    await page.evaluate((si) => (window as any).__edit.hud(si), si);
    await savePng(page, path.join(dir, `${String(si).padStart(3, '0')}_${lay.scenes[si].id}.png`));
  }
  console.log(`${lay.scenes.length} HUD overlays -> ${dir}`);
}

async function stills(page: Page) {
  const dir = path.join(OUT, 'stills');
  mkdirSync(dir, { recursive: true });
  const k = +opt('k', '45')!;
  for (const ci of (opt('cards', '0') ?? '0').split(',').map(Number)) {
    await page.evaluate(([ci, k]) => (window as any).__edit.card(ci, k), [ci, k] as const);
    const f = path.join(dir, `card_${ci}_${k}.png`);
    await savePng(page, f);
    console.log(f);
  }
  for (const si of (opt('huds', '0') ?? '0').split(',').map(Number)) {
    await page.evaluate((si) => (window as any).__edit.hud(si), si);
    const f = path.join(dir, `hud_${si}.png`);
    await savePng(page, f);
    console.log(f);
  }
}

const { url, stop } = await ensureServer();
const { browser, page, logs } = await openPage(url);
try {
  if (mode === 'cards') await cards(page);
  else if (mode === 'hud') await hud(page);
  else await stills(page);
  if (logs.length) console.error('BROWSER LOG:\n' + logs.slice(0, 40).join('\n'));
} finally {
  await browser.close();
  stop();
}
