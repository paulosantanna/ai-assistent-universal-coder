package com.aeos.telemetry.example;

import com.aeos.telemetry.core.Telemetry;
import com.aeos.telemetry.core.TelemetryBootstrap;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.StatusCode;

import java.time.Instant;
import java.util.concurrent.ThreadLocalRandom;

/** Exemplo Java puro: bootstrap de UMA linha + gerador de carga para o dashboard.
 *  O preset/destino vêm do ambiente (default offline → http://127.0.0.1:14318);
 *  rode o sink (devtools) e o dashboard em http://127.0.0.1:14318/. */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) throws Exception {
        // >>> bootstrap de uma linha: todo o resto é resolvido por env > sysprop > yaml (AD-003)
        Telemetry telemetry = TelemetryBootstrap.start(builder -> builder.serviceName("demo-java"));

        try {
            var tracer = telemetry.openTelemetry().getTracer("demo-java");
            var meter = telemetry.openTelemetry().getMeter("demo-java");
            var logger = telemetry.openTelemetry().getLogsBridge().get("demo-java");
            var counter = meter.counterBuilder("demo.requests").ofDoubles().build();

            int rounds = args.length > 0 ? Integer.parseInt(args[0]) : 10;
            for (int i = 1; i <= rounds; i++) {
                Span span = tracer.spanBuilder("checkout-request").setAttribute("pedido.id", i).startSpan();
                try (var ignored = span.makeCurrent()) {
                    Thread.sleep(ThreadLocalRandom.current().nextLong(10, 60));
                    if (i % 5 == 0) {
                        span.setStatus(StatusCode.ERROR, "pagamento recusado");
                    }
                } finally {
                    span.end();
                }
                counter.add(1);
                logger.logRecordBuilder()
                        .setTimestamp(Instant.now())
                        .setSeverityText("INFO")
                        .setBody("pedido " + i + " processado")
                        .setAttribute("pedido.id", i)
                        .emit();
                System.out.println("[demo] rodada " + i + " emitida");
                Thread.sleep(300);
            }
            System.out.println("[demo] carregou " + rounds
                    + " rodadas; confira http://127.0.0.1:14318/ (sink no ar)");
        } finally {
            // flush com teto de 5 s (AD-006) antes de encerrar
            telemetry.shutdown();
        }
    }
}
