// Entry: preview (default) or export mode (?export=1, driven by scripts/render.ts), as in pdoom-video-sbs.
import { Editor, loadFonts, type Program } from './engine';

const params = new URLSearchParams(location.search);
const EXPORT = params.has('export');
const SCALE = Math.max(1, Math.round(+(params.get('scale') ?? '1')));
const canvas = document.getElementById('c') as HTMLCanvasElement;

declare global { interface Window { __edit: any } }

async function boot() {
  await loadFonts();
  const program: Program = await (await fetch('program.json')).json();
  const ed = new Editor(canvas, program, SCALE);
  if (EXPORT) setupExport(ed, program);
  else setupPreview(ed, program);
}

function setupExport(ed: Editor, program: Program) {
  document.body.classList.add('export');
  window.__edit = {
    ready: true, program, layout: ed.lay, width: canvas.width, height: canvas.height,
    card(ci: number, k: number) { ed.card(ci, k); },
    hud(si: number) { ed.hud(si); },
    /** The current canvas as a PNG (with alpha), base64. */
    png(): string { return canvas.toDataURL('image/png').split(',')[1]!; },
    /**
     * Stream every frame of chapter ci's card as raw RGBA (top-down) over a WebSocket. The receiver acknowledges each
     * frame with its running count; at most `inflight` frames are unacknowledged (backpressure from the encoder).
     */
    async streamCard(ci: number, url: string, inflight = 4) {
      const ws = new WebSocket(url);
      ws.binaryType = 'arraybuffer';
      let acked = 0;
      ws.onmessage = (e) => { if (typeof e.data === 'string') acked = Math.max(acked, +e.data || 0); };
      await new Promise<void>((res, rej) => { ws.onopen = () => res(); ws.onerror = (e) => rej(e); });
      const n = program.chapters[ci]!.card_frames;
      for (let k = 0; k < n; k++) {
        ed.card(ci, k);
        while (k - acked >= inflight) await new Promise((r) => setTimeout(r, 2));
        ws.send(ed.rgba());
      }
      while (ws.bufferedAmount > 0) await new Promise((r) => setTimeout(r, 5));
      ws.close();
      return n;
    },
  };
}

function setupPreview(ed: Editor, program: Program) {
  document.body.classList.add('preview');
  const ui = document.getElementById('ui')!;
  // keys: ←/→ previous/next scene, ↑/↓ previous/next chapter card; the card animates in a loop
  let mode: 'card' | 'hud' = 'card', ci = 0, si = 0, k = 0;
  const draw = () => {
    if (mode === 'card') ed.card(ci, k % program.chapters[ci]!.card_frames);
    else ed.hud(si);
    const s = ed.lay.scenes[si];
    ui.textContent = mode === 'card' ? `card ${ci + 1}/${program.chapters.length}: ${program.chapters[ci]!.title}  frame ${k % program.chapters[ci]!.card_frames}`
      : `scene ${si + 1}/${ed.lay.scenes.length}: ${s?.id}  starts at frame ${s?.start}`;
  };
  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'ArrowRight') { mode = 'hud'; si = Math.min(ed.lay.scenes.length - 1, si + 1); }
    if (ev.key === 'ArrowLeft') { mode = 'hud'; si = Math.max(0, si - 1); }
    if (ev.key === 'ArrowDown') { mode = 'card'; ci = Math.min(program.chapters.length - 1, ci + 1); k = 0; }
    if (ev.key === 'ArrowUp') { mode = 'card'; ci = Math.max(0, ci - 1); k = 0; }
  });
  const tick = () => { k++; draw(); requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
}

boot().catch((e) => {
  console.error(e);
  window.__edit = { error: String(e?.stack ?? e) };
});
