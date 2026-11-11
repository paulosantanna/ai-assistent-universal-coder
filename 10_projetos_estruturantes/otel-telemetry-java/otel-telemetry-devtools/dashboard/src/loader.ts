/** Parsing OTLP-JSON → registros planos com cap de carga.
 *  Módulo puro (sem DOM): usado pelo dashboard e pelo teste capsLoadedWindow (C22). */

/** Janela deslizante em memória: acima disso, os registros mais ANTIGOS são descartados. */
export const MAX_RECORDS = 5000;

export type SpanRecord = {
  kind: 'span';
  name: string;
  traceId: string;
  spanId: string;
  startMs: number;
  endMs: number;
  attributes: Record<string, string>;
};

export type LogEntry = {
  kind: 'log';
  message: string;
  severityText: string;
  timeMs: number;
  /** Nanossegundos brutos do OTLP-JSON, quando presentes (dedup estável no modo live). */
  timeNs?: string;
  attributes: Record<string, string>;
};

export type MetricEntry = {
  kind: 'metric';
  name: string;
  monotonic: boolean;
  points: { timeMs: number; value: number }[];
};

export type SignalRecord = SpanRecord | LogEntry | MetricEntry;

/** int64 ns (string ou number no OTLP-JSON) → epoch ms. */
export function nsToMs(value: unknown): number {
  if (value === null || value === undefined) {
    return 0;
  }
  const n = typeof value === 'number' ? value : Number(value);
  return Number.isFinite(n) ? Math.floor(n / 1e6) : 0;
}

/** Attributes OTLP-JSON ([{key, value:{stringValue,...}}]) → Record<string,string>. */
export function attrsToMap(attrs: unknown): Record<string, string> {
  const result: Record<string, string> = {};
  if (!Array.isArray(attrs)) {
    return result;
  }
  for (const kv of attrs) {
    if (kv && typeof kv === 'object' && typeof (kv as any).key === 'string') {
      const value = (kv as any).value;
      let text = '';
      if (value && typeof value === 'object') {
        const v = value as Record<string, unknown>;
        text = String(
          v.stringValue ?? v.intValue ?? v.doubleValue ?? v.boolValue ?? JSON.stringify(v),
        );
      }
      result[(kv as any).key] = text;
    }
  }
  return result;
}

/** Converte um documento Export*ServiceRequest (string JSON ou objeto) em registros planos.
 *  Linhas inválidas são ignoradas (fail-soft do dashboard; never throws). */
export function parseOtlpValue(value: string | object): SignalRecord[] {
  let doc: any;
  if (typeof value === 'string') {
    try {
      doc = JSON.parse(value);
    } catch {
      return [];
    }
  } else {
    doc = value;
  }
  if (!doc || typeof doc !== 'object') {
    return [];
  }

  const records: SignalRecord[] = [];

  const resourceSpans = doc.resourceSpans;
  if (Array.isArray(resourceSpans)) {
    for (const rs of resourceSpans) {
      for (const ss of rs?.scopeSpans ?? []) {
        for (const span of ss?.spans ?? []) {
          records.push({
            kind: 'span',
            name: String(span?.name ?? '(sem nome)'),
            traceId: String(span?.traceId ?? ''),
            spanId: String(span?.spanId ?? ''),
            startMs: nsToMs(span?.startTimeUnixNano),
            endMs: nsToMs(span?.endTimeUnixNano),
            attributes: attrsToMap(span?.attributes),
          });
        }
      }
    }
  }

  const resourceLogs = doc.resourceLogs;
  if (Array.isArray(resourceLogs)) {
    for (const rl of resourceLogs) {
      for (const sl of rl?.scopeLogs ?? []) {
        for (const log of sl?.logRecords ?? []) {
          const body = log?.body;
          const message =
            body && typeof body === 'object' && 'stringValue' in body
              ? String((body as any).stringValue)
              : body != null
                ? JSON.stringify(body)
                : '';
          records.push({
            kind: 'log',
            message,
            severityText: String(log?.severityText ?? ''),
            timeMs: nsToMs(log?.timeUnixNano ?? log?.observedTimeUnixNano),
            timeNs: log?.timeUnixNano != null ? String(log.timeUnixNano) : undefined,
            attributes: attrsToMap(log?.attributes),
          });
        }
      }
    }
  }

  const resourceMetrics = doc.resourceMetrics;
  if (Array.isArray(resourceMetrics)) {
    for (const rm of resourceMetrics) {
      for (const sm of rm?.scopeMetrics ?? []) {
        for (const metric of sm?.metrics ?? []) {
          const points: { timeMs: number; value: number }[] = [];
          const collect = (dp: any) => {
            if (!dp) {
              return;
            }
            const raw = dp.asDouble ?? dp.asInt;
            const value = typeof raw === 'number' ? raw : Number(raw);
            if (Number.isFinite(value)) {
              points.push({ timeMs: nsToMs(dp.timeUnixNano), value });
            }
          };
          metric?.gauge?.dataPoints?.forEach(collect);
          metric?.sum?.dataPoints?.forEach(collect);
          // histograma não tem render próprio no dashboard; buckets ficam de fora até existir exibição
          if (points.length > 0) {
            records.push({
              kind: 'metric',
              name: String(metric?.name ?? '(sem nome)'),
              monotonic: metric?.sum?.isMonotonic === true,
              points,
            });
          }
        }
      }
    }
  }

  return records;
}

/** Lê linhas JSONL e devolve no máximo MAX_RECORDS, PRESERVANDO os mais recentes
 *  (janela deslizante pela ordem de leitura: linhas de trás vencem). Nunca lança. */
export function loadJsonlLines(lines: string[]): SignalRecord[] {
  const all: SignalRecord[] = [];
  for (const line of lines) {
    if (!line || !line.trim()) {
      continue;
    }
    all.push(...parseOtlpValue(line));
    if (all.length > MAX_RECORDS) {
      // short-circuit: só as últimas MAX_RECORDS podem sobreviver
      all.splice(0, all.length - MAX_RECORDS);
    }
  }
  return all.length > MAX_RECORDS ? all.slice(all.length - MAX_RECORDS) : all;
}

/** Último timestamp (ms) dos registros — usado como `since` do modo live. */
export function maxTimeMs(records: SignalRecord[]): number {
  let max = 0;
  for (const r of records) {
    const times = r.kind === 'span'
      ? [r.startMs, r.endMs]
      : r.kind === 'log'
        ? [r.timeMs]
        : r.points.map((p) => p.timeMs);
    for (const t of times) {
      if (t > max) {
        max = t;
      }
    }
  }
  return max;
}
