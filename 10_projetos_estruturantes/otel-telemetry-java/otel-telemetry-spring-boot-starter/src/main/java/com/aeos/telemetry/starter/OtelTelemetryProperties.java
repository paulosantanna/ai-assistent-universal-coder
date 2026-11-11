package com.aeos.telemetry.starter;

import org.springframework.boot.context.properties.ConfigurationProperties;

/** Properties oteltelemetry.* do app Spring Boot. Campos nulos simplesmente não são
 *  passados ao builder — a resolução em camadas do core (env &gt; sysprop &gt; yaml) continua valendo. */
@ConfigurationProperties(prefix = "oteltelemetry")
public record OtelTelemetryProperties(
        String serviceName,
        String preset,
        String protocol,
        String endpoint) {
}
