package com.aeos.telemetry.adapters;

import ch.qos.logback.classic.LoggerContext;
import io.micrometer.core.instrument.MeterRegistry;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.instrumentation.logback.appender.v1_0.OpenTelemetryAppender;
import io.opentelemetry.instrumentation.micrometer.v1_5.OpenTelemetryMeterRegistry;
import org.slf4j.LoggerFactory;

/** Integrações opcionais com bibliotecas do app (logs do Logback e métricas do Micrometer). */
public final class Adapters {

    private Adapters() {
    }

    /** Instala o appender Logback upstream (mesma classe de logback.xml): eventos do root logger
     *  viram LogRecords OTel com severity, corpo e contexto de span.
     *  O upstream {@link OpenTelemetryAppender#install(OpenTelemetry)} só configura appenders JÁ
     *  declarados em logback.xml; este helper anexa a própria instância programaticamente, para uso
     *  sem XML. Apps que declaram o appender em logback.xml devem chamar o install() upstream
     *  diretamente para não duplicar emissão. */
    public static void installLogbackAppender(OpenTelemetry openTelemetry) {
        LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();
        OpenTelemetryAppender appender = new OpenTelemetryAppender();
        appender.setContext(context);
        appender.setName("OtelTelemetryAdapters");
        appender.setOpenTelemetry(openTelemetry);
        appender.setCaptureKeyValuePairAttributes(true);
        appender.start();
        context.getLogger(ch.qos.logback.classic.Logger.ROOT_LOGGER_NAME).addAppender(appender);
    }

    /** Registry Micrometer que exporta métricas para o OpenTelemetry informado (bridge upstream).
     *  A bridge não lê valores de volta; para leitura use outro registry. */
    public static MeterRegistry micrometerRegistry(OpenTelemetry openTelemetry) {
        return OpenTelemetryMeterRegistry.create(openTelemetry);
    }
}
