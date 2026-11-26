"use strict";
// Painel de Criativos: front-end sem build. Fala só com tools/painel.py (127.0.0.1).

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const app = $("#app");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const reduzMovimento = matchMedia("(prefers-reduced-motion: reduce)").matches;

const ICONE = {
  play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>',
  busca: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
  voltar: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>',
  filme: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M17 9h4M3 15h4M17 15h4"/></svg>',
  alvo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>',
  moeda: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2c-1.4 0-2.5-.5-3-1.5M12 6v2M12 16v2"/></svg>',
  lapis: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16v4z"/></svg>',
  vazio: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 9h18"/></svg>',
  refazer: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/></svg>',
  comparar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 3v18M16 3v18M3 8h5M16 16h5"/></svg>',
  filtro: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h18l-7 8v6l-4 2v-8L3 5z"/></svg>',
  mais: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
  chave: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/></svg>',
  link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
  fechar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
};

// ------------------------------------------------------------ preferências do navegador
const prefs = {
  get(k, d) { try { const v = localStorage.getItem("painel." + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("painel." + k, JSON.stringify(v)); } catch { /* sem storage */ } },
};
let EU = null;                       // usuário logado (/api/eu)
const autor = () => (EU ? EU.nome : "");

// ------------------------------------------------------------ API
async function api(path, body) {
  const opt = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const r = await fetch(path, opt);
  const j = await r.json().catch(() => ({}));
  if (r.status === 401 && j.login) { location.href = "/login"; throw new Error("Sessão expirada."); }
  if (body !== undefined) sujarTudo();          // gravou (ou tentou): as próximas leituras vão ao servidor
  if (!r.ok || j.erro) throw new Error(j.erro || `Erro ${r.status}`);
  return j;
}

// Nome de exibição: "Criativo #05" (o ID C05 continua por baixo).
const nomeC = (id) => (id ? "Criativo #" + String(id).replace(/^C/, "") : "");
let toastT;
function toast(msg, ms = 4000) {
  const t = $("#toast"); t.textContent = msg; t.hidden = false;
  t.style.animation = "none"; void t.offsetWidth; t.style.animation = "";
  clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), ms);
}

// ------------------------------------------------------------ pop-up (todo cadastro abre aqui)
// modal({ titulo, sub, corpo, botao, aoSalvar(dados, form) }): aoSalvar pode lançar Error, que aparece
// dentro do pop-up sem fechá-lo. Esc, ✕, Cancelar ou clique fora fecham.
const campo = (rot, html, cls = "") => `<label class="${cls}">${rot}${html}</label>`;
function modal({ titulo, sub = "", corpo, botao = "Salvar", aoSalvar, aoAbrir, largo = false, cancelar = "Cancelar" }) {
  const dl = document.createElement("dialog");
  dl.className = "modal" + (largo ? " largo" : "");
  dl.innerHTML = `<form class="modal-caixa" novalidate>
      <div class="modal-cabeca"><div><h3>${titulo}</h3>${sub ? `<p>${sub}</p>` : ""}</div>
        <button type="button" class="fechar" data-fechar aria-label="Fechar">${ICONE.fechar}</button></div>
      <div class="modal-corpo">${corpo}</div>
      <div class="modal-erro" hidden></div>
      <div class="modal-pe"><button type="button" class="btn fantasma" data-fechar>${cancelar}</button>${aoSalvar ? `<button type="submit" class="btn primario">${botao}</button>` : ""}</div>
    </form>`;
  document.body.append(dl);
  const form = $("form", dl), erro = $(".modal-erro", dl);
  const fechar = () => { if (dl.open) dl.close(); };
  dl.addEventListener("close", () => dl.remove());
  $$("[data-fechar]", dl).forEach((b) => b.addEventListener("click", fechar));
  let fora = false; // só fecha se o clique começou e terminou no fundo (não ao arrastar seleção de texto)
  dl.addEventListener("mousedown", (e) => (fora = e.target === dl));
  dl.addEventListener("click", (e) => { if (fora && e.target === dl) fechar(); });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!aoSalvar) return fechar();
    const dados = {};
    $$("[name]", form).forEach((i) => (dados[i.name] = i.type === "checkbox" ? i.checked : i.type === "password" ? i.value : i.value.trim()));
    const btn = $('button[type="submit"]', form);
    btn.disabled = true; erro.hidden = true;
    try { await aoSalvar(dados, form); fechar(); }
    catch (er) { erro.textContent = er.message; erro.hidden = false; btn.disabled = false; }
  });
  dl.showModal();
  aoAbrir && aoAbrir(form);
  const primeiro = $(".modal-corpo input:not([readonly]):not([type=hidden]), .modal-corpo select, .modal-corpo textarea", dl);
  primeiro && primeiro.focus();
  return dl;
}

// ------------------------------------------------------------ formatação
let MOEDA = "EUR";
const nf = (d) => new Intl.NumberFormat("pt-BR", { maximumFractionDigits: d, minimumFractionDigits: d });
const F = {
  int: (v) => (v == null ? "–" : nf(0).format(v)),
  money: (v) => (v == null ? "–" : new Intl.NumberFormat("pt-BR", { style: "currency", currency: MOEDA }).format(v)),
  pct: (v) => (v == null ? "–" : nf(1).format(v * 100) + "%"),
  x: (v) => (v == null ? "–" : nf(2).format(v) + "x"),
};
const METRICAS = [
  { k: "compras", rot: "Compras", f: "int", melhor: "alto" },
  { k: "roas", rot: "ROAS", f: "x", melhor: "alto" },
  { k: "cpa", rot: "Custo por compra", f: "money", melhor: "baixo" },
  { k: "gasto", rot: "Gasto", f: "money" },
  { k: "impressoes", rot: "Impressões", f: "int" },
  { k: "ctr", rot: "CTR do link", f: "pct", melhor: "alto" },
  { k: "gancho", rot: "Gancho (3 s)", f: "pct", melhor: "alto" },
  { k: "thruplay", rot: "Thruplay", f: "pct", melhor: "alto" },
  { k: "retencao50", rot: "Retenção 50%", f: "pct", melhor: "alto" },
  { k: "cpm", rot: "CPM", f: "money", melhor: "baixo" },
];
function compara(v, media, melhor) {
  if (v == null || media == null || !melhor || media === 0) return { cls: "", seta: "", txt: "" };
  const d = v / media - 1;
  if (Math.abs(d) < 0.005) return { cls: "", seta: "=", txt: "= média" };
  const bom = melhor === "alto" ? d > 0 : d < 0;
  return { cls: bom ? "melhor" : "pior", seta: d > 0 ? "▲" : "▼", txt: `${d > 0 ? "▲" : "▼"} ${nf(0).format(Math.abs(d) * 100)}%` };
}
const tempo = (s) => {
  if (s == null) return "peça";
  const m = Math.floor(s / 60), r = s - m * 60;
  return `${m}:${r.toFixed(1).padStart(4, "0")}`;
};
const STATUS = { em_producao: "em produção", entregue: "entregue", no_ar: "no ar", pausado: "pausado", descartado: "descartado" };
const ETAPAS = ["fila", "analise", "roteiro", "imagens", "takes", "montagem", "revisao"];
const ROT_ETAPA = { fila: "Fila", analise: "Análise", roteiro: "Roteiro", imagens: "Imagens", takes: "Takes", montagem: "Montagem", revisao: "Revisão" };
const rotEtapa = (e, tipo) => (tipo && tipo !== "video" ? { roteiro: "Texto", imagens: "Imagem" }[e] : null) || ROT_ETAPA[e] || e;
const diasDesde = (s) => (s ? Math.max(0, Math.floor((Date.now() - new Date(s)) / 864e5)) : null);
const ha = (s) => { const d = diasDesde(s); return d == null ? "" : d === 0 ? "hoje" : d === 1 ? "há 1 dia" : `há ${d} dias`; };
const usd = (v) => (v ? "US$ " + nf(2).format(v) : "");

