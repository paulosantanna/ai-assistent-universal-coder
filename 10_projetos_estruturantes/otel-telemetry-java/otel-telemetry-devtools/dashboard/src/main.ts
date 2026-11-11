import uPlot from 'uplot';
import 'uplot/dist/uPlot.min.css';
import {
  MAX_RECORDS,
  loadJsonlLines,
  parseOtlpValue,
  maxTimeMs,
  type SignalRecord,
} from './loader';

/** Ponto de entrada do dashboard. Dois modos:
 *  - live (http): consulta /api/{traces,metrics,logs}?since=... a cada 2 s;
 *  - arquivo (file:// ou botão): drag-drop/abrir .jsonl e renderizar igual. */

const RENDER_LIST_LIMIT = 200; // linhas por aba (janela de render)
const MAX_CHART_POINTS = 500; // pontos por série no gráfico
const MAX_CHART_SERIES = 12; // métricas plotadas simultaneamente
const POLL_MS = 2000;

let records: SignalRecord[] = [];
let chart: uPlot | null = null;
let activeTab = 'traces';

const $ = (id: string): HTMLElement => {
  const el = document.getElementById(id);
  if (!el) {
    throw new Error('elemento ausente no index.html: #' + id);
  }
  return el;
};

const isFileMode = location.protocol === 'file:';

/** Chave estável por registro: o servidor devolve o registro de fronteira a cada poll
 *  (filtro timeMs >= since), então o merge deduplica — sem isso, a tabela cresce com
 *  tráfego parado. Log sem timeUnixNano cai para timeMs + message (aproximação de ms). */
function recordKey(r: SignalRecord): string {
  if (r.kind === 'span') {
    return 't:' + r.traceId + ':' + r.spanId;
  }
  if (r.kind === 'log') {
    return 'l:' + (r.timeNs || r.timeMs) + ':' + r.message;
  }
  const last = r.points[r.points.length - 1];
  return 'm:' + r.name + ':' + (last ? last.timeMs : 0) + ':' + (last ? last.value : 0);
}

/** Insere novos registros mantendo a janela deslizante (mais antigos fora). */
function mergeNew(newRecords: SignalRecord[]) {
  if (newRecords.length === 0) {
    return;
  }
  const seen = new Set(records.map(recordKey));
  const fresh = newRecords.filter((r) => !seen.has(recordKey(r)));
  if (fresh.length === 0) {
    return;
  }
  records.push(...fresh);
  if (records.length > MAX_RECORDS) {
    records.splice(0, records.length - MAX_RECORDS);
  }
  renderStatus();
  if (activeTab === 'traces') {
    renderTraces();
  } else if (activeTab === 'logs') {
    renderLogs();
  } else {
    renderMetrics();
  }
}

function renderStatus() {
  const mode = isFileMode ? 'modo arquivo (drag-drop .jsonl)' : 'live ' + location.origin + ' · poll ' + POLL_MS / 1000 + 's';
  $('status').textContent = mode + ' — ' + records.length + ' registros (janela máx ' + MAX_RECORDS + ')';
}

