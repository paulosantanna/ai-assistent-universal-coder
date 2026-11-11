package com.aeos.telemetry.adapters;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.metrics.SdkMeterProvider;
import io.opentelemetry.sdk.metrics.data.MetricData;
import io.opentelemetry.sdk.testing.exporter.InMemoryMetricReader;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

/** C10: contador Micrometer vira métrica OTel no provider subjacente.
 *  A bridge grava DoubleCounter — o tipo da métrica é DOUBLE_SUM (getLongSumData() devolve empty). */
class MicrometerBridgeTest {

    @Test
    void micrometerCounterBecomesOtelMetric() {
        InMemoryMetricReader reader = InMemoryMetricReader.create();
        SdkMeterProvider meterProvider = SdkMeterProvider.builder()
                .registerMetricReader(reader)
                .build();
        OpenTelemetrySdk sdk = OpenTelemetrySdk.builder()
                .setMeterProvider(meterProvider)
                .build();

        MeterRegistry registry = Adapters.micrometerRegistry(sdk);
        Counter counter = Counter.builder("bridge.counter")
                .tag("area", "pagamento")
                .register(registry);
        counter.increment(3);

        MetricData metric = reader.collectAllMetrics().stream()
                .filter(m -> "bridge.counter".equals(m.getName()))
                .findFirst()
                .orElseThrow();
        assertFalse(metric.getDoubleSumData().getPoints().isEmpty());
        assertEquals("pagamento",
                metric.getDoubleSumData().getPoints().iterator().next()
                        .getAttributes().get(AttributeKey.stringKey("area")));
        assertEquals(3.0,
                metric.getDoubleSumData().getPoints().iterator().next().getValue(), 1e-9);
    }
}