// Markdown simples (títulos, tabelas, listas, citações, negrito, código) para os documentos da pasta.
function md(src) {
  const L = String(src || "").replace(/\r/g, "").split("\n");
  const inl = (t) => esc(t)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:!?]|$)/g, "$1<i>$2</i>")
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, u) => (/^https?:/.test(u) ? `<a href="${u}" target="_blank" rel="noopener">${t}</a>` : `<span class="lk" title="${u}">${t}</span>`));
  const celulas = (l) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
  let out = "", i = 0;
  while (i < L.length) {
    const l = L[i];
    if (!l.trim()) { i++; continue; }
    let m;
    if ((m = l.match(/^(#{1,4})\s+(.*)/))) { out += `<h${m[1].length + 1}>${inl(m[2])}</h${m[1].length + 1}>`; i++; continue; }
    if (/^\s*(-{3,}|\*{3,})\s*$/.test(l)) { out += "<hr>"; i++; continue; }
    if (l.trim().startsWith("|") && L[i + 1] && /^\s*\|?\s*:?-{2,}/.test(L[i + 1])) {
      const cab = celulas(l); i += 2; const rows = [];
      while (i < L.length && L[i].trim().startsWith("|")) rows.push(celulas(L[i++]));
      out += `<div class="md-tabela"><table><thead><tr>${cab.map((c) => `<th>${inl(c)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${inl(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
      continue;
    }
    if (/^\s*([-*]|\d+\.)\s+/.test(l)) {
      const ord = /^\s*\d+\./.test(l); const itens = [];
      while (i < L.length && /^\s*([-*]|\d+\.)\s+/.test(L[i])) itens.push(L[i++].replace(/^\s*([-*]|\d+\.)\s+/, ""));
      out += `<${ord ? "ol" : "ul"}>${itens.map((x) => `<li>${inl(x)}</li>`).join("")}</${ord ? "ol" : "ul"}>`;
      continue;
    }
    if (l.startsWith(">")) {
      const q = []; while (i < L.length && L[i].startsWith(">")) q.push(L[i++].replace(/^>\s?/, ""));
      out += `<blockquote>${q.map(inl).join("<br>")}</blockquote>`; continue;
    }
    const p = []; while (i < L.length && L[i].trim() && !/^(#{1,4}\s|\||>|\s*([-*]|\d+\.)\s)/.test(L[i])) p.push(L[i++]);
    if (!p.length) p.push(L[i++]);
    out += `<p>${p.map(inl).join("<br>")}</p>`;
  }
  return `<div class="md">${out}</div>`;
}
const badgeStatus = (s) => `<span class="badge ${s}">${STATUS[s] || esc(s)}</span>`;

// ------------------------------------------------------------ miniaturas e prévia
const thumb = (arquivo, t = 1.5, w = 320) => arquivo ? `/thumb?arquivo=${encodeURIComponent(arquivo)}&t=${(+t || 0).toFixed(2)}&w=${w}` : null;
const capaDe = (c, w = 320) => c && c.capa_arquivo ? thumb(c.capa_arquivo, c.capa_video ? 1.5 : 0, w) : null;
const porId = (id) => (CACHE ? CACHE.criativos.find((c) => c.id === id) : null);
const miniImg = (c, cls = "mini") => {
  const u = capaDe(c, 120);
  return u ? `<img class="${cls}" src="${u}" loading="lazy" alt="" data-espiar="${c.id}">` : `<span class="${cls}"></span>`;
};

// Prévia flutuante: qualquer elemento com data-espiar="C05" mostra o criativo tocando ao lado do cursor.
const espiar = $("#espiar");
let espiarId = null;
document.addEventListener("mouseover", (e) => {
  const el = e.target.closest("[data-espiar]");
  if (!el) return;
  const c = porId(el.dataset.espiar);
  if (!c || espiarId === c.id) return;
  espiarId = c.id;
  const img = capaDe(c, 400);
  espiar.innerHTML = (img ? `<img src="${img}" alt="">` : "")
    + (c.capa_video && !reduzMovimento ? `<video src="${c.capa_video}#t=1.5" muted autoplay loop playsinline></video>` : "")
    + `<div class="leg">${c.id} · ${esc(c.formato || "")}</div>`;
  espiar.classList.add("on");
});
document.addEventListener("mousemove", (e) => {
  if (!espiar.classList.contains("on")) return;
  const w = 200, h = w * 16 / 9, m = 18;
  let x = e.clientX + m, y = e.clientY - h / 2;
  if (x + w > innerWidth - 8) x = e.clientX - w - m;
  y = Math.max(8, Math.min(y, innerHeight - h - 8));
  espiar.style.left = x + "px"; espiar.style.top = y + "px";
});
document.addEventListener("mouseout", (e) => {
  const el = e.target.closest("[data-espiar]");
  if (el && !el.contains(e.relatedTarget)) { espiar.classList.remove("on"); espiarId = null; setTimeout(() => !espiarId && (espiar.innerHTML = ""), 200); }
});

// Spotlight: a luz segue o cursor em toda caixa .spot (React Bits, Spotlight Card).
let rafSpot;
document.addEventListener("pointermove", (e) => {
  if (reduzMovimento) return;
  cancelAnimationFrame(rafSpot);
  rafSpot = requestAnimationFrame(() => {
    const area = e.target.closest && e.target.closest(".spot-area");
    const alvos = area ? $$(".spot", area) : (e.target.closest && e.target.closest(".spot") ? [e.target.closest(".spot")] : []);
    alvos.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.bottom < -300 || r.top > innerHeight + 300) return;
      el.style.setProperty("--mx", e.clientX - r.left + "px");
      el.style.setProperty("--my", e.clientY - r.top + "px");
    });
  });
});

// Counter: números sobem até o valor (React Bits, Counter).
function animarNumeros(raiz = app) {
  $$("[data-cont]", raiz).forEach((el) => {
    const v = +el.dataset.cont, f = F[el.dataset.f] || F.int;
    if (!isFinite(v) || reduzMovimento) { el.textContent = f(v); return; }
    const t0 = performance.now(), dur = 700;
    const passo = (t) => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = f(v * e);
      if (p < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  });
}
const numero = (v, f) => (v == null ? "–" : `<span data-cont="${v}" data-f="${f}">${F[f](0)}</span>`);

// Menu lateral: pílula que desliza até o item ativo (React Bits, Pill Nav).
function moverIndicador() {
  const a = $("#nav a.ativo"), ind = $("#indicador");
  if (!a) { ind.style.opacity = 0; return; }
  ind.style.opacity = 1; ind.style.transform = `translateY(${a.offsetTop}px)`;
}

// Controle segmentado com pílula deslizante.
function segmentado(el, valor, aoMudar) {
  const pil = document.createElement("span"); pil.className = "pilula"; el.prepend(pil);
  const marcar = (v) => {
    $$("button", el).forEach((b) => b.classList.toggle("ativo", b.dataset.v === v));
    const b = $(`button[data-v="${CSS.escape(v)}"]`, el);
    if (b) { pil.style.left = b.offsetLeft + "px"; pil.style.width = b.offsetWidth + "px"; }
  };
  el.addEventListener("click", (e) => { const b = e.target.closest("button[data-v]"); if (b) { marcar(b.dataset.v); aoMudar(b.dataset.v); } });
  requestAnimationFrame(() => marcar(valor));
}

// ------------------------------------------------------------ estado no menu
async function atualizarEstado() {
  try {
    const e = await api("/api/estado");
    $("#dot-banco").className = "dot" + (e.banco ? " ok" : "");
    $("#txt-banco").textContent = e.banco ? "conectado" : "sem banco";
    $("#dot-meta").className = "dot" + (e.meta ? " ok" : "") + (e.sync_rodando ? " pulsa" : "");
    $("#txt-meta").textContent = !e.meta ? "sem token" : e.sync_rodando ? "sincronizando…" : e.ultima_sync ? "às " + e.ultima_sync.slice(11, 16) : "pronto";
    $("#txt-meta").title = e.sync_erro ? "Último erro: " + e.sync_erro : "";
    $("#btn-sync").disabled = !e.meta || e.sync_rodando;
  } catch { /* servidor fora */ }
}
// Contador no menu: cards da Produção aguardando aprovação de alguém do time.
function atualizarContFila() {
  if (!CACHE) return;
  const n = CACHE.criativos.filter((c) => c.esteira && c.esteira.aguardando === "dono").length;
  const el = $("#cont-producao"); el.hidden = !n; el.textContent = n;
}
$("#btn-sync").addEventListener("click", async () => {
  $("#btn-sync").disabled = true; toast("Sincronizando com a Meta…", 60000);
  try { const r = await api("/api/sincronizar", { dias: 30 }); toast(`Sincronizado: ${r.anuncios} anúncios, ${r.linhas_diarias} linhas diárias.`); rota(); }
  catch (e) { toast("Falhou: " + e.message, 8000); }
  atualizarEstado();
});
setInterval(atualizarEstado, 60000);

// ------------------------------------------------------------ gráfico de retenção (SVG, mira + snap)
function pontosCurva(m, dur) {
  const c = m && m.curva; if (!c) return null;
  const p = [[0, 1]];
  if (dur && c.v3s != null && dur > 3) p.push([(3 / dur) * 100, c.v3s]);
  [["p25", 25], ["p50", 50], ["p75", 75], ["p95", 95], ["p100", 100]].forEach(([k, x]) => c[k] != null && p.push([x, c[k]]));
  return p.sort((a, b) => a[0] - b[0]);
}
function graficoRetencao(series, { dur, takes = [], marcas = [] } = {}) {
  series = series.filter((se) => se.pontos);
  const W = 640, H = 260, L = 42, R = 96, T = 14, B = 30;
  const x = (v) => L + (v / 100) * (W - L - R), y = (v) => T + (1 - v) * (H - T - B);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Curva de retenção"><defs>`;
  series.forEach((se, i) => { if (!se.ref) s += `<linearGradient id="ga${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${se.cor}" stop-opacity=".22"/><stop offset="1" stop-color="${se.cor}" stop-opacity="0"/></linearGradient>`; });
  s += `</defs>`;
  [0, 0.25, 0.5, 0.75, 1].forEach((g) => { s += `<line class="${g ? "grade-l" : "eixo"}" x1="${L}" x2="${W - R}" y1="${y(g)}" y2="${y(g)}"/><text x="${L - 8}" y="${y(g) + 4}" text-anchor="end">${g * 100}%</text>`; });
  [0, 25, 50, 75, 100].forEach((v) => { s += `<text x="${x(v)}" y="${H - 8}" text-anchor="middle">${v}%${dur ? " · " + Math.round((v / 100) * dur) + "s" : ""}</text>`; });
  if (dur) takes.slice(1).forEach((t) => { const xv = x((t.inicio / dur) * 100); s += `<line x1="${xv}" x2="${xv}" y1="${T}" y2="${H - B}" stroke="var(--border)"/>`; });
  if (dur) marcas.filter((a) => a.tempo_s != null).forEach((a) => { const xv = x((a.tempo_s / dur) * 100); s += `<path d="M${xv - 5},${H - B + 1} L${xv + 5},${H - B + 1} L${xv},${H - B - 7}Z" fill="var(--mark)"><title>${esc(tempo(+a.tempo_s))} ${esc(a.texto)}</title></path>`; });
  const rotulos = [];
  series.forEach((se, i) => {
    const d = se.pontos.map((p, k) => `${k ? "L" : "M"}${x(p[0]).toFixed(1)},${y(p[1]).toFixed(1)}`).join(" ");
    if (!se.ref && series.filter((z) => !z.ref).length === 1) s += `<path d="${d} L${x(se.pontos.at(-1)[0])},${y(0)} L${x(0)},${y(0)}Z" fill="url(#ga${i})"/>`;
    s += `<path d="${d}" fill="none" stroke="${se.cor}" stroke-width="2" ${se.ref ? 'stroke-dasharray="5 4"' : ""} stroke-linejoin="round" stroke-linecap="round"/>`;
    if (!se.ref) se.pontos.forEach((p) => { s += `<circle cx="${x(p[0])}" cy="${y(p[1])}" r="3.5" fill="${se.cor}" stroke="var(--surface-1)" stroke-width="2"/>`; });
    const u = se.pontos.at(-1);
    rotulos.push({ y: y(u[1]), nome: se.nome });
  });
  rotulos.sort((a, b) => a.y - b.y).forEach((r, i, arr) => { if (i && r.y - arr[i - 1].y < 14) r.y = arr[i - 1].y + 14; s += `<text class="rotulo" x="${W - R + 10}" y="${r.y + 4}">${esc(r.nome)}</text>`; });
  s += `<line class="mira" x1="0" x2="0" y1="${T}" y2="${H - B}"/>`;
  series.forEach((se) => { s += `<circle class="ponto-ativo" r="5" fill="${se.cor}" stroke="var(--surface-1)" stroke-width="2.5" cx="-10" cy="-10"/>`; });
  s += `<rect class="hover" x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}" fill="transparent"/></svg>`;
  const legenda = `<div class="legenda">${series.map((se) => `<span class="${se.ref ? "ref" : ""}" style="--c:${se.cor}">${esc(se.nome)}</span>`).join("")}</div>`;
  const id = "g" + Math.random().toString(36).slice(2);
  const xs = [...new Set(series.flatMap((se) => se.pontos.map((p) => p[0])))].sort((a, b) => a - b);
  setTimeout(() => {
    const box = document.getElementById(id); if (!box) return;
    const svg = $("svg", box), tip = $(".tooltip", box), rect = $("rect.hover", box), mira = $(".mira", box), pts = $$(".ponto-ativo", box);
    rect.addEventListener("mousemove", (ev) => {
      const bb = svg.getBoundingClientRect(), px = ((ev.clientX - bb.left) / bb.width) * W;
      const xv = ((px - L) / (W - L - R)) * 100;
      const alvo = xs.reduce((a, b) => (Math.abs(b - xv) < Math.abs(a - xv) ? b : a));
      mira.setAttribute("x1", x(alvo)); mira.setAttribute("x2", x(alvo));
      const linhas = series.map((se, i) => {
        const p = se.pontos.reduce((a, b) => (Math.abs(b[0] - alvo) < Math.abs(a[0] - alvo) ? b : a));
        pts[i].setAttribute("cx", x(p[0])); pts[i].setAttribute("cy", y(p[1]));
        return `<div class="l" style="--c:${se.cor}"><span><i></i>${esc(se.nome)}</span><b>${F.pct(p[1])}</b></div>`;
      });
      tip.innerHTML = `<div class="t">${Math.round(alvo)}% do vídeo${dur ? ` · ${(alvo / 100 * dur).toFixed(1)} s` : ""}</div>` + linhas.join("");
      box.classList.add("ativo"); tip.style.display = "block";
      const left = (x(alvo) / W) * bb.width + 14;
      tip.style.left = Math.min(left, bb.width - tip.offsetWidth - 4) + "px"; tip.style.top = "6px";
    });
    rect.addEventListener("mouseleave", () => { box.classList.remove("ativo"); tip.style.display = "none"; });
  });
  return `${legenda}<div class="grafico" id="${id}">${s}<div class="tooltip"></div></div>`;
}

// ------------------------------------------------------------ dados (abre na hora, atualiza por trás)
// Cada resposta fica guardada por URL. A tela desenha com o que já tem e pede a versão nova por trás;
// só redesenha se algo mudou. Depois de qualquer gravação (POST), tudo vira "velho" e a próxima leitura espera o servidor.
const SWR = {};
const entradaSWR = (url) => SWR[url] || (SWR[url] = { gen: 0 });
const temDados = (url) => { const e = SWR[url]; return !!(e && e.dados && !e.velho); };
function buscarSWR(url) {
  const e = entradaSWR(url), gen = ++e.gen;
  const p = api(url).then((j) => {
    if (gen !== e.gen) return false;                    // houve gravação no meio: descarta esta resposta
    const txt = JSON.stringify(j), mudou = txt !== e.txt;
    Object.assign(e, { txt, dados: j, velho: false });
    return mudou;
  }).finally(() => { if (e.p === p) e.p = null; });
  e.p = p;
  return p;
}
async function swr(url, vivo, redesenhar) {
  const e = entradaSWR(url);
  for (let i = 0; i < 3 && (!e.dados || e.velho); i++) await (e.p || buscarSWR(url));
  if (!e.dados) await buscarSWR(url);
  else if (redesenhar && !e.p && !e.recente) {
    e.recente = true; setTimeout(() => (e.recente = false), 3000);   // no máximo uma revalidação a cada 3 s
    buscarSWR(url).then((mudou) => { if (mudou && vivo && vivo() && !ocupado()) redesenhar(); }).catch(() => {});
  }
  return e.dados;
}
// Não redesenha por baixo de quem está digitando, com pop-up aberto ou arrastando card: o dado novo fica guardado
// e aparece na próxima vez que a tela abrir.
function ocupado() {
  const a = document.activeElement;
  return !!(document.querySelector("dialog.modal") || document.querySelector(".kcard.arrastando") || (a && a !== document.body && a.closest("#app") && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)));
}
function preCarregar(url) { const e = entradaSWR(url); if (!e.dados && !e.p) buscarSWR(url).catch(() => {}); }
function sujarTudo() { Object.values(SWR).forEach((e) => { e.velho = true; e.gen++; e.p = null; e.recente = false; }); }

let CACHE = null;
function posLista() {
  const comMoeda = CACHE.criativos.find((c) => c.metricas.moeda);
  if (comMoeda) MOEDA = comMoeda.metricas.moeda;
  atualizarContFila();
  return CACHE;
}
// forcar: espera a versão do servidor (usar logo depois de gravar algo).
async function carregarLista(forcar, vivo, redesenhar) {
  if (forcar || !CACHE) { const e = entradaSWR("/api/criativos"); if (forcar) e.velho = true; }
  CACHE = await swr("/api/criativos", vivo, redesenhar);
  return posLista();
}
// Lista para desenhar uma tela: na hora, se já houver; e redesenha a tela se o servidor trouxer algo novo.
const listaRapida = (vivo, redesenhar) => carregarLista(false, vivo, redesenhar);
async function variaveisLib(vivo, redesenhar) { return (await swr("/api/variaveis", vivo, redesenhar)).variaveis; }

// Passar o mouse num link de criativo já busca o detalhe: o clique abre sem espera.
let preT;
document.addEventListener("mouseover", (e) => {
  const a = e.target.closest && e.target.closest('a[href^="#/c/"]');
  if (!a) return;
  clearTimeout(preT);
  preT = setTimeout(() => preCarregar("/api/criativos/" + a.getAttribute("href").slice(4)), 90);
});

const cabeca = (titulo, sub, acoes = "") => `<div class="cabeca-pagina"><div><h1>${titulo}</h1>${sub ? `<p>${sub}</p>` : ""}</div><div class="barra-ferramentas" style="margin:0">${acoes}</div></div>`;
const vazio = (txt) => `<div class="vazio">${ICONE.vazio}<div>${txt}</div></div>`;

// ------------------------------------------------------------ escopo: marca > produto > oferta
let CATALOGO = { marcas: [], produtos: [], ofertas: [] };
let ESCOPO = prefs.get("escopo", { marca: "", produto: "", oferta: "" });
const SEM = "__sem";                  // criativos sem oferta (ainda não registrados no banco)

async function carregarCatalogo(vivo, redesenhar) { CATALOGO = await swr("/api/catalogo", vivo, redesenhar); }

// Filtro de escopo dentro da página (Biblioteca, Métricas, Variáveis, Anúncios, Fila). O valor é o
// mesmo em todas, então quem filtra uma marca na Biblioteca encontra a mesma marca em Métricas.
function filtroEscopo() {
  const ms = CATALOGO.marcas, ps = CATALOGO.produtos.filter((p) => !ESCOPO.marca || p.marca_id === ESCOPO.marca);
  const os = CATALOGO.ofertas.filter((o) => (!ESCOPO.marca || o.marca_id === ESCOPO.marca) && (!ESCOPO.produto || o.produto_id === ESCOPO.produto));
  const sem = ESCOPO.marca === SEM, opt = (v, t, sel) => `<option value="${esc(v)}" ${v === sel ? "selected" : ""}>${esc(t)}</option>`;
  return `<div class="filtro-escopo ${escopoAtivo() ? "ativo" : ""}" title="Escopo: marca › produto › oferta">
    <span class="rot">${ICONE.filtro}Escopo</span>
    <select data-esc="marca" aria-label="Marca" class="${ESCOPO.marca ? "ativo" : ""}">${opt("", "Todas as marcas", ESCOPO.marca)}${ms.map((m) => opt(m.id, m.nome, ESCOPO.marca)).join("")}${opt(SEM, "Sem oferta definida", ESCOPO.marca)}</select>
    <select data-esc="produto" aria-label="Produto" class="${ESCOPO.produto ? "ativo" : ""}" ${sem ? "disabled" : ""}>${opt("", "Todos os produtos", ESCOPO.produto)}${ps.map((p) => opt(p.id, p.nome, ESCOPO.produto)).join("")}</select>
    <select data-esc="oferta" aria-label="Oferta" class="${ESCOPO.oferta ? "ativo" : ""}" ${sem ? "disabled" : ""}>${opt("", "Todas as ofertas", ESCOPO.oferta)}${os.map((o) => opt(o.id, `${o.id} · ${o.nome}${o.status !== "ativa" ? " (" + o.status + ")" : ""}`, ESCOPO.oferta)).join("")}</select>
    ${escopoAtivo() ? `<button type="button" class="limpar" data-esc-limpar title="Limpar escopo">${ICONE.fechar}</button>` : ""}
  </div>`;
}
function definirEscopo(novo) { ESCOPO = { marca: "", produto: "", oferta: "", ...novo }; prefs.set("escopo", ESCOPO); atualizarContFila(); }
function mudarEscopo(k, v) {
  const n = { ...ESCOPO, [k]: v };
  if (k === "marca") { n.produto = ""; n.oferta = ""; }
  if (k === "produto") n.oferta = "";
  definirEscopo(n); rota();
}
document.addEventListener("change", (e) => { const s = e.target.closest("[data-esc]"); if (s) mudarEscopo(s.dataset.esc, s.value); });
document.addEventListener("click", (e) => { if (e.target.closest("[data-esc-limpar]")) { definirEscopo({}); rota(); } });

const noEscopo = (c) => {
  if (!c) return false;
  if (ESCOPO.marca === SEM) return !c.oferta_id;
  return (!ESCOPO.marca || c.marca_id === ESCOPO.marca) && (!ESCOPO.produto || c.produto_id === ESCOPO.produto) && (!ESCOPO.oferta || c.oferta_id === ESCOPO.oferta);
};
const escopoAtivo = () => !!(ESCOPO.marca || ESCOPO.produto || ESCOPO.oferta);
function rotuloEscopo() {
  if (ESCOPO.marca === SEM) return "sem oferta definida";
  const o = CATALOGO.ofertas.find((x) => x.id === ESCOPO.oferta), p = CATALOGO.produtos.find((x) => x.id === ESCOPO.produto), m = CATALOGO.marcas.find((x) => x.id === ESCOPO.marca);
  return o ? `oferta ${o.id}` : p ? p.nome : m ? m.nome : "todas as marcas";
}
const doEscopo = () => (CACHE ? CACHE.criativos.filter(noEscopo) : []);

// Média só dos criativos com números do conjunto (razão das somas; contagens por criativo).
function mediaDe(lista) {
  const com = lista.filter((c) => c.metricas.tem_dados), n = com.length, s = {};
  com.forEach((c) => Object.entries(c.metricas.brutos || {}).forEach(([k, v]) => (s[k] = (s[k] || 0) + (v || 0))));
  const div = (a, b) => (b ? a / b : null), g = (k) => s[k] || 0;
  return {
    criativos: n,
    gasto: n ? g("gasto") / n : null, impressoes: n ? g("impressoes") / n : null, compras: n ? g("compras") / n : null, receita: n ? g("receita") / n : null,
    cpa: div(g("gasto"), g("compras")), roas: div(g("receita"), g("gasto")), ctr: div(g("cliques_link"), g("impressoes")),
    cpm: div(g("gasto") * 1000, g("impressoes")), gancho: div(g("views_3s"), g("impressoes")), thruplay: div(g("thruplays"), g("impressoes")),
    retencao50: div(g("p50"), g("plays")),
    curva: g("plays") ? { p25: g("p25") / g("plays"), p50: g("p50") / g("plays"), p75: g("p75") / g("plays"), p95: g("p95") / g("plays"), p100: g("p100") / g("plays"), v3s: g("views_3s") / g("plays") } : null,
  };
}

// Tags de marca, produto e oferta.
function tagsDe(c, { curto = false, max = 26 } = {}) {
  if (!c) return "";
  if (!c.oferta_id) return `<span class="tags"><span class="tag sem">sem oferta</span></span>`;
  return `<span class="tags">
    ${curto ? "" : `<span class="tag marca" title="Marca"><i></i>${esc(c.marca_nome)}</span>`}
    <span class="tag produto" title="Produto: ${esc(c.produto_nome)}"><i></i>${esc(curtoTxt(c.produto_nome, max))}</span>
    <span class="tag oferta" title="Oferta: ${esc(c.oferta_nome || "")}"><i></i>${esc(c.oferta_id)}</span></span>`;
}
const curtoTxt = (t, n) => (t && t.length > n ? t.slice(0, n - 1) + "…" : t || "");
const celulaPrevia = (c) => `<td class="previa">${c ? `<a href="#/c/${c.id}">${miniImg(c)}</a>` : `<span class="mini"></span>`}</td>`;
const celulaNome = (c, extra = "") => `<td class="esq"><div class="celula-nome"><a class="nome-criativo" href="#/c/${c.id}" data-espiar="${c.id}">${nomeC(c.id)}</a>${tagsDe(c, { curto: !!ESCOPO.marca && ESCOPO.marca !== SEM, max: 18 })}${extra}</div></td>`;

// ------------------------------------------------------------ biblioteca
function cardCriativo(c, i) {
  const m = c.metricas, ab = c.anotacoes.aberta || 0, pd = c.anotacoes.pedida || 0, capa = capaDe(c, 360);
  return `<a class="card spot entra" style="--i:${Math.min(i, 24)}" href="#/c/${c.id}" ${c.capa_video ? `data-video="${c.capa_video}"` : ""}>
    <div class="thumb">
      ${capa ? `<img src="${capa}" loading="lazy" alt="">` : `<div class="sem-midia">sem mídia local</div>`}
      <div class="vinheta"></div>
      <div class="topo">${m.tem_dados ? `<span class="badge acento">rodou</span>` : ""}${ab ? `<span class="badge vidro sem-ponto">${ab} anotação${ab > 1 ? "ões" : ""}</span>` : ""}${pd ? `<span class="badge vidro sem-ponto">${pd} na fila</span>` : ""}${c.n_videos > 1 ? `<span class="badge vidro sem-ponto">${c.n_videos} versões</span>` : ""}</div>
      ${tagsDe(c, { curto: true, max: 16 })}
      <div class="base"><div class="id">${nomeC(c.id)}</div><div class="fmt">${esc(c.formato || "–")}${c.marca_nome ? " · " + esc(c.marca_nome) : ""}</div></div>
      ${c.capa_video ? `<span class="play">${ICONE.play}</span>` : ""}
    </div>
    <div class="pe">
      <div class="linha">${badgeStatus(c.status)}<span class="muted small">${c.drive_nome ? esc(c.drive_nome.replace("Criativo ", "")) : c.nota != null ? "nota " + c.nota : ""}</span></div>
      ${m.tem_dados ? `<div class="kpis-mini"><div><b>${F.money(m.gasto)}</b><span>gasto</span></div><div><b>${F.int(m.compras)}</b><span>compras</span></div><div><b>${F.x(m.roas)}</b><span>ROAS</span></div></div>`
      : `<div class="muted small">${c.tipo === "video" ? "vídeo" : "imagem"} · sem números ainda</div>`}
    </div></a>`;
}
function ligarPreviewHover(raiz) {
  $$(".card[data-video]", raiz).forEach((card) => {
    let v;
    card.addEventListener("mouseenter", () => {
      if (reduzMovimento) return;
      v = document.createElement("video");
      Object.assign(v, { src: card.dataset.video + "#t=1", muted: true, loop: true, playsInline: true, autoplay: true });
      v.addEventListener("playing", () => v.classList.add("tocando"), { once: true });
      $(".thumb", card).insertBefore(v, $(".vinheta", card));
    });
    card.addEventListener("mouseleave", () => { if (v) { v.pause(); v.removeAttribute("src"); v.load(); v.remove(); v = null; } });
  });
}
async function telaBiblioteca(vivo) {
  if (!temDados("/api/criativos")) app.innerHTML = cabeca("Biblioteca", "Carregando…") + `<div class="carregando">${"<div class='esqueleto'></div>".repeat(12)}</div>`;
  const d = await listaRapida(vivo, () => telaBiblioteca(vivo));
  if (!vivo()) return;
  const f = prefs.get("filtros", { busca: "", tipo: "", status: "", rodou: false, ordem: "id" });
  // Biblioteca = acervo pronto (entregue, no ar, pausado, descartado). O que está sendo feito fica na Produção.
  const prontos = d.criativos.filter((c) => c.status !== "em_producao");
  const cs = prontos.filter(noEscopo), rodaram = cs.filter((c) => c.metricas.tem_dados);
  const emProd = d.criativos.filter((c) => c.status === "em_producao" && noEscopo(c)).length;
  const abertas = cs.reduce((s, c) => s + (c.anotacoes.aberta || 0), 0), fila = cs.reduce((s, c) => s + (c.anotacoes.pedida || 0), 0);
  const semOferta = prontos.filter((c) => !c.oferta_id).length;
  app.innerHTML = cabeca("Biblioteca", `${escopoAtivo() ? `<b>${esc(rotuloEscopo())}</b> · ` : ""}${cs.length} criativos prontos · ${cs.filter((c) => c.tipo === "video").length} vídeos · ${cs.filter((c) => c.tipo !== "video").length} imagens`, filtroEscopo())
    + (semOferta && !escopoAtivo() ? `<div class="aviso">${semOferta} criativo(s) ainda sem oferta. Abra o criativo e clique em "Definir oferta" para ele entrar no filtro de marca, produto e oferta (ou escolha "Sem oferta definida" no escopo).</div>` : "")
    + `<div class="bento spot-area">
      <div class="tile spot entra" style="--i:0"><div class="rot">${ICONE.filme}Criativos prontos</div><div class="val">${numero(cs.length, "int")}</div><div class="sub"><a href="#/producao" class="link-sutil">${emProd} em produção →</a></div></div>
      <div class="tile spot entra" style="--i:1"><div class="rot">${ICONE.alvo}Rodaram em campanha</div><div class="val">${numero(rodaram.length, "int")}</div><div class="sub">${cs.filter((c) => c.status === "no_ar").length} no ar agora</div></div>
      <div class="tile spot entra" style="--i:2"><div class="rot">${ICONE.moeda}Gasto total</div><div class="val">${numero(rodaram.reduce((s, c) => s + (c.metricas.gasto || 0), 0), "money")}</div><div class="sub">${F.int(rodaram.reduce((s, c) => s + (c.metricas.compras || 0), 0))} compras</div></div>
      <div class="tile spot entra" style="--i:3"><div class="rot">${ICONE.lapis}Anotações</div><div class="val">${numero(abertas, "int")}</div><div class="sub">${fila} na fila de refação</div></div>
    </div>
    <div class="barra-ferramentas">
      <div class="busca">${ICONE.busca}<input id="f-busca" placeholder="Buscar #05, formato, oferta, variável…" value="${esc(f.busca)}"></div>
      <div class="segmentado" id="f-tipo"><button data-v="">Todos</button><button data-v="video">Vídeo</button><button data-v="nativo">Imagem</button></div>
      <select id="f-status"><option value="">Todos os status</option>${Object.entries(STATUS).filter(([k]) => k !== "em_producao").map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select>
      <label class="chave"><input type="checkbox" id="f-rodou" ${f.rodou ? "checked" : ""}><span class="trilho"></span>Só os que rodaram</label>
      <select id="f-ordem" class="direita"><option value="id">Ordem: número</option><option value="compras">Mais compras</option><option value="roas">Maior ROAS</option><option value="gasto">Maior gasto</option><option value="nota">Maior nota</option><option value="anot">Com anotações</option></select>
    </div>
    <div class="grade spot-area" id="grade"></div>`;
  animarNumeros();
  $("#f-status").value = f.status; $("#f-ordem").value = f.ordem;
  let tipo = f.tipo;
  const desenhar = () => {
    const g = { busca: $("#f-busca").value.trim().toLowerCase(), tipo, status: $("#f-status").value, rodou: $("#f-rodou").checked, ordem: $("#f-ordem").value };
    prefs.set("filtros", g);
    let l = cs.filter((c) =>
      (!g.tipo || (g.tipo === "video" ? c.tipo === "video" : c.tipo !== "video")) &&
      (!g.status || c.status === g.status) && (!g.rodou || c.metricas.tem_dados) &&
      (!g.busca || [c.id, nomeC(c.id), "#" + c.id.slice(1), c.formato, c.descricao, c.drive_nome, c.marca_nome, c.produto_nome, c.oferta_id, c.oferta_nome, ...c.variaveis.map((v) => v.valor + " " + v.id)].join(" ").toLowerCase().includes(g.busca)));
    const k = { compras: (c) => c.metricas.compras || 0, roas: (c) => c.metricas.roas || 0, gasto: (c) => c.metricas.gasto || 0, nota: (c) => c.nota || 0, anot: (c) => (c.anotacoes.aberta || 0) + (c.anotacoes.pedida || 0) }[g.ordem];
    if (k) l = [...l].sort((a, b) => k(b) - k(a));
    $("#grade").innerHTML = l.map(cardCriativo).join("") || vazio("Nada com esses filtros.");
    ligarPreviewHover($("#grade"));
  };
  segmentado($("#f-tipo"), tipo, (v) => { tipo = v; desenhar(); });
  ["#f-busca", "#f-status", "#f-rodou", "#f-ordem"].forEach((s) => $(s).addEventListener("input", desenhar));
  desenhar();
}

// ------------------------------------------------------------ detalhe: esteira e abas
function barraEsteira(d) {
  const e = d.esteira, et = d.etapas, i = et.indexOf(e.etapa), dono = e.aguardando === "dono";
  const pedidas = (d.anotacoes_lista || []).filter((a) => a.status === "pedida").length;
  const info = [ha(e.desde) && "nesta etapa " + ha(e.desde), e.custo_usd ? "gasto " + usd(e.custo_usd) : "", e.inferida ? "etapa deduzida dos arquivos (corrija em Mover)" : ""].filter(Boolean).join(" · ");
  return `<div class="esteira-barra ${dono ? "vez-dono" : ""}">
    <ol class="passos">${et.map((k, j) => `<li class="${j < i ? "feito" : j === i ? "atual" : ""}"><span class="bol">${j < i ? "✓" : j + 1}</span>${rotEtapa(k, d.tipo)}</li>`).join("")}<li><span class="bol">★</span>Entregue</li></ol>
    <div class="esteira-acoes">
      <div class="esteira-info">
        ${dono ? `<span class="selo dono">aguardando você</span><b>${esc(rotEtapa(e.etapa, d.tipo))} pronto para aprovar</b>`
               : `<span class="selo claude">com o Claude</span><span>${pedidas ? `<b>${pedidas} ajuste(s) pedido(s).</b> ` : ""}No Claude Code, diga "continue a esteira".</span>`}
        ${info ? `<span class="muted small">${info}</span>` : ""}
      </div>
      <div class="btns">
        ${dono ? `<button class="btn" id="es-ajuste">${ICONE.lapis}Pedir ajuste</button><button class="btn primario" id="es-aprovar">✓ ${e.etapa === "revisao" ? "Aprovar e entregar" : "Aprovar " + rotEtapa(e.etapa, d.tipo).toLowerCase()}</button>` : ""}
        <button class="btn fantasma" id="es-mover">Mover</button><button class="btn fantasma" id="es-descartar">Descartar</button>
      </div>
    </div></div>`;
}

// Texto do anúncio: da ficha.json; sem ficha, do copy_final_<idioma>.txt dos nativos.
function anuncioDe(d) {
  const f = d.ficha && d.ficha.anuncio;
  if (f && (f.texto_principal || f.titulo)) return { ...f, fonte: "ficha.json" };
  if (d.copy) {
    const t = d.copy, pega = (r) => ((t.match(r) || [])[1] || "").trim();
    const corpo = t.split(/TEXTO DO POST:\s*\n/)[1];
    return { titulo: pega(/T[ÍI]TULO DO LINK:\s*(.*)/), descricao: pega(/DESCRI[ÇC][ÃA]O:\s*(.*)/), botao: pega(/BOT[ÃA]O:\s*(.*)/), texto_principal: (corpo ?? t).trim(), fonte: "copy_final" };
  }
  return null;
}
const BLOCOS = [["hook", "Hook", "para o dedo e escolhe quem fica"], ["body", "Body", "problema, mecanismo, produto, prova"], ["cta", "CTA", "oferta, garantia e chamada"]];
const ROT_ESTRATEGIA = { consciencia: "Nível de consciência", sofisticacao: "Sofisticação do mercado", lead: "Tipo de lead", crenca: "Crença única", promessa: "Promessa", mecanismo: "Mecanismo", avatar: "Avatar", angulo: "Ângulo", desejo: "Desejo de massa" };
const btnCopiar = (txt) => (txt ? `<button class="copiar" data-copiar="${esc(txt)}" title="Copiar">copiar</button>` : "");

function abaCopy(d) {
  const f = d.ficha || {}, an = anuncioDe(d), pt = (an && an.pt) || {};
  const campoAn = (rot, k, longo) => an && an[k] ? `<div class="an-campo ${longo ? "longo" : ""}"><div class="an-rot">${rot}${btnCopiar(an[k])}</div><div class="an-val" data-orig="${esc(an[k])}" data-pt="${esc(pt[k] || "")}">${esc(an[k])}</div></div>` : "";
  const anuncio = `<div class="caixa"><h2>Anúncio na Meta ${an ? `<span class="direita">${an.fonte}${an.pt ? ` · <label class="chave small"><input type="checkbox" id="an-pt"><span class="trilho"></span>ver em português</label>` : ""}</span>` : ""}</h2>
    ${an ? `<div class="anuncio">${campoAn("Texto principal", "texto_principal", true)}<div class="an-link">${campoAn("Título", "titulo")}${campoAn("Descrição", "descricao")}${campoAn("Botão", "botao")}${an.url ? campoAn("URL", "url") : ""}</div></div>`
         : `<p class="muted small" style="margin:0">${f.anuncio && f.anuncio.pendente ? esc(f.anuncio.pendente) : "Texto do anúncio ainda não escrito. O Claude escreve na etapa de roteiro e grava na ficha.json."}</p>`}</div>`;
  if (!d.ficha) {
    const rot = d.documentos.find((x) => /^roteiro_/.test(x.nome));
    return anuncio + (d.ficha_erro ? `<div class="aviso" style="border-left-color:var(--bad)">${esc(d.ficha_erro)}</div>` : "")
      + `<div class="caixa"><h2>Roteiro <span class="direita">sem ficha.json: mostrando ${rot ? esc(rot.nome) : "nada"}</span></h2>${rot ? md(rot.texto) : vazio("Sem roteiro nesta pasta ainda.")}</div>`;
  }
  const chips = [f.processo && (f.processo === "modelagem" ? "Modelagem" : "Réplica"), f.formato, f.idioma && f.idioma.toUpperCase(), f.duracao_s && `~${f.duracao_s} s`].filter(Boolean);
  const kv = (o, rot) => Object.entries(o || {}).filter(([, v]) => v).map(([k, v]) => `<div class="kv"><span>${esc((rot && rot[k]) || k)}</span><div>${esc(v)}</div></div>`).join("");
  const linhas = (f.roteiro || []);
  const bloco = ([k, rot, sub]) => {
    const ls = linhas.filter((l) => (l.bloco || "body") === k);
    if (!ls.length) return "";
    return `<div class="rbloco b-${k}"><div class="rbloco-cab"><b>${rot}</b><span>${sub}</span><span class="direita muted small">${ls.reduce((s, l) => s + (+l.duracao_s || 0), 0) || ""}${ls.some((l) => l.duracao_s) ? " s" : ""}</span></div>
      ${ls.map((l) => `<div class="rlinha">
        <div class="rtake"><b>${esc(l.take || "")}</b>${l.duracao_s ? `<span>${l.duracao_s} s</span>` : ""}</div>
        <div class="rfala"><div class="orig">${esc(l.fala || "")}</div>${l.pt ? `<div class="pt">${esc(l.pt)}</div>` : ""}</div>
        <div class="rmeta">${l.funcao ? `<div class="funcao">${esc(l.funcao)}</div>` : ""}${(l.elementos || []).length ? `<div class="els">${l.elementos.map((x) => `<span>${esc(x)}</span>`).join("")}</div>` : ""}
          ${l.visual ? `<div class="det"><i>Visual</i>${esc(l.visual)}</div>` : ""}${l.texto_tela ? `<div class="det"><i>Na tela</i>${esc(l.texto_tela)}</div>` : ""}
          ${l.alerta ? `<div class="det alerta"><i>⚠</i>${esc(l.alerta)}</div>` : ""}</div>
      </div>`).join("")}</div>`;
  };
  const lista = (t, l, cls = "") => (l && l.length ? `<div class="caixa ${cls}"><h2>${t}</h2><ul class="lista">${l.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>` : "");
  return `<div class="caixa ficha-topo">${f.resumo ? `<p class="resumo">${esc(f.resumo)}</p>` : ""}<div class="chips-mini">${chips.map((c) => `<span>${esc(c)}</span>`).join("")}</div></div>`
    + anuncio
    + `<div class="grade-2">
        ${f.estrategia ? `<div class="caixa"><h2>Estratégia de copy</h2>${kv(f.estrategia, ROT_ESTRATEGIA)}</div>` : ""}
        ${f.teste ? `<div class="caixa"><h2>Teste ${f.teste.id ? `<span class="direita">${esc(f.teste.id)}</span>` : ""}</h2>${kv({ variavel: f.teste.variavel, hipotese: f.teste.hipotese, vitoria: f.teste.vitoria, corte: f.teste.corte }, { variavel: "Variável em teste", hipotese: "Hipótese", vitoria: "Vence se", corte: "Corta se" })}</div>` : ""}
        ${f.referencia ? `<div class="caixa"><h2>Referência</h2>${kv({ rotulo: f.referencia.rotulo, link: f.referencia.link, vem: f.referencia.o_que_vem_dela }, { rotulo: "Base", link: "Link", vem: "O que vem dela" })}</div>` : ""}
      </div>`
    + `<div class="caixa"><h2>Roteiro dissecado <span class="direita"><label class="chave small"><input type="checkbox" id="r-pt" checked><span class="trilho"></span>tradução</label></span></h2>
        <div id="roteiro" class="roteiro">${BLOCOS.map(bloco).join("") || vazio("Roteiro vazio na ficha.")}</div></div>`
    + lista("Adaptações em relação à referência", f.adaptacoes) + lista("Riscos (política e alegações)", f.riscos, "riscos")
    + (f.checklist && f.checklist.length ? `<div class="caixa"><h2>Checklist de copy</h2><ul class="lista check">${f.checklist.map((c) => `<li class="${c.ok ? "ok" : "nao"}"><b>${c.ok ? "✓" : "✗"}</b> ${esc(c.item)}${c.nota ? ` <span class="muted">— ${esc(c.nota)}</span>` : ""}</li>`).join("")}</ul></div>` : "");
}
function ligarAbaCopy() {
  const p = $('[data-painel="copy"]');
  p.addEventListener("click", async (e) => {
    const b = e.target.closest("[data-copiar]"); if (!b) return;
    e.preventDefault();
    try { await navigator.clipboard.writeText(b.dataset.copiar); b.textContent = "copiado"; setTimeout(() => (b.textContent = "copiar"), 1500); }
    catch { toast("Não deu para copiar: selecione o texto e use Ctrl+C."); }
  });
  $("#an-pt", p)?.addEventListener("change", (e) => $$(".an-val", p).forEach((v) => (v.textContent = e.target.checked && v.dataset.pt ? v.dataset.pt : v.dataset.orig)));
  $("#r-pt", p)?.addEventListener("change", (e) => $("#roteiro", p).classList.toggle("sem-pt", !e.target.checked));
}

function abaMidia(d) {
  const porTake = {};
  d.takes_arquivos.forEach((t) => (porTake[t.take] = porTake[t.take] || []).push(t));
  const falaDe = (tk) => ((d.ficha?.roteiro || []).find((l) => l.take === tk) || {}).fala || ((d.videos[0]?.takes || []).find((x) => x.take === tk) || {}).texto || "";
  const nAnot = (arq) => (d.anotacoes_lista || []).filter((a) => a.arquivo === arq && a.status !== "descartada").length;
  const mini = (arq, url, nome, video) => `<button class="mcard" data-ver="${esc(arq)}" data-url="${esc(url)}" data-video="${video ? 1 : ""}" title="${esc(nome)}">
      <img src="${thumb(arq, video ? 0.5 : 0, 240)}" loading="lazy" alt="">${video ? `<span class="play">${ICONE.play}</span>` : ""}
      <span class="nome">${esc(nome)}</span>${nAnot(arq) ? `<span class="badge vidro sem-ponto anot">${nAnot(arq)}</span>` : ""}</button>`;
  const takes = Object.keys(porTake).length ? Object.entries(porTake).map(([tk, vs]) => `<div class="take-grupo"><div class="take-cab"><b>${esc(tk)}</b><span class="sec small">${esc(falaDe(tk))}</span></div>
      <div class="mgrade">${vs.map((v) => mini(v.arquivo, v.url, v.nome.replace(/\.mp4$/, ""), true)).join("")}</div></div>`).join("")
    : `<p class="muted small" style="margin:0">Nenhum take na pasta.</p>`;
  const imgs = d.imagens.length ? `<div class="mgrade">${d.imagens.map((im) => mini(im.arquivo, im.url, im.nome, false)).join("")}</div>` : `<p class="muted small" style="margin:0">Nenhuma imagem na pasta.</p>`;
  return `<div class="caixa"><h2>Takes <span class="direita">${d.takes_arquivos.length} arquivo(s) · clique para ver e anotar</span></h2>${takes}</div>
    <div class="caixa"><h2>Imagens <span class="direita">${d.imagens.length}</span></h2>${imgs}</div>`;
}
function ligarAbaMidia(d) {
  $('[data-painel="midia"]').addEventListener("click", (e) => {
    const b = e.target.closest("[data-ver]"); if (!b) return;
    const video = !!b.dataset.video, arq = b.dataset.ver;
    const anots = (d.anotacoes_lista || []).filter((a) => a.arquivo === arq && a.status !== "descartada");
    modal({
      titulo: esc(arq.split("/").pop()), largo: true, cancelar: "Fechar", botao: "Guardar anotação",
      corpo: `<div class="visor">${video ? `<video src="${b.dataset.url}" controls autoplay playsinline></video>` : `<img src="${b.dataset.url}" alt="">`}</div>
        ${anots.length ? `<ul class="lista small" style="margin:12px 0 0">${anots.map((a) => `<li>${a.tempo_s != null ? `<b>${tempo(+a.tempo_s)}</b> ` : ""}${esc(a.texto)} <span class="muted">(${esc(a.autor || "?")}, ${a.status})</span></li>`).join("")}</ul>` : ""}
        <div class="modal-campos" style="margin-top:12px">${campo(video ? "Anotar neste ponto do take (pause no lugar certo)" : "Anotar nesta imagem", `<textarea name="texto" rows="2" placeholder="Ex.: mão deformada, refazer; fala cortada no fim"></textarea>`, "inteiro")}</div>`,
      aoSalvar: async (r, form) => {
        if (!r.texto) throw new Error("Escreva o que mudar.");
        const v = $("video", form); if (v) v.pause();
        const a = await api("/api/anotacoes", { criativo_id: d.id, arquivo: arq, tempo_s: v ? v.currentTime : null, texto: r.texto });
        d.anotacoes_lista.push(a);
        toast(`Anotado${v ? " em " + tempo(v.currentTime) : ""}. Para mandar ao Claude: "Pedir ajuste" (em produção) ou "Refazer com anotações" (Visão geral).`, 7000);
      },
    });
  });
}

function abaDocs(d) {
  if (!d.documentos.length) return vazio("Nenhum documento na pasta.");
  return `<div class="segmentado docs-sel" id="docs-sel">${d.documentos.map((x, i) => `<button data-v="${i}">${esc(x.nome)}</button>`).join("")}</div><div class="caixa" id="doc-corpo" style="margin-top:12px"></div>`;
}
function ligarAbaDocs(d) {
  if (!d.documentos.length) return;
  const mostrar = (i) => { const x = d.documentos[+i]; $("#doc-corpo").innerHTML = /\.md$/.test(x.nome) ? md(x.texto) : `<pre class="copy">${esc(x.texto)}</pre>`; };
  const ini = String(Math.max(0, d.documentos.findIndex((x) => /^roteiro_/.test(x.nome))));
  let feito = false;
  $("#abas").addEventListener("click", (e) => { if (!feito && e.target.closest('[data-aba="docs"]')) { feito = true; segmentado($("#docs-sel"), ini, mostrar); } });
  mostrar(ini);
}

const ROT_ACAO = { criou: "entrou na esteira", entregou: "entregou para aprovação", aprovou: "aprovou", pediu_ajuste: "pediu ajuste", moveu: "moveu", descartou: "descartou", concluiu: "aprovou a entrega" };
function abaHistorico(d) {
  if (!d.eventos.length) return vazio("Sem histórico ainda. Cada entrega, aprovação e ajuste aparece aqui.");
  return `<div class="caixa"><ol class="linha-hist">${d.eventos.map((e) => `<li class="h-${e.acao}">
    <div class="quando">${new Date(e.em).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}</div>
    <div><b>${esc(e.autor || "?")}</b> ${ROT_ACAO[e.acao] || e.acao} <span class="badge sem-ponto">${esc(rotEtapa(e.etapa, d.tipo))}</span>${e.custo_usd ? ` <span class="muted small">${usd(+e.custo_usd)}</span>` : ""}
      ${e.comentario ? `<div class="sec">${esc(e.comentario)}</div>` : ""}</div></li>`).join("")}</ol></div>`;
}

async function telaCriativo(cid, vivo) {
  const url = "/api/criativos/" + cid;
  if (!temDados(url)) app.innerHTML = `<a class="voltar" href="#/">${ICONE.voltar}Voltar</a>` + cabeca(nomeC(cid), "Carregando…");
  // O detalhe redesenha sozinho se o servidor trouxer algo novo, mas não no meio de um vídeo tocando.
  const redesenhar = () => { const v = $("#player video"); if (!(v && !v.paused) && !document.querySelector("dialog.modal")) telaCriativo(cid, vivo); };
  const [d, vars] = await Promise.all([swr(url, vivo, redesenhar), variaveisLib().catch(() => []), listaRapida()]);
  if (!vivo()) return;
  if (d.metricas.moeda) MOEDA = d.metricas.moeda;
  let vi = 0, imgSel = d.imagens.length ? d.imagens.length - 1 : -1;
  // Compara com a mesma oferta; sem oferta, com todos.
  const grupo = d.oferta_id ? CACHE.criativos.filter((c) => c.oferta_id === d.oferta_id) : CACHE.criativos;
  const m = d.metricas, media = mediaDe(grupo), rotMedia = d.oferta_id ? `da oferta ${d.oferta_id}` : "geral";
  const v0 = d.videos[0] || {};
  const ofertasOpc = (sel) => CATALOGO.ofertas.map((o) => `<option value="${esc(o.id)}" ${o.id === sel ? "selected" : ""}>${esc(o.id)} · ${esc(o.nome)}</option>`).join("");
  const caixaOferta = d.no_banco
    ? `<div class="caixa"><h2>Oferta<button class="btn mini direita" id="of-trocar">${ICONE.lapis}Trocar oferta</button></h2>
        <div class="barra-ferramentas" style="margin:0">${tagsDe(d)}<span class="sec small">${esc(d.oferta_nome || "")}</span></div></div>`
    : `<div class="caixa" style="border-color:var(--warn)"><h2>Oferta<button class="btn mini primario direita" id="btn-reg">${ICONE.mais}Definir oferta</button></h2>
        <p class="small muted" style="margin:0">Este criativo ainda não está no banco. Defina a oferta para ele entrar no filtro de marca, produto e oferta e na média do grupo.</p></div>`;

  const kpis = METRICAS.map((x, i) => {
    const c = compara(m[x.k], media[x.k], x.melhor);
    return `<div class="kpi spot entra" style="--i:${i}"><div class="rot">${x.rot}</div><div class="val">${numero(m[x.k], x.f)}</div>
      <div class="kpi-rodape">${c.txt ? `<span class="delta ${c.cls}">${c.txt}</span>` : ""}<span>média ${F[x.f](media[x.k])}</span></div></div>`;
  }).join("");

  const naProducao = !!d.esteira;
  const abas = [["geral", "Visão geral"], ["copy", "Copy e roteiro"], ["midia", `Takes e imagens <span class="n">${d.takes_arquivos.length + d.imagens.length}</span>`],
    ["docs", `Documentos <span class="n">${d.documentos.length}</span>`], ["hist", `Histórico <span class="n">${d.eventos.length}</span>`]];
  // Aba inicial: a que tem o que aprovar na etapa atual.
  const abaInicial = !naProducao ? "geral" : ["analise", "roteiro"].includes(d.esteira.etapa) ? "copy" : ["imagens", "takes"].includes(d.esteira.etapa) ? "midia" : "geral";
  app.innerHTML = `
    <a class="voltar" href="${naProducao ? "#/producao" : "#/"}">${ICONE.voltar}${naProducao ? "Produção" : "Biblioteca"}</a>
    ${cabeca(`${nomeC(d.id)} <span style="margin-left:8px;vertical-align:middle">${badgeStatus(d.status)}</span>`, [d.ficha?.titulo, d.formato, d.drive_nome, d.processo && (d.processo === "modelagem" ? "Modelagem" : "Réplica"), d.pasta].filter(Boolean).map(esc).join(" · "))}
    <div style="margin:-8px 0 18px">${tagsDe(d)}</div>
    ${naProducao ? barraEsteira(d) : ""}
    <nav class="abas" id="abas">${abas.map(([k, r]) => `<button data-aba="${k}" class="${k === abaInicial ? "ativa" : ""}">${r}</button>`).join("")}</nav>
    <div data-painel="copy" ${abaInicial === "copy" ? "" : "hidden"}>${abaCopy(d)}</div>
    <div data-painel="midia" ${abaInicial === "midia" ? "" : "hidden"}>${abaMidia(d)}</div>
    <div data-painel="docs" hidden>${abaDocs(d)}</div>
    <div data-painel="hist" hidden>${abaHistorico(d)}</div>
    <div class="detalhe" data-painel="geral" ${abaInicial === "geral" ? "" : "hidden"}>
      <div>
        <div class="caixa">
          ${d.videos.length > 1 ? `<div class="segmentado" id="sel-video" style="margin-bottom:12px;flex-wrap:wrap">${d.videos.map((v, i) => `<button data-v="${i}">${esc(v.nome.replace(/^Criativo \d+ - /, "").replace(/\.mp4$/, ""))}</button>`).join("")}</div>` : ""}
          <div class="player" id="player"></div>
          <div class="linha-tempo" id="lt"></div>
          <div class="take-texto" id="take-texto"></div>
          ${!d.videos.length && d.imagens.length ? `<div class="galeria" id="galeria">${d.imagens.map((im, i) => `<img src="${thumb(im.arquivo, 0, 160)}" data-i="${i}" title="${esc(im.nome)}" class="${i === imgSel ? "sel" : ""}">`).join("")}</div>` : ""}
          <div class="anotar">
            <textarea id="anot-texto" placeholder="O que mudar neste ponto? Ex.: trocar o fundo, legenda errada, fala mais rápida"></textarea>
            <div class="linha">
              <button class="btn primario" id="btn-anotar">${ICONE.lapis}Guardar anotação <span id="anot-t" class="num"></span></button>
              ${d.videos.length ? `<label class="chave small"><input type="checkbox" id="anot-peca"><span class="trilho"></span>vale para a peça inteira</label>` : ""}
            </div>
          </div>
        </div>
        <div class="caixa">
          <h2>Anotações <span class="direita" id="anot-resumo"></span></h2>
          <div id="anot-lista"></div>
          <div style="margin-top:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap">
            <button class="btn primario" id="btn-refazer">${ICONE.refazer}Refazer com anotações</button>
            <span class="small muted">Vai para a fila. O Claude refaz só o take marcado, com custo antes.</span>
          </div>
        </div>
        <div class="caixa">
          <h2>Nota de 0 a 10 <span class="direita">${d.avaliacoes.map((a) => `${esc(a.autor)}: ${a.nota}`).join(" · ") || "ninguém deu nota"}</span></h2>
          <div class="notas" id="notas">${Array.from({ length: 11 }, (_, i) => `<button data-n="${i}">${i}</button>`).join("")}</div>
        </div>
      </div>
      <div>
        ${caixaOferta}
        <div class="caixa">
          <h2>Métricas ${m.tem_dados ? `<span class="direita">${m.primeiro_dia} a ${m.ultimo_dia} · ${m.anuncios} anúncio(s) · média ${rotMedia} (${media.criativos} criativo(s))</span>` : ""}</h2>
          ${m.tem_dados ? `<div class="kpi-grade spot-area">${kpis}</div>` : vazio("Sem números ainda. Ligue um anúncio da Meta a este criativo (aba Anúncios) ou lance um número manual abaixo.")}
        </div>
        <div class="caixa">
          <h2>Retenção <span class="direita">de quem deu play</span></h2>
          ${m.curva ? graficoRetencao([
            { nome: "#" + d.id.slice(1), cor: "var(--series-1)", pontos: pontosCurva(m, v0.duracao) },
            { nome: "Média " + (d.oferta_id ? "da oferta" : "geral"), cor: "var(--ref)", ref: true, pontos: pontosCurva(media, null) },
          ], { dur: v0.duracao, takes: v0.takes || [], marcas: d.anotacoes_lista.filter((a) => a.arquivo === v0.arquivo) })
            + `<p class="small muted" style="margin:8px 0 0">Linhas verticais: troca de take. Triângulos: anotações. Pontos: 3 s, 25%, 50%, 75%, 95% e 100%.</p>`
          : vazio("A curva aparece quando houver números de vídeo da Meta.")}
        </div>
        <div class="caixa">
          <h2>Variáveis deste criativo<button class="btn mini direita" id="btn-var">${ICONE.mais}Marcar variável</button></h2>
          <div class="chips" id="vars">${d.variaveis.map((v) => `<span class="chip" title="${esc(v.categoria)} · ${esc(v.variavel)}"><span class="st-${v.status}">●</span><span class="id">${v.id}</span><span class="sec">${esc(v.valor.slice(0, 64))}</span>${v.papel === "em_teste" ? `<span class="badge acento sem-ponto">em teste</span>` : ""}<button data-rm="${v.id}" title="Tirar">✕</button></span>`).join("") || `<span class="muted small">Nenhuma marcada ainda.</span>`}</div>
        </div>
        ${d.copy ? `<div class="caixa"><h2>Texto do post</h2><div class="copy">${esc(d.copy)}</div></div>` : ""}
        <div class="caixa">
          <h2>Anúncios na Meta<button class="btn mini direita" id="btn-num" title="Lançar números sem a API da Meta">${ICONE.mais}Lançar número manual</button></h2>
          ${d.anuncios.length ? `<div class="tabela-wrap"><table class="tabela-padrao"><thead><tr><th class="previa"></th><th class="esq">Anúncio</th><th>Status</th><th>Gasto</th><th>Compras</th></tr></thead><tbody>${d.anuncios.map((a) => `<tr>${celulaPrevia(d)}<td class="esq"><div class="celula-nome"><span class="clamp">${esc(a.nome)}</span><span class="muted small clamp">${esc(a.campanha_nome || "")}</span></div></td><td>${esc(a.status || "")}</td><td>${F.money(a.gasto)}</td><td>${F.int(a.compras)}</td></tr>`).join("")}</tbody></table></div>`
            : `<p class="muted small" style="margin:0">Nenhum anúncio ligado. O nome do anúncio começando com "${d.id} |" liga sozinho na sincronização.</p>`}
          ${d.manuais.length ? `<p class="small muted" style="margin:12px 0 0">Números manuais: ${d.manuais.map((r) => `${r.periodo_inicio} a ${r.periodo_fim}: ${F.money(r.gasto)}, ${r.compras ?? 0} compras`).join(" · ")}</p>` : ""}
        </div>
      </div>
    </div>`;
  animarNumeros();

  // --- player + linha do tempo
  const video = () => $("#player video");
  const atual = () => d.videos[vi];
  function montarPlayer() {
    const pl = $("#player");
    if (d.videos.length) {
      pl.innerHTML = `<video src="${atual().url}" controls playsinline preload="auto" poster="${thumb(atual().arquivo, 0.5, 540)}"></video>`;
      const v = video(), dur = () => v.duration || atual().duracao || 1;
      const lt = $("#lt"), tks = atual().takes || [];
      const desenharLT = () => {
        const marcas = d.anotacoes_lista.filter((a) => a.arquivo === atual().arquivo && a.tempo_s != null && a.status !== "descartada");
        lt.innerHTML = `<div class="faixa">${tks.map((t, i) => `<div class="take" data-i="${i}" style="left:${(t.inicio / dur()) * 100}%;width:${((t.fim - t.inicio) / dur()) * 100}%" title="${esc(t.take)}: ${esc(t.texto)}">${esc(t.take)}</div>`).join("")
          || `<div class="take" style="left:0;width:100%">sem mapa de takes (montagem.json)</div>`}<div class="progresso" id="progresso"></div></div>`
          + marcas.map((a) => `<div class="marca ${a.status}" style="left:${(a.tempo_s / dur()) * 100}%" title="${esc(tempo(+a.tempo_s))} ${esc(a.texto)}"></div>`).join("")
          + `<div class="cabeca" id="cabeca"></div>`;
      };
      const tick = () => {
        if (!v.isConnected || !$("#anot-t")) return;          // tela já trocada
        const t = v.currentTime, p = (t / dur()) * 100;
        const cab = $("#cabeca"), pr = $("#progresso");
        if (cab) cab.style.left = p + "%";
        if (pr) pr.style.width = p + "%";
        $("#anot-t").textContent = $("#anot-peca") && $("#anot-peca").checked ? "· peça inteira" : `· ${tempo(t)}`;
        const i = tks.findIndex((x) => t >= x.inicio && t < x.fim);
        $$(".take", lt).forEach((el) => el.classList.toggle("atual", +el.dataset.i === i));
        $("#take-texto").innerHTML = i >= 0 ? `<b>${esc(tks[i].take)}</b>${esc(tks[i].texto)}` : `<span class="muted">Dê play ou clique na barra para ver o texto de cada take.</span>`;
      };
      v.addEventListener("loadedmetadata", () => { desenharLT(); tick(); });
      v.addEventListener("timeupdate", tick);
      v.addEventListener("seeked", tick);
      let raf; v.addEventListener("play", () => { const loop = () => { tick(); raf = requestAnimationFrame(loop); }; loop(); });
      v.addEventListener("pause", () => cancelAnimationFrame(raf));
      lt.onclick = (ev) => { const bb = lt.getBoundingClientRect(); v.currentTime = ((ev.clientX - bb.left) / bb.width) * dur(); };
      desenharLT(); tick();
      montarPlayer.redesenhar = desenharLT;
    } else if (imgSel >= 0) {
      pl.innerHTML = `<img src="${d.imagens[imgSel].url}" alt="">`;
      $("#lt").innerHTML = ""; $("#take-texto").hidden = true; $("#anot-t").textContent = `· ${d.imagens[imgSel].nome}`;
      montarPlayer.redesenhar = () => {};
    } else {
      pl.innerHTML = `<div class="sem-midia" style="position:static;aspect-ratio:9/16">Sem vídeo nem imagem local. Copie da pasta do time.</div>`;
      $("#take-texto").hidden = true;
      montarPlayer.redesenhar = () => {};
    }
  }
  montarPlayer();
  if ($("#sel-video")) segmentado($("#sel-video"), "0", (v) => { vi = +v; montarPlayer(); desenharAnot(); });
  $("#galeria")?.addEventListener("click", (e) => { const i = e.target.dataset.i; if (i == null) return; imgSel = +i; $$("#galeria img").forEach((im) => im.classList.toggle("sel", +im.dataset.i === imgSel)); montarPlayer(); desenharAnot(); });
  $("#anot-peca")?.addEventListener("change", () => video() && video().dispatchEvent(new Event("timeupdate")));

  // --- anotações
  function arquivoAtual() { return d.videos.length ? atual().arquivo : imgSel >= 0 ? d.imagens[imgSel].arquivo : null; }
  function desenharAnot() {
    const l = d.anotacoes_lista.filter((a) => a.status !== "descartada");
    const nAb = l.filter((a) => a.status === "aberta").length, nPd = l.filter((a) => a.status === "pedida").length;
    $("#btn-refazer").innerHTML = `${ICONE.refazer}Refazer com anotações (${nAb})`; $("#btn-refazer").disabled = !nAb;
    $("#anot-resumo").textContent = `${nAb} aberta(s) · ${nPd} na fila`;
    $("#anot-lista").innerHTML = l.map((a, i) => `
      <div class="anot entra" style="--i:${i}">
        <div class="quadro" data-t="${a.tempo_s ?? ""}" data-arq="${esc(a.arquivo || "")}" title="Ir para este ponto">
          ${a.arquivo ? `<img src="${thumb(a.arquivo, a.tempo_s ?? 0, 120)}" loading="lazy" alt="">` : ""}<span>${a.tempo_s != null ? tempo(+a.tempo_s) : "peça"}</span>
        </div>
        <div>${esc(a.texto)}
          <div class="meta">${a.take ? `<span class="badge acento sem-ponto">${esc(a.take)}</span>` : ""}<span class="badge ${a.status === "pedida" ? "em_producao" : a.status === "feita" ? "no_ar" : ""}">${a.status}</span>${esc(a.autor || "?")}${a.resposta ? " · " + esc(a.resposta) : ""}</div>
        </div>
        <div>${a.status === "aberta" ? `<button class="btn mini fantasma" data-del="${a.id}">Apagar</button>` : a.status === "pedida" ? `<button class="btn mini fantasma" data-desc="${a.id}">Cancelar</button>` : ""}</div>
      </div>`).join("") || `<p class="muted small" style="margin:0">Nenhuma anotação. Pause no ponto exato e escreva o que mudar.</p>`;
    montarPlayer.redesenhar && montarPlayer.redesenhar();
  }
  desenharAnot();
  $("#anot-lista").addEventListener("click", async (e) => {
    const q = e.target.closest(".quadro");
    if (q && q.dataset.t !== "" && d.videos.length) {
      const idx = d.videos.findIndex((v) => v.arquivo === q.dataset.arq);
      if (idx >= 0 && idx !== vi) { vi = idx; montarPlayer(); }
      const v = video(); const ir = () => { v.currentTime = +q.dataset.t; v.pause(); };
      v.readyState ? ir() : v.addEventListener("loadedmetadata", ir, { once: true });
      $("#player").scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    const del = e.target.dataset.del, desc = e.target.dataset.desc;
    try {
      if (del) { await api("/api/anotacoes/" + del, { apagar: true }); d.anotacoes_lista = d.anotacoes_lista.filter((a) => a.id != del); }
      if (desc) { await api("/api/anotacoes/" + desc, { status: "descartada" }); d.anotacoes_lista.find((a) => a.id == desc).status = "descartada"; }
      if (del || desc) desenharAnot();
    } catch (er) { toast(er.message); }
  });
  $("#btn-anotar").addEventListener("click", async () => {
    const texto = $("#anot-texto").value.trim();
    if (!texto) return toast("Escreva o que mudar.");
    const v = video(); if (v) v.pause();
    const peca = !v || ($("#anot-peca") && $("#anot-peca").checked);
    try {
      const r = await api("/api/anotacoes", { criativo_id: d.id, arquivo: arquivoAtual(), tempo_s: peca ? null : v.currentTime, texto });
      d.anotacoes_lista.push(r); d.anotacoes_lista.sort((a, b) => (a.tempo_s ?? -1) - (b.tempo_s ?? -1));
      $("#anot-texto").value = ""; desenharAnot();
      toast(r.take ? `Anotado em ${tempo(+r.tempo_s)} (${r.take}).` : "Anotado.");
    } catch (er) { toast(er.message); }
  });
  $("#btn-refazer").addEventListener("click", async () => {
    try {
      const r = await api("/api/refazer", { criativo_id: d.id });
      d.anotacoes_lista.forEach((a) => a.status === "aberta" && (a.status = "pedida")); desenharAnot();
      CACHE = null; carregarLista();
      toast(`${r.pedidas} pedido(s) na fila. No Claude Code, diga: "refaça os pedidos do painel".`, 7000);
    } catch (er) { toast(er.message); }
  });

  // --- nota
  const minha = d.avaliacoes.find((a) => a.autor === autor());
  if (minha) $(`#notas button[data-n="${minha.nota}"]`)?.classList.add("sel");
  $("#notas").addEventListener("click", async (e) => {
    const n = e.target.dataset.n; if (n == null) return;
    try { await api("/api/nota", { criativo_id: d.id, nota: +n }); $$("#notas button").forEach((b) => b.classList.toggle("sel", b.dataset.n === n)); toast("Nota gravada."); }
    catch (er) { toast(er.message); }
  });

  // --- variáveis
  const recarregar = () => telaCriativo(cid, vivo);

  // --- abas
  $("#abas").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-aba]"); if (!b) return;
    $$("#abas button").forEach((x) => x.classList.toggle("ativa", x === b));
    $$("[data-painel]").forEach((p) => (p.hidden = p.dataset.painel !== b.dataset.aba));
    $$('[data-painel]:not([data-painel="geral"]) video').forEach((v) => v.pause());
    if (b.dataset.aba !== "geral" && video()) video().pause();
  });
  ligarAbaCopy(d); ligarAbaMidia(d); ligarAbaDocs(d);

  // --- esteira: aprovar, pedir ajuste, mover, descartar
  const acaoEsteira = async (body, msg) => {
    const r = await api("/api/esteira", { criativo_id: d.id, ...body });
    toast(r.entregue ? `${nomeC(d.id)} entregue: foi para a Biblioteca.` : msg, 6000);
    CACHE = null; await carregarLista(true);
    recarregar();
  };
  $("#es-aprovar")?.addEventListener("click", () => {
    const e = d.esteira, ultima = e.etapa === "revisao";
    const prox = d.etapas[d.etapas.indexOf(e.etapa) + 1];
    modal({
      titulo: ultima ? "Aprovar e entregar" : `Aprovar ${rotEtapa(e.etapa, d.tipo).toLowerCase()}`,
      sub: ultima ? `${nomeC(d.id)} sai da Produção e vai para a Biblioteca como entregue.` : `${nomeC(d.id)} segue para ${rotEtapa(prox, d.tipo).toLowerCase()}, com o Claude. Ele informa o custo antes de gerar.`,
      botao: ultima ? "Aprovar e entregar" : "Aprovar",
      corpo: `<div class="modal-campos">${campo("Comentário (opcional)", `<textarea name="comentario" rows="3" placeholder="Ex.: pode seguir, mas use a imagem B2 no lugar da B1"></textarea>`, "inteiro")}</div>`
        + ((d.anotacoes_lista || []).some((a) => a.status === "aberta") ? `<p class="small" style="margin:10px 0 0;color:var(--warn)">Há anotações abertas neste criativo. Se elas são ajustes, use "Pedir ajuste".</p>` : ""),
      aoSalvar: (b) => acaoEsteira({ acao: "aprovar", comentario: b.comentario }, `${rotEtapa(e.etapa, d.tipo)} aprovado. No Claude Code: "continue a esteira".`),
    });
  });
  $("#es-ajuste")?.addEventListener("click", () => {
    const abertas = (d.anotacoes_lista || []).filter((a) => a.status === "aberta").length;
    modal({
      titulo: `Pedir ajuste: ${rotEtapa(d.esteira.etapa, d.tipo).toLowerCase()}`, sub: `${nomeC(d.id)} volta para o Claude refazer esta etapa.`, botao: "Pedir ajuste",
      corpo: `<div class="modal-campos">${campo("O que ajustar", `<textarea name="comentario" rows="5" placeholder="Ex.: o hook está longo, corte para uma frase; a CTA precisa citar os 30 dias"></textarea>`, "inteiro")}</div>`
        + (abertas ? `<p class="small muted" style="margin:10px 0 0">As ${abertas} anotação(ões) aberta(s) no vídeo ou nas imagens vão junto.</p>` : ""),
      aoSalvar: (b) => { if (!b.comentario) throw new Error("Escreva o que ajustar."); return acaoEsteira({ acao: "ajuste", comentario: b.comentario }, "Ajuste pedido. O card voltou para o Claude."); },
    });
  });
  $("#es-mover")?.addEventListener("click", () => modal({
    titulo: "Mover de etapa", sub: "Para corrigir a etapa do card (ex.: deduzida errado pelos arquivos).", botao: "Mover",
    corpo: `<div class="modal-campos">
      ${campo("Etapa", `<select name="etapa">${d.etapas.map((k) => `<option value="${k}" ${k === d.esteira.etapa ? "selected" : ""}>${rotEtapa(k, d.tipo)}</option>`).join("")}</select>`)}
      ${campo("Com quem está", `<select name="aguardando"><option value="dono" ${d.esteira.aguardando === "dono" ? "selected" : ""}>Aguardando aprovação</option><option value="claude" ${d.esteira.aguardando === "claude" ? "selected" : ""}>Com o Claude</option></select>`)}
      ${campo("Motivo (opcional)", `<input name="comentario">`, "inteiro")}</div>`,
    aoSalvar: (b) => acaoEsteira({ acao: "mover", ...b }, "Card movido."),
  }));
  $("#es-descartar")?.addEventListener("click", () => modal({
    titulo: `Descartar ${nomeC(d.id)}?`, sub: "Sai da Produção. Os arquivos da pasta ficam; o status vira descartado (se estiver registrado numa oferta).", botao: "Descartar",
    corpo: `<div class="modal-campos">${campo("Motivo", `<textarea name="comentario" rows="3" placeholder="Ex.: conceito fraco, risco de política"></textarea>`, "inteiro")}</div>`,
    aoSalvar: (b) => acaoEsteira({ acao: "descartar", comentario: b.comentario }, `${nomeC(d.id)} descartado.`),
  }));
  $("#btn-var").addEventListener("click", () => {
    // Só as variáveis da marca do criativo (todas, se ainda não tem oferta) e que ainda não estão marcadas.
    const marcadas = new Set(d.variaveis.map((v) => v.id));
    const opc = vars.filter((v) => (!d.marca_id || v.marca_id === d.marca_id) && !marcadas.has(v.variavel_id));
    const rot = (v) => `${v.variavel_id} · ${v.categoria} · ${v.variavel}: ${String(v.valor).slice(0, 80)} (${v.status})`;
    const opcoes = (l) => l.map((v) => `<option value="${esc(v.variavel_id)}">${esc(rot(v))}</option>`).join("");
    modal({
      titulo: "Marcar variável", sub: `${nomeC(d.id)}${d.marca_nome ? " · variáveis da " + esc(d.marca_nome) : ""}`, botao: "Marcar",
      corpo: opc.length ? `<div class="modal-campos">
          ${campo("Buscar", `<input id="mv-busca" placeholder="ID, categoria ou valor" autocomplete="off">`, "inteiro")}
          ${campo("Variável", `<select name="variavel_id" size="8" required>${opcoes(opc)}</select>`, "inteiro")}
          ${campo("Papel neste criativo", `<select name="papel"><option value="base">base (vem do que já ganhou)</option><option value="em_teste">em teste (a variável testada)</option></select>`, "inteiro")}
        </div>` : `<p class="muted">Nenhuma variável disponível${d.marca_nome ? " para a " + esc(d.marca_nome) : ""}. Registre as variáveis em <code>Variáveis/&lt;Marca&gt;.md</code>.</p>`,
      aoAbrir: (f) => {
        const sel = $('[name="variavel_id"]', f); if (!sel) return;
        sel.selectedIndex = 0;
        $("#mv-busca", f).addEventListener("input", (e) => {
          const q = e.target.value.trim().toLowerCase();
          sel.innerHTML = opcoes(opc.filter((v) => rot(v).toLowerCase().includes(q))); sel.selectedIndex = 0;
        });
      },
      aoSalvar: opc.length ? async (b) => {
        if (!b.variavel_id) throw new Error("Escolha uma variável.");
        await api("/api/criativo_variaveis", { criativo_id: d.id, variavel_id: b.variavel_id, papel: b.papel });
        toast(`${b.variavel_id} marcada.`); recarregar();
      } : null,
    });
  });
  $("#vars").addEventListener("click", async (e) => {
    const rm = e.target.dataset.rm; if (!rm) return;
    try { await api("/api/criativo_variaveis", { criativo_id: d.id, variavel_id: rm, remover: true }); recarregar(); }
    catch (er) { toast(er.message); }
  });

  // --- oferta
  const semOfertas = `<p class="muted">Nenhuma oferta cadastrada. Crie uma em <a href="#/ofertas"><b>Marcas e ofertas</b></a>.</p>`;
  $("#of-trocar")?.addEventListener("click", () => modal({
    titulo: "Trocar oferta", sub: nomeC(d.id), botao: "Trocar",
    corpo: CATALOGO.ofertas.length ? `<div class="modal-campos">${campo("Oferta", `<select name="oferta_id">${ofertasOpc(d.oferta_id)}</select>`, "inteiro")}</div>` : semOfertas,
    aoSalvar: CATALOGO.ofertas.length ? async (b) => {
      await api("/api/criativos/registrar", { id: d.id, oferta_id: b.oferta_id });
      toast("Oferta trocada."); CACHE = null; await carregarCatalogo(); recarregar();
    } : null,
  }));
  $("#btn-reg")?.addEventListener("click", () => modal({
    titulo: "Definir oferta", sub: `${nomeC(d.id)} entra no banco com estes dados`, botao: "Registrar",
    corpo: CATALOGO.ofertas.length ? `<div class="modal-campos">
        ${campo("Oferta", `<select name="oferta_id">${ofertasOpc("")}</select>`, "inteiro")}
        ${campo("Processo", `<select name="processo"><option value="replica">Réplica</option><option value="modelagem">Modelagem</option></select>`)}
        ${campo("Tipo", `<select name="tipo"><option value="video" ${d.tipo === "video" ? "selected" : ""}>Vídeo</option><option value="nativo" ${d.tipo === "nativo" ? "selected" : ""}>Nativo</option><option value="imagem" ${d.tipo === "imagem" ? "selected" : ""}>Imagem</option></select>`)}
        ${campo("Formato", `<input name="formato" value="${esc(d.formato || "")}" placeholder="Lo-fi, Narrado…">`)}
        ${campo("Idioma", `<input name="idioma" value="fr" maxlength="5">`)}
        ${campo("Status", `<select name="status">${Object.entries(STATUS).map(([k, v]) => `<option value="${k}" ${k === d.status ? "selected" : ""}>${v}</option>`).join("")}</select>`, "inteiro")}
      </div>` : semOfertas,
    aoSalvar: CATALOGO.ofertas.length ? async (b) => {
      await api("/api/criativos/registrar", { id: d.id, ...b });
      toast(`${nomeC(d.id)} registrado na oferta ${b.oferta_id}.`); CACHE = null; await carregarCatalogo(); recarregar();
    } : null,
  }));

  // --- número manual
  $("#btn-num").addEventListener("click", () => {
    const cps = [["periodo_inicio", "De", "date"], ["periodo_fim", "Até", "date"], ["moeda", "Moeda", "text"], ["gasto", "Gasto", "number"], ["impressoes", "Impressões", "number"], ["views_3s", "Views de 3 s", "number"], ["cliques_link", "Cliques no link", "number"], ["compras", "Compras", "number"], ["receita", "Receita", "number"]];
    modal({
      titulo: "Lançar número manual", sub: `${nomeC(d.id)} · para quando o número não vem pela API da Meta. Mesmo período sobrescreve.`, botao: "Gravar número",
      corpo: `<div class="modal-campos tres">${cps.map(([k, r, t]) => campo(r, `<input name="${k}" type="${t}" ${t === "number" ? 'step="any" min="0" inputmode="decimal"' : ""} ${k === "moeda" ? `value="${esc(MOEDA)}" maxlength="3"` : ""}>`)).join("")}</div>`
        + (d.manuais.length ? `<p class="small muted" style="margin:12px 0 0">Já lançados: ${d.manuais.map((r) => `${r.periodo_inicio} a ${r.periodo_fim}`).join(" · ")}</p>` : ""),
      aoSalvar: async (b) => {
        if (!b.periodo_inicio || !b.periodo_fim) throw new Error("Preencha o período (De e Até).");
        const body = { criativo_id: d.id };
        cps.forEach(([k, , t]) => (body[k] = b[k] === "" ? null : t === "number" ? +b[k] : b[k]));
        await api("/api/resultado", body); toast("Número gravado."); recarregar();
      },
    });
  });
}

// ------------------------------------------------------------ métricas (todos os criativos)
async function telaMetricas(vivo) {
  if (!temDados("/api/criativos")) app.innerHTML = cabeca("Métricas", "Carregando…");
  const d = await listaRapida(vivo, () => telaMetricas(vivo));
  if (!vivo()) return;
  let ord = prefs.get("ordMetricas", { k: "compras", asc: false });
  let todos = false;
  const sel = new Set();
  const atalhos = [["compras", "Mais compras"], ["cpa", "Menor CPA"], ["roas", "Maior ROAS"], ["ctr", "Maior CTR"], ["gancho", "Gancho mais forte"], ["retencao50", "Mais retenção"]];
  const asc = (k) => k === "cpa" || k === "cpm" || k === "id";
  const base = d.criativos.filter(noEscopo), md = mediaDe(base);
  app.innerHTML = cabeca("Métricas", `${escopoAtivo() ? `<b>${esc(rotuloEscopo())}</b> · ` : ""}Criativos com números da Meta ou manuais · média de ${md.criativos} criativo(s) do escopo`,
    filtroEscopo() + `<button class="btn primario" id="btn-comp" disabled>${ICONE.comparar}Comparar</button>`)
    + `<div class="barra-ferramentas">
      <div class="segmentado" id="atalhos">${atalhos.map(([k, r]) => `<button data-v="${k}">${r}</button>`).join("")}</div>
      <label class="chave direita"><input type="checkbox" id="m-todos"><span class="trilho"></span>Mostrar sem números</label>
    </div>
    <div class="tabela-wrap"><table id="tab" class="tabela-padrao"></table></div>
    <p class="small muted">Verde é melhor que a média do escopo, vermelho é pior. Passe o mouse na prévia para ver o vídeo. Marque 2 a 4 para comparar.</p>`;
  const cols = [{ k: "id", rot: "Criativo", esq: true }, ...METRICAS];
  const desenhar = () => {
    let l = base.filter((c) => todos || c.metricas.tem_dados).map((c) => ({ ...c.metricas, id: c.id, c }));
    l.sort((a, b) => {
      const x = a[ord.k], y = b[ord.k];
      if (x == null && y == null) return 0; if (x == null) return 1; if (y == null) return -1;
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * (ord.asc ? 1 : -1);
    });
    const maxRoas = Math.max(...l.map((r) => r.roas || 0), 0.0001);
    $("#tab").innerHTML = `<thead><tr><th></th><th class="previa">Prévia</th>${cols.map((c) => `<th data-k="${c.k}" class="${c.esq ? "esq" : ""} ${ord.k === c.k ? "ord" + (ord.asc ? " asc" : "") : ""}">${c.rot}</th>`).join("")}</tr></thead>
      <tbody>
        <tr class="media"><td></td><td></td><td class="esq">Média por criativo</td>${METRICAS.map((x) => `<td>${F[x.f](md[x.k])}</td>`).join("")}</tr>
        ${l.map((r, i) => `<tr class="entra" style="--i:${Math.min(i, 20)}">
          <td><input type="checkbox" data-sel="${r.id}" ${sel.has(r.id) ? "checked" : ""}></td>
          ${celulaPrevia(r.c)}${celulaNome(r.c)}
          ${METRICAS.map((x) => {
            const c = compara(r[x.k], md[x.k], x.melhor);
            const val = `<span class="${c.cls}">${c.seta ? `<span class="small">${c.seta}</span> ` : ""}${F[x.f](r[x.k])}</span>`;
            return x.k === "roas" ? `<td><div class="celula-barra">${val}<span class="b"><i style="width:${((r.roas || 0) / maxRoas) * 100}%"></i></span></div></td>` : `<td>${val}</td>`;
          }).join("")}
        </tr>`).join("")}
      </tbody>`;
    if (!l.length) $("#tab").insertAdjacentHTML("beforeend", `<tbody><tr><td colspan="${cols.length + 2}">${vazio("Nenhum criativo com números ainda. Configure a Meta (META.md) ou lance números no detalhe do criativo.")}</td></tr></tbody>`);
  };
  $("#tab").addEventListener("click", (e) => {
    const th = e.target.closest("th[data-k]");
    if (th) { const k = th.dataset.k; ord = { k, asc: ord.k === k ? !ord.asc : asc(k) }; prefs.set("ordMetricas", ord); desenhar(); }
  });
  $("#tab").addEventListener("change", (e) => {
    const id = e.target.dataset.sel; if (!id) return;
    e.target.checked ? sel.add(id) : sel.delete(id);
    $("#btn-comp").disabled = sel.size < 2; $("#btn-comp").innerHTML = `${ICONE.comparar}Comparar${sel.size ? ` (${sel.size})` : ""}`;
  });
  segmentado($("#atalhos"), atalhos.some(([k]) => k === ord.k) ? ord.k : "", (k) => { ord = { k, asc: asc(k) }; prefs.set("ordMetricas", ord); desenhar(); });
  $("#m-todos").addEventListener("change", (e) => { todos = e.target.checked; desenhar(); });
  $("#btn-comp").addEventListener("click", () => { location.hash = "#/comparar/" + [...sel].slice(0, 4).join(","); });
  desenhar();
}

// ------------------------------------------------------------ comparar
async function telaComparar(ids, vivo) {
  ids = ids.slice(0, 4);
  app.innerHTML = cabeca("Comparar", `Carregando ${ids.map(nomeC).join(", ")}…`);
  const ds = await Promise.all(ids.map((id) => swr("/api/criativos/" + id)));
  await listaRapida();
  if (!vivo()) return;
  const cores = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)"];
  const media = mediaDe(doEscopo());
  const barras = METRICAS.map((x) => {
    const vals = ds.map((d) => d.metricas[x.k]);
    const max = Math.max(...vals.filter((v) => v != null), media[x.k] || 0) || 1;
    const validos = vals.filter((v) => v != null);
    const melhor = x.melhor && validos.length > 1 ? (x.melhor === "alto" ? Math.max(...validos) : Math.min(...validos)) : null;
    return `<div class="caixa spot" style="margin:0"><h2>${x.rot}<span class="direita">média ${F[x.f](media[x.k])}</span></h2>
      ${ds.map((d, i) => `<div class="barra" style="--c:${cores[i]}"><b>#${d.id.slice(1)}${vals[i] != null && vals[i] === melhor ? " ★" : ""}</b>
        <div class="trilho"><div class="enche" style="width:${vals[i] == null ? 0 : (vals[i] / max) * 100}%"></div></div><span class="num" style="text-align:right">${F[x.f](vals[i])}</span></div>`).join("")}
    </div>`;
  }).join("");
  app.innerHTML = `<a class="voltar" href="#/metricas">${ICONE.voltar}Métricas</a>`
    + cabeca(`Comparando ${ds.map((d) => "#" + d.id.slice(1)).join(" × ")}`, `★ = melhor do grupo · média de ${esc(rotuloEscopo())}. Com pouco gasto a diferença pode ser acaso.`, `<button class="btn" id="tocar">${ICONE.play}Tocar todos juntos</button>`)
    + `<div class="comp-cards" style="grid-template-columns:repeat(${ds.length}, minmax(150px, 230px));margin-bottom:16px">
        ${ds.map((d, i) => `<a class="comp-card entra" style="--i:${i}" href="#/c/${d.id}"><div class="thumb" style="--c:${cores[i]}">${d.capa_video ? `<video src="${d.capa_video}" muted playsinline preload="metadata" poster="${capaDe(d, 360)}"></video>` : capaDe(d) ? `<img src="${capaDe(d, 360)}" alt="">` : `<div class="sem-midia">sem mídia</div>`}<div class="vinheta"></div>${tagsDe(d, { curto: true })}<div class="base"><div class="id">${nomeC(d.id)}</div><div class="fmt">${esc(d.formato || "")}</div></div></div></a>`).join("")}
      </div>
      <div class="caixa"><h2>Retenção</h2>${graficoRetencao([
        ...ds.map((d, i) => ({ nome: "#" + d.id.slice(1), cor: cores[i], pontos: pontosCurva(d.metricas, null) })),
        { nome: "Média", cor: "var(--ref)", ref: true, pontos: pontosCurva(media, null) },
      ])}</div>
      <div class="comparar spot-area">${barras}</div>`;
  $("#tocar").addEventListener("click", () => {
    const vs = $$(".comp-card video"); const tocando = vs.some((v) => !v.paused);
    vs.forEach((v) => { if (tocando) v.pause(); else { v.currentTime = 0; v.play(); } });
    $("#tocar").innerHTML = tocando ? `${ICONE.play}Tocar todos juntos` : "Pausar";
  });
}

// ------------------------------------------------------------ variáveis
async function telaVariaveis(vivo) {
  if (!temDados("/api/variaveis")) app.innerHTML = cabeca("Variáveis", "Carregando…");
  const re = () => telaVariaveis(vivo);
  const [todas] = await Promise.all([variaveisLib(vivo, re), listaRapida(vivo, re)]);
  if (!vivo()) return;
  // Escopo: variáveis da marca escolhida; números só dos criativos do escopo.
  const marca = ESCOPO.marca && ESCOPO.marca !== SEM ? ESCOPO.marca : "";
  const vars = todas.filter((v) => !marca || v.marca_id === marca);
  const media = mediaDe(doEscopo());
  let ord = { k: "categoria", asc: true };
  const metr = METRICAS.filter((x) => ["gasto", "compras", "cpa", "roas", "ctr", "gancho", "thruplay"].includes(x.k));
  const cols = [{ k: "variavel_id", rot: "ID", esq: true }, { k: "valor", rot: "Variável", esq: true }, { k: "status", rot: "Status", esq: true }, { k: "criativos", rot: "Criativos" }, ...metr];
  app.innerHTML = cabeca("Variáveis", `${escopoAtivo() ? `<b>${esc(rotuloEscopo())}</b> · ` : ""}${vars.length} variáveis na biblioteca`, filtroEscopo())
    + `<div class="aviso">A marca escolhe quais variáveis aparecem; produto e oferta só mudam os números. Cada linha soma os criativos marcados com a variável (botão "Marcar variável" no detalhe do criativo), só dentro do escopo. Com 1 criativo ou poucas impressões, não decide nada. Winner só com número contra o controle (MODELAGEM.md).</div>
    <div class="tabela-wrap"><table id="tab" class="tabela-padrao"></table></div>`;
  // Números da variável recalculados com os criativos do escopo.
  const linhas = vars.map((v) => {
    const cs = v.criativos_ids.map((x) => porId(x.id)).filter(noEscopo);
    const m = mediaDe(cs), n = m.criativos;
    const soma = (k) => cs.reduce((s, c) => s + ((c.metricas.brutos || {})[k] || 0), 0);
    return { ...v, cs, criativos: cs.length, m: { ...m, gasto: soma("gasto"), compras: soma("compras"), tem_dados: n > 0 } };
  });
  const val = (v, k) => (["variavel_id", "status", "criativos"].includes(k) ? v[k] : k === "valor" ? v.categoria + v.variavel + v.valor : v.m[k]);
  const desenhar = () => {
    const l = [...linhas].sort((a, b) => {
      const x = val(a, ord.k), y = val(b, ord.k);
      if (x == null && y == null) return 0; if (x == null) return 1; if (y == null) return -1;
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * (ord.asc ? 1 : -1);
    });
    $("#tab").innerHTML = `<thead><tr><th class="previa">Prévia</th>${cols.map((c) => `<th data-k="${c.k}" class="${c.esq ? "esq" : ""} ${ord.k === c.k ? "ord" + (ord.asc ? " asc" : "") : ""}">${c.rot}</th>`).join("")}</tr></thead>
      <tbody>${l.map((v, i) => `<tr class="entra" style="--i:${Math.min(i, 20)}">
        <td class="previa">${v.cs.length ? `<div class="pilha">${v.cs.slice(0, 3).map((c) => `<a href="#/c/${c.id}">${miniImg(c, "")}</a>`).join("")}${v.cs.length > 3 ? `<span class="mais">+${v.cs.length - 3}</span>` : ""}</div>` : `<span class="mini"></span>`}</td>
        <td class="esq"><b>${v.variavel_id}</b></td>
        <td class="esq"><div class="celula-nome" style="max-width:420px"><span class="muted small">${esc(v.categoria)} · ${esc(v.variavel)}</span><span class="clamp" title="${esc(v.valor)}">${esc(v.valor)}</span></div></td>
        <td class="esq"><span class="badge st-${v.status}" style="color:inherit"><span class="st-${v.status}">${v.status}</span></span></td>
        <td>${v.criativos || `<span class="muted">0</span>`}</td>
        ${metr.map((x) => { const c = ["gasto", "compras"].includes(x.k) ? { cls: "" } : compara(v.m[x.k], media[x.k], x.melhor); return `<td class="${v.m.tem_dados ? c.cls : ""}">${v.m.tem_dados ? F[x.f](v.m[x.k]) : `<span class="muted">–</span>`}</td>`; }).join("")}
      </tr>`).join("") || `<tr><td colspan="${cols.length + 1}">${vazio("Nenhuma variável para esta marca.")}</td></tr>`}</tbody>`;
  };
  $("#tab").addEventListener("click", (e) => { const th = e.target.closest("th[data-k]"); if (th) { ord = { k: th.dataset.k, asc: ord.k === th.dataset.k ? !ord.asc : ["variavel_id", "valor", "status", "cpa"].includes(th.dataset.k) }; desenhar(); } });
  desenhar();
}

// ------------------------------------------------------------ anúncios
async function telaAnuncios(vivo) {
  if (!temDados("/api/anuncios")) app.innerHTML = cabeca("Anúncios", "Carregando…");
  const re = () => telaAnuncios(vivo);
  const [a, l] = await Promise.all([swr("/api/anuncios", vivo, re), listaRapida(vivo, re)]);
  if (!vivo()) return;
  // Escopo: anúncios ligados a criativos do escopo + os que ainda não têm criativo (para ligar).
  const lista = a.anuncios.filter((x) => !x.criativo_id || noEscopo(porId(x.criativo_id)) || !escopoAtivo());
  const opcoes = l.criativos.filter((c) => !escopoAtivo() || noEscopo(c));
  const sem = lista.filter((x) => !x.criativo_id).length;
  app.innerHTML = cabeca("Anúncios", `${escopoAtivo() ? `<b>${esc(rotuloEscopo())}</b> · ` : ""}${lista.length} anúncio(s) · ${sem} sem criativo`, filtroEscopo())
    + `<div class="aviso">O anúncio liga sozinho quando o nome começa com o ID do criativo ("C19 | ..."). Os outros, clique em "Ligar". A ligação manual não é desfeita pela sincronização.</div>
    <div class="tabela-wrap"><table class="tabela-padrao">
      <thead><tr><th class="previa">Prévia</th><th class="esq">Criativo</th><th class="esq">Anúncio</th><th class="esq">Campanha</th><th>Status</th><th>Gasto</th><th></th></tr></thead>
      <tbody>${lista.map((x, i) => { const c = porId(x.criativo_id); return `<tr class="entra" style="--i:${Math.min(i, 20)}">
        ${celulaPrevia(c)}
        ${c ? celulaNome(c) : `<td class="esq"><span class="badge em_producao">sem criativo</span></td>`}
        <td class="esq"><div class="celula-nome"><span class="clamp">${esc(x.nome)}</span><span class="muted small">${x.ad_id}</span></div></td>
        <td class="esq"><span class="clamp sec" style="max-width:240px">${esc(x.campanha_nome || "")}</span></td><td>${esc(x.status || "")}</td><td>${F.money(x.gasto)}</td>
        <td><button class="btn mini ${c ? "" : "primario"}" data-ligar="${esc(x.ad_id)}">${ICONE.link}${c ? "Trocar" : "Ligar"}</button></td></tr>`; }).join("")
        || `<tr><td colspan="7">${vazio("Nenhum anúncio sincronizado. Configure a Meta (META.md) e clique em Sincronizar.")}</td></tr>`}</tbody>
    </table></div>`;
  app.onclick = (e) => {
    const b = e.target.closest("[data-ligar]"); if (!b) return;
    const x = lista.find((y) => y.ad_id === b.dataset.ligar);
    const rot = (o) => `${nomeC(o.id)}${o.oferta_id ? " · " + o.oferta_id : ""}${o.formato ? " · " + o.formato : ""}`;
    const opc = (l) => `<option value="">— sem criativo —</option>` + l.map((o) => `<option value="${o.id}" ${o.id === x.criativo_id ? "selected" : ""}>${esc(rot(o))}</option>`).join("");
    modal({
      titulo: x.criativo_id ? "Trocar criativo do anúncio" : "Ligar anúncio a um criativo", sub: esc(x.nome), botao: "Ligar",
      corpo: `<div class="modal-campos">
          ${campo("Buscar", `<input id="lg-busca" placeholder="#19, oferta, formato" autocomplete="off">`, "inteiro")}
          ${campo("Criativo", `<select name="criativo_id" size="8">${opc(opcoes)}</select>`, "inteiro")}
        </div>${escopoAtivo() ? `<p class="small muted" style="margin:10px 0 0">Mostrando só os criativos de <b>${esc(rotuloEscopo())}</b>.</p>` : ""}`,
      aoAbrir: (f) => {
        const sel = $('[name="criativo_id"]', f);
        if (sel.selectedIndex < 0) sel.selectedIndex = 0;
        $("#lg-busca", f).addEventListener("input", (ev) => {
          const q = ev.target.value.trim().toLowerCase().replace(/^#/, "");
          sel.innerHTML = opc(opcoes.filter((o) => (rot(o) + " " + o.id).toLowerCase().includes(q)));
        });
      },
      aoSalvar: async (r) => {
        await api("/api/ligar", { ad_id: x.ad_id, criativo_id: r.criativo_id || null });
        toast(`Anúncio ligado a ${r.criativo_id ? nomeC(r.criativo_id) : "nenhum"}.`); CACHE = null; telaAnuncios(vivo);
      },
    });
  };
}

// ------------------------------------------------------------ produção (quadro da esteira)
let PAN = null;                       // arrasto do fundo do quadro (ouvintes da janela registrados uma vez só)
window.addEventListener("pointermove", (e) => {
  if (!PAN) return;
  const dx = e.clientX - PAN.x;
  if (!PAN.moveu && Math.abs(dx) < 4) return;
  PAN.moveu = true; PAN.q.classList.add("puxando"); PAN.q.scrollLeft = PAN.s - dx;
});
window.addEventListener("pointerup", () => { if (PAN) { PAN.q.classList.remove("puxando"); PAN = null; } });

async function telaProducao(vivo) {
  if (!temDados("/api/criativos")) app.innerHTML = cabeca("Produção", "Carregando…");
  const d = await listaRapida(vivo, () => telaProducao(vivo));
  if (!vivo()) return;
  let vez = prefs.get("vezProducao", "");
  const naEsteira = d.criativos.filter((c) => c.esteira && noEscopo(c));
  // Refação de criativo já pronto (ex.: no ar): continua na Biblioteca, mas aparece aqui até o Claude refazer.
  const refacao = d.criativos.filter((c) => !c.esteira && (c.anotacoes.pedida || 0) > 0 && noEscopo(c));
  const comVoce = naEsteira.filter((c) => c.esteira.aguardando === "dono").length;
  app.innerHTML = cabeca("Produção", `${escopoAtivo() ? `<b>${esc(rotuloEscopo())}</b> · ` : ""}${naEsteira.length} criativo(s) em produção · <b>${comVoce} aguardando você</b>`, filtroEscopo())
    + `<div class="barra-ferramentas">
        <div class="segmentado" id="p-vez"><button data-v="">Todos</button><button data-v="dono">Aguardando você</button><button data-v="claude">Com o Claude</button></div>
        <span class="small muted direita">Clique no card para revisar e aprovar. Arraste para mudar de etapa. No Claude Code: <b>"continue a esteira"</b>.</span>
      </div>
      <div class="quadro-esteira" id="quadro"></div>`;
  const cartao = (c) => {
    const e = c.esteira || {}, aj = c.anotacoes.pedida || 0, capa = capaDe(c, 120);
    const selo = !c.esteira ? `<span class="selo refacao">refação</span>` : e.aguardando === "dono" ? `<span class="selo dono">aguardando você</span>` : `<span class="selo claude">com o Claude</span>`;
    // Cinco linhas fixas: nome, vez, formato, tags, rodapé. O CSS corta o excesso: todo card tem o mesmo tamanho.
    return `<a class="kcard ${e.aguardando === "dono" ? "vez-dono" : ""}" href="#/c/${c.id}" draggable="${c.esteira ? "true" : "false"}" data-id="${c.id}" title="${esc(nomeC(c.id) + (c.formato ? " · " + c.formato : ""))}">
      <div class="kthumb">${capa ? `<img src="${capa}" loading="lazy" alt="" draggable="false">` : ""}</div>
      <div class="kcorpo">
        <div class="klinha"><b>${nomeC(c.id)}</b>${aj ? `<span class="aj" title="Ajustes pedidos">${aj} ajuste${aj > 1 ? "s" : ""}</span>` : ""}</div>
        <div>${selo}</div>
        <div class="small sec">${esc(c.formato || (c.tipo === "video" ? "vídeo" : "nativo"))}${c.processo ? " · " + (c.processo === "modelagem" ? "Modelagem" : "Réplica") : ""}</div>
        ${tagsDe(c, { curto: true, max: 26 })}
        <div class="kpe">${[ha(e.desde), usd(e.custo_usd), e.inferida ? `<span title="Etapa deduzida pelos arquivos da pasta">≈ etapa deduzida</span>` : ""].filter(Boolean).join(" · ") || "&nbsp;"}</div>
      </div></a>`;
  };
  const desenhar = () => {
    const filtra = (l) => l.filter((c) => !vez || (c.esteira ? c.esteira.aguardando === vez : vez === "claude"));
    const colunas = [];
    if (refacao.length) colunas.push({ k: "refacao", rot: "Refação", sub: "já prontos, com ajuste pedido", cs: filtra(refacao) });
    ETAPAS.forEach((k) => colunas.push({ k, rot: k === "roteiro" ? "Roteiro / texto" : ROT_ETAPA[k], cs: filtra(naEsteira.filter((c) => c.esteira.etapa === k)) }));
    $("#quadro").innerHTML = colunas.map((col) => {
      const nDono = col.cs.filter((c) => c.esteira && c.esteira.aguardando === "dono").length;
      return `<section class="kcoluna" data-etapa="${col.k}">
        <header><b>${col.rot}</b><span class="n">${col.cs.length}</span>${nDono ? `<span class="n dono" title="Aguardando você">${nDono}</span>` : ""}${col.sub ? `<small>${col.sub}</small>` : ""}</header>
        <div class="kcards">${col.cs.map(cartao).join("") || `<div class="kvazio">—</div>`}</div></section>`;
    }).join("");
  };
  segmentado($("#p-vez"), vez, (v) => { vez = v; prefs.set("vezProducao", v); desenhar(); });
  desenhar();
  const q = $("#quadro");
  // Arrastar o fundo do quadro (fora dos cards) rola para o lado, como no Trello.
  q.addEventListener("pointerdown", (e) => {
    if (e.button !== 0 || e.target.closest(".kcard, button, a, select, input")) return;
    PAN = { q, x: e.clientX, s: q.scrollLeft, moveu: false };
  });
  // Roda do mouse no cabeçalho das colunas também rola para o lado.
  q.addEventListener("wheel", (e) => { if (e.target.closest(".kcoluna > header") && Math.abs(e.deltaY) > Math.abs(e.deltaX)) { e.preventDefault(); q.scrollLeft += e.deltaY; } }, { passive: false });
  // Arrastar um card entre colunas = mover de etapa (mantém com quem está a vez).
  let arrastando = null;
  q.addEventListener("dragstart", (e) => { const k = e.target.closest(".kcard"); if (!k) return; arrastando = k.dataset.id; e.dataTransfer.effectAllowed = "move"; k.classList.add("arrastando"); });
  q.addEventListener("dragend", (e) => { e.target.closest(".kcard")?.classList.remove("arrastando"); $$(".kcoluna", q).forEach((c) => c.classList.remove("alvo")); });
  q.addEventListener("dragover", (e) => { const col = e.target.closest(".kcoluna"); if (!arrastando || !col || col.dataset.etapa === "refacao") return; e.preventDefault(); $$(".kcoluna", q).forEach((c) => c.classList.toggle("alvo", c === col)); });
  q.addEventListener("drop", async (e) => {
    const col = e.target.closest(".kcoluna"); if (!arrastando || !col || col.dataset.etapa === "refacao") return;
    e.preventDefault();
    const c = porId(arrastando); arrastando = null;
    if (!c || c.esteira.etapa === col.dataset.etapa) return desenhar();
    try {
      await api("/api/esteira", { criativo_id: c.id, acao: "mover", etapa: col.dataset.etapa, aguardando: c.esteira.aguardando });
      toast(`${nomeC(c.id)} movido para ${rotEtapa(col.dataset.etapa, c.tipo)}.`); telaProducao(vivo);
    } catch (er) { toast(er.message, 6000); desenhar(); }
  });
}

// ------------------------------------------------------------ marcas, produtos e ofertas
async function telaOfertas(vivo) {
  if (!temDados("/api/catalogo")) app.innerHTML = cabeca("Marcas e ofertas", "Carregando…");
  const re = () => telaOfertas(vivo);
  await Promise.all([carregarCatalogo(vivo, re), listaRapida(vivo, re)]);
  if (!vivo()) return;
  const { marcas, produtos, ofertas } = CATALOGO;
  const crOf = (id) => CACHE.criativos.filter((c) => c.oferta_id === id);
  const semOferta = CACHE.criativos.filter((c) => !c.oferta_id);
  const linhaOferta = (o) => {
    const cs = crOf(o.id), m = mediaDe(cs);
    return `<tr class="entra">
      <td class="previa">${cs.length ? `<div class="pilha">${cs.slice(0, 3).map((c) => `<a href="#/c/${c.id}">${miniImg(c, "")}</a>`).join("")}${cs.length > 3 ? `<span class="mais">+${cs.length - 3}</span>` : ""}</div>` : `<span class="mini"></span>`}</td>
      <td class="esq"><div class="celula-nome"><b>${esc(o.id)}</b><span class="sec clamp">${esc(o.nome)}</span></div></td>
      <td class="esq"><span class="badge ${o.status === "ativa" ? "no_ar" : "pausado"}">${o.status}</span></td>
      <td class="esq">${esc(o.pais)} · ${esc(o.idioma)}</td>
      <td>${cs.length}</td><td>${F.money(cs.reduce((s, c) => s + (c.metricas.gasto || 0), 0))}</td><td>${F.int(cs.reduce((s, c) => s + (c.metricas.compras || 0), 0))}</td><td>${F.x(m.roas)}</td>
      <td><div class="acoes-linha"><button class="btn mini fantasma" data-editar-oferta="${esc(o.id)}">${ICONE.lapis}Editar</button><button class="btn mini" data-escopo="${esc(o.id)}">${ICONE.filtro}Ver criativos</button></div></td></tr>`;
  };
  const semMarca = !marcas.length, semProduto = !produtos.length;
  app.innerHTML = cabeca("Marcas e ofertas", "Marca › produto › oferta. Todo criativo pertence a uma oferta; o filtro de escopo de cada tela usa esta árvore.",
      `<button class="btn" data-nova="marca">${ICONE.mais}Nova marca</button>
       <button class="btn" data-nova="produto" ${semMarca ? "disabled title='Crie uma marca antes'" : ""}>${ICONE.mais}Novo produto</button>
       <button class="btn primario" data-nova="oferta" ${semProduto ? "disabled title='Crie um produto antes'" : ""}>${ICONE.mais}Nova oferta</button>`)
    + (semOferta.length ? `<div class="aviso">${semOferta.length} criativo(s) sem oferta: ${semOferta.slice(0, 12).map((c) => `<a href="#/c/${c.id}"><b>#${c.id.slice(1)}</b></a>`).join(", ")}${semOferta.length > 12 ? "…" : ""}. Abra cada um e clique em "Definir oferta".</div>` : "")
    + `<div class="arvore">${marcas.map((mc) => `
      <div class="caixa"><h2><span class="tag marca"><i></i>${esc(mc.nome)}</span><span class="muted small">prefixo ${esc(mc.prefixo)}</span>
        <span class="acoes-linha direita"><button class="btn mini fantasma" data-editar-marca="${esc(mc.id)}">${ICONE.lapis}Editar</button><button class="btn mini fantasma" data-nova="produto" data-marca="${esc(mc.id)}">${ICONE.mais}Produto</button><button class="btn mini" data-escopo-marca="${esc(mc.id)}">${ICONE.filtro}Ver criativos</button></span></h2>
        ${produtos.filter((p) => p.marca_id === mc.id).map((p) => `
          <div class="produto"><div class="produto-cabeca"><span class="tag produto"><i></i>${esc(p.nome)}</span><span class="muted small">${esc(p.id)}</span>
              <span class="acoes-linha direita"><button class="btn mini fantasma" data-editar-produto="${esc(p.id)}">${ICONE.lapis}Editar</button><button class="btn mini fantasma" data-nova="oferta" data-marca="${esc(mc.id)}" data-produto="${esc(p.id)}">${ICONE.mais}Oferta</button></span></div>
            <div class="tabela-wrap"><table class="tabela-padrao"><thead><tr><th class="previa">Prévia</th><th class="esq">Oferta</th><th class="esq">Status</th><th class="esq">Mercado</th><th>Criativos</th><th>Gasto</th><th>Compras</th><th>ROAS</th><th></th></tr></thead>
              <tbody>${ofertas.filter((o) => o.produto_id === p.id).map(linhaOferta).join("") || `<tr><td colspan="9" class="esq muted small">Nenhuma oferta para este produto.</td></tr>`}</tbody></table></div>
          </div>`).join("") || `<p class="muted small">Nenhum produto.</p>`}
      </div>`).join("") || vazio("Nenhuma marca ainda. Clique em Nova marca.")}</div>
    <p class="small muted">Promessa, avatar, garantia e funil continuam pelo portão de contexto (<code>tools/dados.py contexto</code>): o Claude pergunta o que faltar antes do primeiro criativo.</p>`;

  const salvar = (tipo) => async (b) => { await api("/api/catalogo/" + tipo, b); toast("Salvo."); await carregarCatalogo(); telaOfertas(vivo); };
  const opcMarcas = (sel) => marcas.map((m) => `<option value="${esc(m.id)}" ${m.id === sel ? "selected" : ""}>${esc(m.nome)}</option>`).join("");
  const opcProdutos = (mk, sel) => produtos.filter((p) => p.marca_id === mk).map((p) => `<option value="${esc(p.id)}" ${p.id === sel ? "selected" : ""}>${esc(p.nome)}</option>`).join("");
  const travado = "readonly title='Não muda depois de criado'";

  const formMarca = (m) => modal({
    titulo: m ? `Editar marca ${esc(m.nome)}` : "Nova marca", botao: m ? "Salvar" : "Criar marca",
    corpo: `<div class="modal-campos">
      ${campo("ID (minúsculas)", `<input name="id" placeholder="cinnarae" value="${esc(m?.id || "")}" ${m ? travado : ""}>`)}
      ${campo("Prefixo dos IDs", `<input name="prefixo" placeholder="CIN" maxlength="5" value="${esc(m?.prefixo || "")}" ${m ? travado : ""} style="text-transform:uppercase">`)}
      ${campo("Nome", `<input name="nome" placeholder="Cinnarae" value="${esc(m?.nome || "")}">`, "inteiro")}
    </div><p class="small muted" style="margin:10px 0 0">O prefixo abre o ID das ofertas (CIN-FR-01).</p>`,
    aoSalvar: (b) => salvar("marca")({ ...b, prefixo: b.prefixo.toUpperCase() }),
  });
  const formProduto = (p, marcaId) => modal({
    titulo: p ? `Editar produto ${esc(p.nome)}` : "Novo produto", botao: p ? "Salvar" : "Criar produto",
    corpo: `<div class="modal-campos">
      ${campo("Marca", `<select name="marca_id" ${p ? "disabled" : ""}>${opcMarcas(p?.marca_id || marcaId)}</select>`)}
      ${campo("ID (minúsculas)", `<input name="id" placeholder="cayenne-softgels" value="${esc(p?.id || "")}" ${p ? travado : ""}>`)}
      ${campo("Nome", `<input name="nome" placeholder="Cayenne Softgels" value="${esc(p?.nome || "")}">`, "inteiro")}
      ${campo("Descrição (opcional)", `<textarea name="descricao" rows="3">${esc(p?.descricao || "")}</textarea>`, "inteiro")}
    </div>`,
    aoSalvar: salvar("produto"),
  });
  const formOferta = (o, marcaId, produtoId) => {
    const mk = o?.marca_id || marcaId || marcas[0]?.id;
    const st = o?.status || "ativa";
    modal({
      titulo: o ? `Editar oferta ${esc(o.id)}` : "Nova oferta", botao: o ? "Salvar" : "Criar oferta",
      sub: o ? "Marca, produto, ID, país e idioma ficam fixos depois de criados." : "",
      corpo: `<div class="modal-campos">
        ${campo("Marca", `<select name="marca_id" ${o ? "disabled" : ""}>${opcMarcas(mk)}</select>`)}
        ${campo("Produto", `<select name="produto_id" ${o ? "disabled" : ""}>${opcProdutos(mk, o?.produto_id || produtoId)}</select>`)}
        ${campo("País", `<input name="pais" placeholder="FR" maxlength="2" value="${esc(o?.pais || "")}" ${o ? travado : ""} style="text-transform:uppercase">`)}
        ${campo("Idioma", `<input name="idioma" placeholder="fr" maxlength="5" value="${esc(o?.idioma || "")}" ${o ? travado : ""}>`)}
        ${campo("ID", `<input name="id" placeholder="CIN-FR-02" value="${esc(o?.id || "")}" ${o ? travado : ""} style="text-transform:uppercase">`)}
        ${campo("Moeda", `<input name="moeda" maxlength="3" value="${esc(o?.moeda || "EUR")}" style="text-transform:uppercase">`)}
        ${campo("Nome", `<input name="nome" placeholder="França Black Friday" value="${esc(o?.nome || "")}">`, "inteiro")}
        ${campo("Status", `<select name="status">${["ativa", "pausada", "encerrada"].map((s) => `<option value="${s}" ${s === st ? "selected" : ""}>${s}</option>`).join("")}</select>`)}
        ${campo("Oferta atual", `<input name="oferta_atual" placeholder="-20% na 1ª compra" value="${esc(o?.oferta_atual || "")}">`)}
      </div>`,
      aoAbrir: (f) => {
        if (o) return;
        const sm = $('[name="marca_id"]', f), sp = $('[name="produto_id"]', f), pais = $('[name="pais"]', f), id = $('[name="id"]', f);
        // Sugere o próximo ID livre: PREFIXO-PAÍS-NN.
        const sugerir = () => {
          const pre = (marcas.find((m) => m.id === sm.value) || {}).prefixo || "XXX", pa = (pais.value || "FR").toUpperCase();
          const usados = ofertas.map((x) => x.id).filter((x) => x.startsWith(`${pre}-${pa}-`)).map((x) => +x.slice(-2));
          id.placeholder = `${pre}-${pa}-${String((usados.length ? Math.max(...usados) : 0) + 1).padStart(2, "0")}`;
        };
        sm.addEventListener("change", () => { sp.innerHTML = opcProdutos(sm.value); sugerir(); });
        pais.addEventListener("input", sugerir); sugerir();
        id.addEventListener("focus", () => { if (!id.value) id.value = id.placeholder; });
      },
      aoSalvar: (b) => {
        if (!b.produto_id) throw new Error("Essa marca ainda não tem produto. Crie o produto antes.");
        return salvar("oferta")({ ...b, id: b.id.toUpperCase(), pais: b.pais.toUpperCase(), moeda: b.moeda.toUpperCase() });
      },
    });
  };

  app.onclick = (e) => {
    const alvo = (s) => e.target.closest(s);
    let el;
    if ((el = alvo("[data-escopo]"))) { const o = ofertas.find((x) => x.id === el.dataset.escopo); definirEscopo({ marca: o.marca_id, produto: o.produto_id, oferta: o.id }); location.hash = "#/"; }
    else if ((el = alvo("[data-escopo-marca]"))) { definirEscopo({ marca: el.dataset.escopoMarca }); location.hash = "#/"; }
    else if ((el = alvo("[data-editar-marca]"))) formMarca(marcas.find((m) => m.id === el.dataset.editarMarca));
    else if ((el = alvo("[data-editar-produto]"))) formProduto(produtos.find((p) => p.id === el.dataset.editarProduto));
    else if ((el = alvo("[data-editar-oferta]"))) formOferta(ofertas.find((o) => o.id === el.dataset.editarOferta));
    else if ((el = alvo("[data-nova]"))) {
      const t = el.dataset.nova;
      if (t === "marca") formMarca();
      else if (t === "produto") formProduto(null, el.dataset.marca);
      else formOferta(null, el.dataset.marca, el.dataset.produto);
    }
  };
}

// ------------------------------------------------------------ equipe
async function telaEquipe(vivo) {
  if (!temDados("/api/usuarios")) app.innerHTML = cabeca("Equipe", "Carregando…");
  const r = await swr("/api/usuarios", vivo, () => telaEquipe(vivo));
  if (!vivo()) return;
  const data = (s) => (s ? new Date(s).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "nunca");
  app.innerHTML = cabeca("Equipe", `${r.usuarios.length} pessoa(s) com acesso. Cada anotação e nota fica com o nome de quem fez.`,
      `<button class="btn" data-senha>${ICONE.chave}Trocar minha senha</button><button class="btn primario" id="btn-user">${ICONE.mais}Novo usuário</button>`)
    + `<div class="tabela-wrap"><table class="tabela-padrao"><thead><tr><th class="previa"></th><th class="esq">Nome</th><th class="esq">E-mail</th><th class="esq">Criado</th><th class="esq">Último acesso</th><th></th></tr></thead>
      <tbody>${r.usuarios.map((u) => `<tr><td class="previa"><span class="avatar">${esc(iniciais(u.nome))}</span></td><td class="esq"><b>${esc(u.nome)}</b>${u.id === EU.id ? ` <span class="badge acento sem-ponto">você</span>` : ""}</td><td class="esq sec">${esc(u.email)}</td><td class="esq sec">${data(u.criado_em)}</td><td class="esq sec">${data(u.ultimo_login)}</td>
        <td>${u.id === EU.id ? `<button class="btn mini fantasma" data-senha>${ICONE.chave}Trocar senha</button>` : ""}</td></tr>`).join("")}</tbody></table></div>`;
  $("#btn-user").addEventListener("click", () => modal({
    titulo: "Novo usuário", sub: "Passe a senha por um canal seguro e peça para a pessoa trocar no primeiro acesso.", botao: "Criar usuário",
    corpo: `<div class="modal-campos">
      ${campo("Nome", `<input name="nome" autocomplete="off">`, "inteiro")}
      ${campo("E-mail", `<input name="email" type="email" autocomplete="off">`, "inteiro")}
      ${campo("Senha inicial (mín. 10)", `<input name="senha" type="password" autocomplete="new-password">`)}
      ${campo("Repita a senha", `<input name="conf" type="password" autocomplete="new-password">`)}
    </div>`,
    aoSalvar: async (b) => {
      if (!b.nome || !b.email) throw new Error("Preencha nome e e-mail.");
      if (b.senha !== b.conf) throw new Error("As senhas não conferem.");
      await api("/api/usuarios", { nome: b.nome, email: b.email, senha: b.senha });
      toast(`Usuário ${b.nome} criado.`); telaEquipe(vivo);
    },
  }));
  app.onclick = (e) => { if (e.target.closest("[data-senha]")) modalSenha(); };
}
function modalSenha() {
  modal({
    titulo: "Trocar minha senha", sub: EU ? esc(EU.email) : "", botao: "Trocar senha",
    corpo: `<div class="modal-campos">
      ${campo("Senha atual", `<input name="atual" type="password" autocomplete="current-password">`, "inteiro")}
      ${campo("Nova senha (mín. 10)", `<input name="nova" type="password" autocomplete="new-password">`)}
      ${campo("Repita a nova", `<input name="conf" type="password" autocomplete="new-password">`)}
    </div>`,
    aoSalvar: async (b) => {
      if (b.nova !== b.conf) throw new Error("As senhas novas não conferem.");
      await api("/api/senha", { atual: b.atual, nova: b.nova }); toast("Senha trocada.");
    },
  });
}
const iniciais = (n) => (n || "?").split(/\s+/).filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join("");
$("#btn-senha-menu").addEventListener("click", modalSenha);

// ------------------------------------------------------------ rotas
let rotaN = 0;
async function rota() {
  const n = ++rotaN, vivo = () => n === rotaN;
  const h = location.hash || "#/";
  const emProd = (id) => { const c = porId(id); return c && c.status === "em_producao"; };
  const ativo = h.startsWith("#/c/") ? (emProd(h.slice(4)) ? "#/producao" : "#/") : h.startsWith("#/comparar") ? "#/metricas" : h;
  $$("#nav a").forEach((a) => a.classList.toggle("ativo", a.getAttribute("href") === ativo));
  moverIndicador();
  espiar.classList.remove("on"); espiarId = null;
  app.onclick = null;
  // Para e descarrega os vídeos da tela anterior: senão continuam baixando em segundo plano.
  $$("video", app).forEach((v) => { v.pause(); v.removeAttribute("src"); v.load(); });
  try {
    let m;
    if ((m = h.match(/^#\/c\/(C\d{2,3})$/))) await telaCriativo(m[1], vivo);
    else if ((m = h.match(/^#\/comparar\/([C\d,]+)$/))) await telaComparar(m[1].split(","), vivo);
    else if (h === "#/metricas") await telaMetricas(vivo);
    else if (h === "#/variaveis") await telaVariaveis(vivo);
    else if (h === "#/anuncios") await telaAnuncios(vivo);
    else if (h === "#/producao") await telaProducao(vivo);
    else if (h === "#/fila") { location.replace("#/producao"); return; }
    else if (h === "#/ofertas") await telaOfertas(vivo);
    else if (h === "#/equipe") await telaEquipe(vivo);
    else await telaBiblioteca(vivo);
  } catch (e) {
    if (vivo()) app.innerHTML = `<p class="erro">Erro: ${esc(e.message)}</p>`;
  }
}
window.addEventListener("hashchange", () => { rota(); window.scrollTo(0, 0); });
window.addEventListener("resize", moverIndicador);
$("#btn-sair").addEventListener("click", async () => { try { await api("/api/logout", {}); } catch { /* já saiu */ } location.href = "/login"; });

(async function iniciar() {
  try {
    preCarregar("/api/criativos");                 // a lista vem junto, em paralelo
    [EU] = await Promise.all([api("/api/eu"), carregarCatalogo()]);
    $("#eu-nome").textContent = EU.nome; $("#eu-email").textContent = EU.email; $("#avatar").textContent = iniciais(EU.nome);
  } catch (e) { if (!/Sessão/.test(e.message)) toast(e.message); }
  atualizarEstado();
  rota();
})();