function esc(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function table(html: string): string {
  return '<table class="records"><thead><tr><th>tempo</th><th>conteúdo</th></tr></thead><tbody>'
    + html + '</tbody></table>';
}

function fmtMs(ms: number): string {
  return ms > 0 ? new Date(ms).toISOString().replace('T', ' ').replace('Z', '') : '—';
}

function renderTraces() {
  const spans = records.filter((r): r is Extract<SignalRecord, { kind: 'span' }> => r.kind === 'span');
  const rows = spans.slice(-RENDER_LIST_LIMIT).reverse().map((s) =>
    '<tr><td>' + esc(fmtMs(s.startMs)) + '</td><td><b>' + esc(s.name)
    + '</b> · trace ' + esc(s.traceId.slice(0, 12)) + ' · ' + (s.endMs - s.startMs) + 'ms</td></tr>');
  $('list-traces').innerHTML = table(rows.join(''));
}

function renderLogs() {
  const logs = records.filter((r): r is Extract<SignalRecord, { kind: 'log' }> => r.kind === 'log');
  const rows = logs.slice(-RENDER_LIST_LIMIT).reverse().map((l) =>
    '<tr><td>' + esc(fmtMs(l.timeMs)) + '</td><td><span class="sev">' + esc(l.severityText || 'LOG')
    + '</span> ' + esc(l.message) + '</td></tr>');
  $('list-logs').innerHTML = table(rows.join(''));
}

/** Métricas agregadas por nome: último valor + série para o gráfico. */
type MetricSeries = { name: string; monotonic: boolean; points: { timeMs: number; value: number }[] };

function metricSeries(): MetricSeries[] {
  const byName = new Map<string, MetricSeries>();
  for (const r of records) {
    if (r.kind !== 'metric') {
      continue;
    }
    let series = byName.get(r.name);
    if (!series) {
      series = { name: r.name, monotonic: r.monotonic, points: [] };
      byName.set(r.name, series);
    }
    series.monotonic = series.monotonic || r.monotonic;
    series.points.push(...r.points);
  }
  const all = [...byName.values()];
  for (const series of all) {
    series.points.sort((a, b) => a.timeMs - b.timeMs);
    // dedup por tempo (último vence) e cap de janela
    const dedup = new Map<number, number>();
    for (const p of series.points) {
      dedup.set(p.timeMs, p.value);
    }
    let sorted = [...dedup.entries()].map(([timeMs, value]) => ({ timeMs, value }));
    if (sorted.length > MAX_CHART_POINTS) {
      sorted = sorted.slice(sorted.length - MAX_CHART_POINTS);
    }
    series.points = sorted;
  }
  return all.sort((a, b) => b.points.length - a.points.length).slice(0, MAX_CHART_SERIES);
}

/** Modo delta: somas monotônicas plotam a diferença entre pontos consecutivos. */
function toDelta(points: { timeMs: number; value: number }[]): { timeMs: number; value: number }[] {
  const out: { timeMs: number; value: number }[] = [];
  for (let i = 1; i < points.length; i++) {
    out.push({ timeMs: points[i].timeMs, value: Math.max(0, points[i].value - points[i - 1].value) });
  }
  return out;
}

function renderMetrics() {
  const series = metricSeries();
  const rows = series.map((s) => {
    const last = s.points[s.points.length - 1];
    return '<tr><td>' + esc(fmtMs(last ? last.timeMs : 0)) + '</td><td><b>' + esc(s.name)
      + '</b> · ' + s.points.length + ' pts · ' + esc(String(last ? last.value : '—'))
      + (s.monotonic ? ' (soma monotônica → Δ)' : '') + '</td></tr>';
  });
  $('list-metrics').innerHTML = table(rows.join(''));
  drawChart(series);
}

const PALETTE = ['#3b82f6', '#ef4444', '#22c55e', '#eab308', '#a855f7', '#06b6d4',
  '#f97316', '#ec4899', '#84cc16', '#6366f1', '#14b8a6', '#f43f5e'];

function drawChart(series: MetricSeries[]) {
  const container = $('chart');
  if (series.length === 0) {
    container.innerHTML = '<p class="empty">Sem métricas carregadas ainda.</p>';
    if (chart) {
      chart.destroy();
      chart = null;
    }
    return;
  }

  const aligned = series.map((s) => (s.monotonic ? toDelta(s.points) : s.points));
  const times = [...new Set(aligned.flatMap((pts) => pts.map((p) => p.timeMs)))].sort((a, b) => a - b);
  const xData = times.map((t) => t / 1000); // uPlot: eixo x em segundos
  const data: uPlot.AlignedData = [
    xData,
    ...aligned.map((pts) => {
      const byTime = new Map(pts.map((p) => [p.timeMs / 1000, p.value]));
      return times.map((t) => byTime.get(t / 1000) ?? null);
    }),
  ];

  const width = container.clientWidth || 800;
  const opts: uPlot.Options = {
    width,
    height: 300,
    title: 'Δ entre pontos consecutivos (somas monotônicas) · valores brutos (gauges)',
    spanGaps: true,
    scales: { x: { time: false } },
    series: [
      { label: 'tempo' },
      ...aligned.map((pts, i) => ({
        label: series[i].name + (series[i].monotonic ? ' (Δ)' : ''),
        stroke: PALETTE[i % PALETTE.length],
        width: 1.5,
        points: { show: (pts ?? []).length < 40 },
      })),
    ],
  };

  if (chart) {
    chart.destroy();
  }
  chart = new uPlot(opts, data, container);
}

function switchTab(tab: string) {
  activeTab = tab;
  for (const t of ['traces', 'logs', 'metrics']) {
    $('panel-' + t).hidden = t !== tab;
    $('tab-' + t).classList.toggle('active', t === tab);
  }
  if (tab === 'traces') {
    renderTraces();
  } else if (tab === 'logs') {
    renderLogs();
  } else {
    renderMetrics();
  }
}

/* ---------- live mode ---------- */

const signals = ['traces', 'metrics', 'logs'] as const;

/** Token Bearer do sink — informado uma única vez quando o /api responde 403 e
 *  reenviado nas chamadas seguintes (a UI estática é servida sem auth por design). */
let sinkToken = '';

async function apiFetch(url: string): Promise<Response> {
  const headers: Record<string, string> = sinkToken ? { Authorization: 'Bearer ' + sinkToken } : {};
  let response = await fetch(url, { headers });
  if (response.status === 403 && !sinkToken) {
    const token = window.prompt('O sink exige autenticação (OTELTELEMETRY_SINK_TOKEN). Bearer token:');
    if (token && token.trim()) {
      sinkToken = token.trim();
      response = await fetch(url, { headers: { Authorization: 'Bearer ' + sinkToken } });
    }
  }
  return response;
}

async function pollOnce() {
  const since = maxTimeMs(records);
  try {
    for (const signal of signals) {
      const response = await apiFetch('/api/' + signal + '?since=' + since + '&limit=100');
      if (!response.ok) {
        continue;
      }
      const body = await response.json();
      const items = Array.isArray(body?.items) ? body.items : [];
      const parsed: SignalRecord[] = [];
      for (const item of items) {
        parsed.push(...parseOtlpValue(item));
      }
      mergeNew(parsed);
    }
  } catch (error) {
    // fail-soft: rede indisponível não deve derrubar o dashboard
    console.warn('poll falhou', error);
  }
}

/* ---------- file mode ---------- */

function ingestFiles(files: FileList | File[]) {
  const selected = Array.from(files);
  const texts: string[] = [];
  let pending = selected.length;
  for (const file of selected) {
    const reader = new FileReader();
    reader.onload = () => {
      texts.push(String(reader.result ?? ''));
      if (--pending > 0) {
        return; // lote completo antes de renderizar (multi-arquivo nunca é last-wins)
      }
      const parsed = loadJsonlLines(texts.flatMap((text) => text.split('\n')));
      if (isFileMode) {
        // o lote inteiro vira a base completa — com o mesmo dedup do modo live,
        // porque arquivos rotacionados/ativos podem conter os mesmos registros
        const seen = new Set<string>();
        records = parsed.filter((r) => {
          const key = recordKey(r);
          if (seen.has(key)) {
            return false;
          }
          seen.add(key);
          return true;
        });
      } else {
        mergeNew(parsed);
        return;
      }
      renderStatus();
      switchTab(activeTab);
    };
    reader.readAsText(file);
  }
}

function setupDrop() {
  const overlay = $('drop-overlay');
  let depth = 0;
  window.addEventListener('dragenter', (e) => {
    e.preventDefault();
    depth++;
    overlay.hidden = false;
  });
  window.addEventListener('dragleave', () => {
    depth--;
    if (depth <= 0) {
      depth = 0;
      overlay.hidden = true;
    }
  });
  window.addEventListener('dragover', (e) => e.preventDefault());
  window.addEventListener('drop', (e) => {
    e.preventDefault();
    depth = 0;
    overlay.hidden = true;
    if (e.dataTransfer?.files?.length) {
      ingestFiles(e.dataTransfer.files);
    }
  });
  $('open-file').addEventListener('click', () => $('file-input').click());
  $('file-input').addEventListener('change', (e) => {
    const input = e.target as HTMLInputElement;
    if (input.files?.length) {
      ingestFiles(input.files);
    }
    input.value = '';
  });
}

function init() {
  for (const tab of signals) {
    $('tab-' + tab).addEventListener('click', () => switchTab(tab));
  }
  setupDrop();
  renderStatus();
  switchTab('traces');

  let timer: number | undefined;
  if (!isFileMode) {
    pollOnce();
    timer = window.setInterval(pollOnce, POLL_MS);
  }

  let resizeTimer: number | undefined;
  window.addEventListener('resize', () => {
    if (activeTab !== 'metrics') {
      return;
    }
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(() => {
      if (chart) {
        chart.setSize({ width: $('chart').clientWidth || 800, height: 300 });
      }
    }, 200);
  });

  // parar o poll quando a aba é fechada (economia em dev)
  window.addEventListener('beforeunload', () => {
    if (timer !== undefined) {
      window.clearInterval(timer);
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
