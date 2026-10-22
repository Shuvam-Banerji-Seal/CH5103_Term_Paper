// Slide viewer: PDF.js renders one page at a time, fitted to the stage. URL: slides.html?deck=full#42
(() => {
  "use strict";
  const DECKS = { handout: "pdf/ch5103-handout.pdf", full: "pdf/ch5103-presentation.pdf" };
  const $ = (id) => document.getElementById(id);
  const canvas = $("page"), ctx = canvas.getContext("2d"), stage = $("stage"), msg = $("msg");
  const lib = window.pdfjsLib;
  if (!lib) { msg.textContent = "The PDF viewer could not load. Download the slides instead (link above)."; return; }
  lib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  const params = new URLSearchParams(location.search);
  let deck = params.get("deck") === "full" ? "full" : "handout";
  let pdf = null, num = 1, busy = false, again = false, sections = [];

  const pageFromHash = () => { const n = parseInt(location.hash.replace(/^#(page=)?/, ""), 10); return n > 0 ? n : 1; };

  async function resolveSections(doc) {
    const out = [];
    const outline = (await doc.getOutline()) || [];
    for (const item of outline) {
      try {
        const dest = typeof item.dest === "string" ? await doc.getDestination(item.dest) : item.dest;
        if (!dest) continue;
        const idx = typeof dest[0] === "object" ? await doc.getPageIndex(dest[0]) : dest[0];
        out.push({ title: item.title, page: idx + 1 });
      } catch (_) { /* skip unresolvable entries */ }
    }
    return out.sort((a, b) => a.page - b.page);
  }

  function fillJump() {
    const sel = $("jump");
    sel.length = 1;
    sections.forEach((s, i) => { const o = document.createElement("option"); o.value = String(i); o.textContent = s.title; sel.append(o); });
    sel.disabled = sections.length === 0;
  }
  const sectionIndexOf = (n) => { let k = -1; sections.forEach((s, i) => { if (s.page <= n) k = i; }); return k; };

  async function load(which, startPage, keepSection) {
    deck = which;
    document.querySelectorAll(".seg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.deck === deck)));
    $("dl").href = DECKS[deck];
    msg.textContent = "Loading slides…"; msg.hidden = false;
    try {
      const prevSections = sections;
      pdf = await lib.getDocument({ url: DECKS[deck] }).promise;
      sections = await resolveSections(pdf);
      fillJump();
      $("total").textContent = pdf.numPages;
      $("num").max = pdf.numPages;
      let target = startPage;
      if (keepSection != null && keepSection >= 0 && sections[keepSection] && prevSections.length === sections.length) target = sections[keepSection].page;
      go(target);
    } catch (e) {
      msg.textContent = "Could not load the slides. Try the download link above.";
      console.error(e);
    }
  }

  function go(n) {
    if (!pdf) return;
    num = Math.min(pdf.numPages, Math.max(1, n | 0));
    $("num").value = num;
    $("prev").disabled = $("first").disabled = num <= 1;
    $("next").disabled = $("last").disabled = num >= pdf.numPages;
    $("prog").style.width = (pdf.numPages > 1 ? ((num - 1) / (pdf.numPages - 1)) * 100 : 100) + "%";
    const k = sectionIndexOf(num);
    $("jump").value = k >= 0 ? String(k) : "";
    const url = new URL(location.href);
    if (deck === "full") url.searchParams.set("deck", "full"); else url.searchParams.delete("deck");
    url.hash = String(num);
    history.replaceState(null, "", url);
    render();
  }

  async function render() {
    if (!pdf) return;
    if (busy) { again = true; return; } // one render at a time on the canvas; re-run once it finishes
    busy = true; again = false;
    const want = num;
    const page = await pdf.getPage(want);
    const box = stage.getBoundingClientRect();
    const base = page.getViewport({ scale: 1 });
    const scale = Math.max(0.1, Math.min((box.width - 16) / base.width, (box.height - 16) / base.height));
    const dpr = Math.min(window.devicePixelRatio || 1, 3);
    const vp = page.getViewport({ scale: scale * dpr });
    canvas.width = Math.floor(vp.width); canvas.height = Math.floor(vp.height);
    canvas.style.width = Math.floor(vp.width / dpr) + "px"; canvas.style.height = Math.floor(vp.height / dpr) + "px";
    try { await page.render({ canvasContext: ctx, viewport: vp }).promise; msg.hidden = true; }
    catch (e) { console.error(e); }
    canvas.setAttribute("aria-label", `Slide page ${want} of ${pdf.numPages}`);
    busy = false;
    if (again || want !== num) { render(); return; }
    if (want < pdf.numPages) pdf.getPage(want + 1); // warm the next page
  }

  // ---------------------------------------------------------------- controls
  $("prev").onclick = () => go(num - 1);
  $("next").onclick = () => go(num + 1);
  $("first").onclick = () => go(1);
  $("last").onclick = () => go(pdf ? pdf.numPages : 1);
  document.querySelector(".nav-zone.prev").onclick = () => go(num - 1);
  document.querySelector(".nav-zone.next").onclick = () => go(num + 1);
  $("num").addEventListener("change", (e) => go(parseInt(e.target.value, 10) || 1));
  $("jump").addEventListener("change", (e) => { const s = sections[parseInt(e.target.value, 10)]; if (s) go(s.page); });
  document.querySelectorAll(".seg button").forEach((b) => b.addEventListener("click", () => {
    if (b.dataset.deck !== deck) load(b.dataset.deck, 1, sectionIndexOf(num));
  }));
  const fullscreen = () => {
    const v = $("viewer");
    if (document.fullscreenElement) document.exitFullscreen(); else if (v.requestFullscreen) v.requestFullscreen();
  };
  $("fs").onclick = fullscreen;
  document.addEventListener("fullscreenchange", () => setTimeout(render, 60));
  document.addEventListener("keydown", (e) => {
    if ((e.target instanceof Element && e.target.closest("input, select, textarea")) || e.altKey || e.ctrlKey || e.metaKey) return;
    const k = e.key;
    if (k === "ArrowRight" || k === "PageDown" || k === " " || k === "ArrowDown") { e.preventDefault(); go(num + (e.shiftKey && k === " " ? -1 : 1)); }
    else if (k === "ArrowLeft" || k === "PageUp" || k === "ArrowUp" || k === "Backspace") { e.preventDefault(); go(num - 1); }
    else if (k === "Home") { e.preventDefault(); go(1); }
    else if (k === "End") { e.preventDefault(); go(pdf ? pdf.numPages : 1); }
    else if (k === "f" || k === "F") { fullscreen(); }
  });
  let x0 = null;
  stage.addEventListener("pointerdown", (e) => { if (e.pointerType !== "mouse") x0 = e.clientX; });
  stage.addEventListener("pointerup", (e) => {
    if (x0 == null) return;
    const dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) go(num + (dx < 0 ? 1 : -1));
  });
  let rt = null;
  new ResizeObserver(() => { clearTimeout(rt); rt = setTimeout(render, 120); }).observe(stage);
  window.addEventListener("hashchange", () => { const n = pageFromHash(); if (n !== num) go(n); });

  load(deck, pageFromHash(), null);
})();
