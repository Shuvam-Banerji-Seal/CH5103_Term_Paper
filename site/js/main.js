// CH5103 site: math rendering, derivation cards, test matrix, distonic chart, figure gallery.
(() => {
  "use strict";
  const REPO = "https://github.com/Shuvam-Banerji-Seal/CH5103_Term_Paper/blob/main/";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, attrs = {}, html = "") => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    if (html) el.innerHTML = html;
    return el;
  };
  const tex = (el) => {
    if (window.renderMathInElement) {
      window.renderMathInElement(el, {
        delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
        throwOnError: false,
      });
    }
  };

  // ------------------------------------------------------------------ derivations (section numbers as in the PDF)
  const DERIV = [
    [0, "Conventions", "Atomic units, chemists' notation for integrals \\((pq|rs)\\), spin-orbital conventions."],
    [1, "Antisymmetry and two-electron spin functions", "Exchange eigenvalue \\(\\pm1\\); the four spin functions are eigenfunctions of \\(\\hat S^2\\) and \\(\\hat S_z\\)."],
    [2, "Two electrons in two orbitals (Figure 1)", "Six determinants; \\(M_S=0\\) needs two of them; the open-shell singlet is \\(\\tfrac12(D_{iv}-D_{iii})\\)."],
    [3, "Energies and the 2e/2o Hamiltonian", "\\(E_{\\text{OSS}}-E_T=2K_{ab}\\); the full singlet matrix, checked against full CI."],
    [4, "Fermi and Coulomb holes", "Pair densities of singlet and triplet; \\(K_{ab}\\ge0\\) and \\(J_{ab}\\ge K_{ab}\\) proved."],
    [5, "Hund's rule and the virial theorem", "Frozen orbitals cannot satisfy the virial theorem; the triplet wins on nuclear attraction (He, exact)."],
    [6, "Static correlation", "H₂: the RHF error tends to \\(U/2\\) on dissociation; the weak-interaction limit of Figure 2."],
    [7, "Kinetic exchange", "\\(E_S-E_T\\approx 2k-4t^2/(U-V)\\): ionic configurations mix only into the singlet."],
    [8, "NBMOs and disjointness", "Disjoint NBMOs give \\(K\\approx0\\); #NBMO \\(\\ge N-2T\\) (Longuet-Higgins)."],
    [9, "Spin polarisation, Ovchinnikov, Lieb", "\\(S=\\tfrac12|n_A-n_B|\\); the S–T gap scales as \\(U^2\\) for disjoint diradicals."],
    [10, "Koopmans and Janak", "\\(\\partial E/\\partial n_i=\\varepsilon_i\\); the S–T gap equals a HOMO-energy difference, \\(2K\\)."],
    [11, "Quasi-closed-shell radicals", "UHF \\(\\alpha/\\beta\\) splitting \\(K_{hs}\\); SOMO below HOMO iff \\(h_s+J_{hs}&lt;h_h+J_{hh}\\); the DFT test."],
    [12, "ROHF canonicalisation", "Diagonal Fock blocks are arbitrary: the orbital order is a convention."],
    [13, "The 3d/4s problem", "\\(\\Delta=(\\varepsilon_d-\\varepsilon_s)+(\\bar J_{dd}-\\bar J_{ds})\\): filling and ionisation orders differ."],
    [14, "Quantum numbers of single electrons", "\\([\\hat l_{1z},r_{12}^{-1}]\\ne0\\) but \\([\\hat L_z,r_{12}^{-1}]=0\\)."],
    [15, "The adiabatic principle", "Why adding an electron has no continuous adiabatic path."],
    [16, "Broken symmetry and spin projection", "Yamaguchi: \\(J=(E_{\\text{BS}}-E_{\\text{HS}})/(\\langle S^2\\rangle_{\\text{HS}}-\\langle S^2\\rangle_{\\text{BS}})\\)."],
    [17, "Summary and sources", "Verification record, corrections, and the access status of every cited source."],
  ];
  const dg = $("#deriv-grid");
  for (const [n, title, body] of DERIV) {
    dg.append(h("div", { class: "panel" }, `<div class="sec">§${n}</div><h3>${title}</h3><p>${body}</p>`));
  }

  // ------------------------------------------------------------------ test matrix
  const PILL = { ok: '<span class="pill ok">pass</span>', fail: '<span class="pill bad">fail</span>', hand: '<span class="pill info">by hand</span>' };
  const res = (f) => `<a href="data/results/${f}.txt">output</a>`;
  const src = (p, label) => `<a href="${REPO}${p}">${label}</a>`;
  const TESTS = [
    ["T1", "spin functions, Figure 1 combinations, the sign erratum", "SymPy", "ok", [src("verification/t01_spin_and_determinants.py", "script"), res("t01_spin_and_determinants")]],
    ["T1b", "sign erratum again: \\(\\hat S^2\\) on numerical two-electron tensors", "NumPy", "ok", [src("verification/t01b_sign_error_numeric.py", "script"), res("t01b_sign_error_numeric")]],
    ["T2", "2e/2o Hamiltonian vs full CI, 5 random integral sets", "PySCF FCI", "ok", [src("verification/t02_two_orbital_hamiltonian.py", "script"), res("t02_two_orbital_hamiltonian")]],
    ["T3", "\\(K_{pq}\\ge0\\), \\(J_{pq}\\ge K_{pq}\\) for water MOs", "RHF/6-31G", "ok", [src("verification/t03_t05_hund_virial_h2.py", "script"), res("t03_t05_hund_virial_h2")]],
    ["T4", "He \\(2\\,{}^3S/2\\,{}^1S\\): virial theorem, less screening", "exact, 16s7p4d basis", "ok", [src("verification/t03_t05_hund_virial_h2.py", "script"), res("t03_t05_hund_virial_h2")]],
    ["T5", "H₂ minimal basis: closed forms and dissociation limits", "STO-3G vs PySCF", "ok", [src("verification/t03_t05_hund_virial_h2.py", "script"), res("t03_t05_hund_virial_h2")]],
    ["T6", "two-orbital gap model", "SymPy", "ok", [src("verification/t06_t09_models.py", "script"), res("t06_t09_models")]],
    ["T7", "kinetic exchange in the extended Hubbard dimer", "SymPy + FCI", "ok", [src("verification/t06_t09_models.py", "script"), res("t06_t09_models")]],
    ["T8", "Hückel NBMO rules, disjointness", "NumPy", "ok", [src("verification/t06_t09_models.py", "script"), res("t06_t09_models")]],
    ["T9", "Ovchinnikov/Lieb ground-state spins for 7 graphs; spin alternation", "exact diagonalisation", "ok", [src("verification/t06_t09_models.py", "script"), res("t06_t09_models")]],
    ["T9b", "S–T gap \\(\\propto U\\) (nondisjoint) vs \\(\\propto U^2\\) (disjoint)", "exact diagonalisation", "ok", [src("verification/t09b_t15_correlation.py", "script"), res("t09b_t15_correlation")]],
    ["T10", "S–T gap equals the HOMO-energy difference", "SymPy", "ok", [src("verification/t10_t12_t13_symbolic.py", "script"), res("t10_t12_t13_symbolic")]],
    ["T11a", "ROHF stationarity blocks; canonicalisation dependence", "ROHF/6-31G*", "ok", [src("verification/t11_rohf_and_distonic.py", "script"), src("verification/logs/t11.log", "log")]],
    ["T11b", "distonic radical anion, pH switch with B3LYP", "UB3LYP ΔSCF", "fail", [src("verification/t11_rohf_and_distonic.py", "script"), src("verification/logs/t11.log", "log")]],
    ["T11c", "distonic anions and acids, B3LYP vs CAM-B3LYP", "UKS ΔSCF", "ok", [src("verification/t11c_distonic_functionals.py", "script"), res("t11c_check")]],
    ["T12", "the 3d/4s identity", "SymPy", "ok", [src("verification/t10_t12_t13_symbolic.py", "script"), res("t10_t12_t13_symbolic")]],
    ["T13", "\\([\\hat l_1,r_{12}^{-1}]\\ne0\\), \\([\\hat L,r_{12}^{-1}]=0\\)", "SymPy", "ok", [src("verification/t10_t12_t13_symbolic.py", "script"), res("t10_t12_t13_symbolic")]],
    ["T14", "Yamaguchi projection on the BS-UHF Hubbard dimer", "NumPy", "ok", [src("verification/t06_t09_models.py", "script"), res("t06_t09_models")]],
    ["T15", "same- vs opposite-spin correlation", "MP2, He + molecules", "ok", [src("verification/t09b_t15_correlation.py", "script"), res("t09b_t15_correlation")]],
    ["T16", "citations against publisher records (Katriel–Pauncz 1977, Lieb 1989, Hongo 2004)", "manual", "hand", [src("docs/VERIFICATION.md", "notes")]],
    ["T17", "17 algebraic theorems", "Lean 4 + Mathlib", "ok", [src("verification/lean_proofs/Ch5103/Identities.lean", "proofs")]],
  ];
  const tb = $("#test-rows");
  for (const [id, what, method, st, files] of TESTS) {
    tb.append(h("tr", {}, `<td class="id">${id}</td><td>${what}</td><td>${method}</td><td>${PILL[st]}</td><td>${files.join(" · ")}</td>`));
  }

  // ------------------------------------------------------------------ Lean theorem names
  const LEAN = ["sum_is_triplet", "diff_is_singlet", "erratum_plus_is_not_singlet", "gap_frozen", "gap_as_homo_difference",
    "scaling_derivative", "virial_consequences", "less_screening", "frozen_orbitals_violate_virial", "ci_equal_diagonals",
    "h2_limits", "gap_model_root", "dimer_singlet_root", "dimer_gap", "pairing", "three_d_four_s", "yamaguchi"];
  $("#lean-names").innerHTML = "All 17: " + LEAN.map((n) => `<code>${n}</code>`).join(", ") +
    `. Source: ${src("verification/lean_proofs/Ch5103/Identities.lean", "Identities.lean")}.`;

  // ------------------------------------------------------------------ distonic chart
  const LABELS = { shortacid: "short acid", shortanion: "short anion", tempoacid: "TEMPO acid", tempoanion: "TEMPO anion" };
  const FALLBACK = [ // presentation/data/distonic.csv (T11c)
    { system: "shortacid", b3lyp: 1.406, camb3lyp: 1.421 }, { system: "shortanion", b3lyp: 0.072, camb3lyp: -0.363 },
    { system: "tempoacid", b3lyp: 1.285, camb3lyp: 1.229 }, { system: "tempoanion", b3lyp: 0.067, camb3lyp: -0.296 },
  ];
  const SERIES = [
    { key: "b3lyp", name: "B3LYP", color: "var(--series-b3lyp)" },
    { key: "camb3lyp", name: "CAM-B3LYP", color: "var(--series-cam)" },
  ];
  const tip = $("#tip");
  const showTip = (html, x, y) => {
    tip.innerHTML = html; tip.classList.add("on");
    const r = tip.getBoundingClientRect();
    tip.style.left = Math.min(window.innerWidth - r.width - 8, Math.max(8, x - r.width / 2)) + "px";
    tip.style.top = Math.max(8, y - r.height - 12) + "px";
  };
  const hideTip = () => tip.classList.remove("on");

  const fmt = (v, d = 3) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d);
  function drawChart(rows) {
    const svg = $("#chart"), NS = "http://www.w3.org/2000/svg";
    const W = 560, H = 350, m = { l: 54, r: 8, t: 40, b: 44 };
    const y0 = -0.6, y1 = 1.6, py = (v) => m.t + (y1 - v) / (y1 - y0) * (H - m.t - m.b);
    const band = (W - m.l - m.r) / rows.length, bw = 24, gap = 2;
    const el = (tag, attrs, text) => {
      const e = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (text != null) e.textContent = text;
      svg.append(e); return e;
    };
    for (const v of [-0.5, 0, 0.5, 1, 1.5]) {
      if (v !== 0) el("line", { class: "grid", x1: m.l, x2: W - m.r, y1: py(v), y2: py(v) });
      el("text", { x: m.l - 8, y: py(v) + 4, "text-anchor": "end" }, (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(1));
    }
    const ttl = el("text", { x: 4, y: 18 });
    ttl.innerHTML = 'Δ = E<tspan baseline-shift="sub" font-size="12">T</tspan> − E<tspan baseline-shift="sub" font-size="12">CS</tspan> (eV)';
    el("text", { class: "zone", x: W - m.r - 4, y: py(1.6) + 12, "text-anchor": "end" }, "↑ closed shell lower");
    el("text", { class: "zone", x: W - m.r - 4, y: py(-0.6) - 6, "text-anchor": "end" }, "↓ diradical lower");
    rows.forEach((row, i) => {
      const cx = m.l + band * (i + 0.5);
      el("text", { x: cx, y: H - m.b + 26, "text-anchor": "middle" }, LABELS[row.system] || row.system);
      SERIES.forEach((s, j) => {
        const v = row[s.key], x = cx + (j === 0 ? -bw - gap / 2 : gap / 2);
        const yv = py(v), yz = py(0), top = Math.min(yv, yz), hgt = Math.max(1, Math.abs(yz - yv)), r = Math.min(4, hgt);
        // 4px rounded data-end, square at the baseline
        const d = v >= 0
          ? `M${x},${yz}V${top + r}Q${x},${top} ${x + r},${top}H${x + bw - r}Q${x + bw},${top} ${x + bw},${top + r}V${yz}Z`
          : `M${x},${yz}V${yv - r}Q${x},${yv} ${x + r},${yv}H${x + bw - r}Q${x + bw},${yv} ${x + bw},${yv - r}V${yz}Z`;
        const g = document.createElementNS(NS, "g");
        g.setAttribute("class", "bar"); g.setAttribute("tabindex", "0");
        const label = `${LABELS[row.system]}, ${s.name}: ${fmt(v)} eV`;
        g.setAttribute("aria-label", label);
        const p = document.createElementNS(NS, "path");
        p.setAttribute("d", d); p.setAttribute("class", "mark"); p.setAttribute("style", `fill:${s.color}`);
        const hit = document.createElementNS(NS, "rect"); // hit target larger than the mark
        hit.setAttribute("x", x - 3); hit.setAttribute("width", bw + 6);
        hit.setAttribute("y", Math.min(top, yz) - 8); hit.setAttribute("height", hgt + 16); hit.setAttribute("fill", "transparent");
        g.append(hit, p); svg.append(g);
        const html = `<span class="sw" style="background:${s.color}"></span><b>${s.name}</b><br>${LABELS[row.system]}: ` +
          `${fmt(v)} eV<br><span style="color:var(--muted)">${v < 0 ? "diradical lower" : "closed shell lower"}</span>`;
        const at = (e) => { const b = g.getBoundingClientRect(); showTip(html, e && e.clientX ? e.clientX : b.left + b.width / 2, b.top); };
        g.addEventListener("pointerenter", at); g.addEventListener("pointermove", at);
        g.addEventListener("pointerleave", hideTip); g.addEventListener("focus", () => at()); g.addEventListener("blur", hideTip);
        if (row.system.endsWith("anion")) { // selective direct labels: the decision-relevant bars only
          el("text", { class: "val", x: x + bw / 2, y: v >= 0 ? yv - 6 : yv + 15, "text-anchor": "middle" },
            fmt(v, 2));
        }
      });
    });
    el("line", { class: "zero", x1: m.l, x2: W - m.r, y1: py(0), y2: py(0) });
    const tbody = $("#chart-table tbody");
    for (const row of rows) {
      tbody.append(h("tr", {}, `<td>${LABELS[row.system]}</td><td class="num">${fmt(row.b3lyp)}</td><td class="num">${fmt(row.camb3lyp)}</td>`));
    }
  }
  fetch("data/distonic.csv").then((r) => (r.ok ? r.text() : Promise.reject()))
    .then((t) => t.trim().split(/\r?\n/).slice(1).map((l) => { const [system, b, c] = l.split(","); return { system, b3lyp: +b, camb3lyp: +c }; }))
    .then((rows) => (rows.length === 4 && rows.every((r) => isFinite(r.b3lyp) && isFinite(r.camb3lyp)) ? rows : FALLBACK))
    .catch(() => FALLBACK)
    .then(drawChart);

  // ------------------------------------------------------------------ figure gallery
  const gal = $("#gallery"), lb = $("#lightbox");
  const openFig = (f) => {
    $("#lb-img").src = f.file; $("#lb-img").alt = `${f.label} of the review`;
    $("#lb-title").textContent = `${f.label} · p. ${f.journal_page}`;
    $("#lb-cap").textContent = f.caption;
    if (lb.showModal) lb.showModal(); else window.open(f.file, "_blank");
  };
  $(".close", lb).addEventListener("click", () => lb.close());
  lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  fetch("data/figures.jsonl").then((r) => r.text()).then((t) => {
    const figs = t.trim().split(/\r?\n/).map((l) => JSON.parse(l));
    for (const f of figs) {
      const b = h("button", { type: "button", class: "fig", "data-type": f.type });
      b.innerHTML = `<div class="img"><img loading="lazy" width="400" height="300" src="${f.file}" alt="${f.label} of the review"></div>` +
        `<div class="cap"><b>${f.label}</b><span></span></div>`;
      $(".cap span", b).textContent = f.caption;
      b.addEventListener("click", () => openFig(f));
      gal.append(b);
    }
  }).catch(() => { gal.innerHTML = '<p class="muted">The figure list could not be loaded.</p>'; });
  document.querySelectorAll(".filters button").forEach((btn) => btn.addEventListener("click", () => {
    document.querySelectorAll(".filters button").forEach((o) => o.setAttribute("aria-pressed", String(o === btn)));
    const f = btn.dataset.f;
    gal.querySelectorAll(".fig").forEach((c) => { c.hidden = !(f === "all" || c.dataset.type === f); });
  }));

  // ------------------------------------------------------------------ nav highlight + progress
  const links = [...document.querySelectorAll('.nav a[href^="#"]')];
  const secs = links.map((a) => document.getElementById(a.getAttribute("href").slice(1))).filter(Boolean);
  const bar = $(".progress i");
  const onScroll = () => {
    const y = window.scrollY + 90;
    let cur = null;
    for (const s of secs) if (s.offsetTop <= y) cur = s.id;
    links.forEach((a) => a.setAttribute("aria-current", String(a.getAttribute("href") === "#" + cur)));
    const max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ------------------------------------------------------------------ build stamp (written by scripts/build_site.sh)
  fetch("data/build.json").then((r) => (r.ok ? r.json() : null)).then((b) => {
    if (!b || !b.commit) return;
    const short = b.commit.slice(0, 7), when = (b.built || "").replace("T", " ").replace("Z", " UTC");
    const commit = `<a href="https://github.com/Shuvam-Banerji-Seal/CH5103_Term_Paper/commit/${b.commit}">${short}</a>`;
    $("#build-stamp").innerHTML = ` · built from ${commit} on ${when}` + (b.run ? ` (<a href="${b.run}">CI run</a>)` : "");
  }).catch(() => {});

  // math last, once the dynamic content exists
  const renderAll = () => tex(document.body);
  if (window.renderMathInElement) renderAll(); else window.addEventListener("load", renderAll);
})();
