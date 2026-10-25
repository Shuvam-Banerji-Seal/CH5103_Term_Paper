// The editorial layer of the video, as a deterministic function of the program position (the pdoom-video-sbs
// contract: a frame depends only on t, so any frame can be rendered in any order and re-rendered identically).
//
//   card(chapter, k): frame k of the chapter's title card (opaque, full frame)
//   hud(scene):       the overlay drawn over a scene (transparent except a progress bar along the top edge with
//                     ticks at the chapter starts, and the part label at the top right)
//
// Colours and fonts are the slides' noir theme (video/scenes/noir.py).

export interface SceneEntry { id: string; file: string; frames: number }
export interface Chapter { id: string; part: string; title: string; card_frames: number; scenes: SceneEntry[] }
export interface Program { fps: number; width: number; height: number; total_frames: number; chapters: Chapter[] }

export const C = {
  bg: '#000000', panel: '#111116', track: '#24242C', fg: '#ECE8E1', muted: '#9C9AA6', gold: '#E9B95B',
  cyan: '#5FD4D0', rose: '#FF5D8F',
};

const FONTS: [string, string][] = [
  ['TeX Gyre Chorus', 'texgyrechorus-mediumitalic.otf'],
  ['EB Garamond', 'EBGaramond-Regular.otf'],
  ['EB Garamond Medium', 'EBGaramond-Medium.otf'],
  ['Libertinus Serif', 'LibertinusSerif-Regular.otf'],
];

export async function loadFonts(base = 'fonts/') {
  for (const [family, file] of FONTS) {
    const f = new FontFace(family, `url(${base}${file})`);
    await f.load();
    document.fonts.add(f);
  }
}

/** Where each chapter and scene starts in the program (in frames), cards included. */
export function layout(p: Program) {
  const chapters: { start: number; cardEnd: number; end: number }[] = [];
  const scenes: { chapter: number; start: number; end: number; id: string }[] = [];
  let f = 0;
  p.chapters.forEach((ch, ci) => {
    const start = f;
    f += ch.card_frames;
    const cardEnd = f;
    for (const s of ch.scenes) { scenes.push({ chapter: ci, start: f, end: f + s.frames, id: s.id }); f += s.frames; }
    chapters.push({ start, cardEnd, end: f });
  });
  return { chapters, scenes, total: f };
}

const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ease = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); }; // smoothstep

export class Editor {
  readonly ctx: CanvasRenderingContext2D;
  readonly lay: ReturnType<typeof layout>;
  /** `scale`: physical pixels per layout pixel (2 renders the 1920x1080 layout at 3840x2160). */
  constructor(readonly canvas: HTMLCanvasElement, readonly p: Program, readonly scale = 1) {
    canvas.width = p.width * scale; canvas.height = p.height * scale;
    this.ctx = canvas.getContext('2d', { willReadFrequently: true })!;
    this.ctx.setTransform(scale, 0, 0, scale, 0, 0);
    this.lay = layout(p);
  }

  private progressBar(fraction: number, current: number, y = 0, h = 5, alpha = 1) {
    const c = this.ctx, W = this.p.width, total = this.lay.total;
    c.globalAlpha = alpha;
    c.fillStyle = C.track; c.fillRect(0, y, W, h);
    c.fillStyle = C.gold; c.fillRect(0, y, Math.round(W * fraction), h);
    this.lay.chapters.forEach((ch, i) => {   // a tick at every chapter start; the current chapter's tick is cyan
      const x = Math.round((W * ch.start) / total);
      c.fillStyle = i === current ? C.cyan : C.muted;
      c.fillRect(Math.max(0, x - 1), y, 2, h + 4);
    });
    c.globalAlpha = 1;
  }

  /** Overlay for scene number `si` (0-based over the whole program): transparent except the HUD. */
  hud(si: number) {
    const c = this.ctx, W = this.p.width, H = this.p.height;
    c.clearRect(0, 0, W, H);
    const s = this.lay.scenes[si]!;
    const ch = this.p.chapters[s.chapter]!;
    this.progressBar(s.start / this.lay.total, s.chapter);
    c.font = '22px "EB Garamond"';
    c.fillStyle = C.muted;
    c.textAlign = 'right'; c.textBaseline = 'alphabetic';
    c.fillText(`${ch.part} · ${ch.title}`, W - 28, 36);
  }

  /** Frame k (0-based) of chapter `ci`'s title card: opaque. */
  card(ci: number, k: number) {
    const c = this.ctx, W = this.p.width, H = this.p.height, fps = this.p.fps;
    const ch = this.p.chapters[ci]!;
    const t = k / fps, T = ch.card_frames / fps;
    const fadeIn = ease(t / 0.6), fadeOut = 1 - ease((t - (T - 0.6)) / 0.6);
    const a = Math.min(fadeIn, fadeOut);
    c.globalAlpha = 1;
    c.fillStyle = C.bg; c.fillRect(0, 0, W, H);
    // part label: tracked small capitals in gold
    c.globalAlpha = a;
    c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    c.fillStyle = C.gold;
    c.font = '34px "EB Garamond Medium"';
    const label = ch.part.toUpperCase().split('').join(' ');
    c.fillText(label, W / 2, H / 2 - 96);
    // title: calligraphic, rising 18 px as it fades in
    const rise = (1 - ease(t / 0.9)) * 18;
    c.font = '108px "TeX Gyre Chorus"';
    c.fillStyle = C.gold;
    c.fillText(ch.title, W / 2, H / 2 + 20 + rise);
    // a gold rule that grows from the centre
    const rw = 620 * ease((t - 0.25) / 0.9);
    const g = c.createLinearGradient(W / 2 - rw / 2, 0, W / 2 + rw / 2, 0);
    g.addColorStop(0, 'rgba(233,185,91,0)'); g.addColorStop(0.5, C.gold); g.addColorStop(1, 'rgba(233,185,91,0)');
    c.fillStyle = g; c.fillRect(W / 2 - rw / 2, H / 2 + 62, rw, 2);
    // where we are: chapter number and scene count
    c.font = 'italic 28px "EB Garamond"';
    c.fillStyle = C.muted;
    const n = this.p.chapters.length;
    c.fillText(`chapter ${ci + 1} of ${n}  ·  ${ch.scenes.length} scenes`, W / 2, H / 2 + 128);
    c.globalAlpha = 1;
    // the programme's progress bar, as in every scene, fading with the card
    this.progressBar(this.lay.chapters[ci]!.start / this.lay.total, ci, 0, 5, a);
  }

  rgba(): Uint8ClampedArray { return this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height).data; }
}
