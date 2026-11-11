package com.aeos.telemetry.core;

import io.opentelemetry.sdk.common.CompletableResultCode;
import io.opentelemetry.sdk.trace.data.SpanData;
import io.opentelemetry.sdk.trace.export.SpanExporter;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/** Exporter de gravação para testes: NÃO descarta os spans recebidos no shutdown()
 *  (InMemorySpanExporter limpa a lista em shutdown e por isso não serve para
 *  asserções pós-shutdown do flush de C4). */
public final class RecordingSpanExporter implements SpanExporter {

    private final Queue<SpanData> recorded = new ConcurrentLinkedQueue<>();
    private volatile boolean stopped;

    public static RecordingSpanExporter create() {
        return new RecordingSpanExporter();
    }

    /** Spans entregues por export(); preservados mesmo após shutdown(). */
    public List<SpanData> getFinishedSpanItems() {
        return Collections.unmodifiableList(new ArrayList<>(recorded));
    }

    @Override
    public CompletableResultCode export(Collection<SpanData> spans) {
        if (stopped) {
            return CompletableResultCode.ofFailure();
        }
        recorded.addAll(spans);
        return CompletableResultCode.ofSuccess();
    }

    @Override
    public CompletableResultCode flush() {
        return CompletableResultCode.ofSuccess();
    }

    @Override
    public CompletableResultCode shutdown() {
        stopped = true;
        return CompletableResultCode.ofSuccess();
    }
}
