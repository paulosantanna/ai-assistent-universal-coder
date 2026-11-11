package com.aeos.telemetry.core;

import java.lang.System.Logger;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.ServiceLoader;
import java.util.function.Consumer;

/** Ponto de entrada da biblioteca: resolve a configuração e instala a telemetria (fail-soft, AD-006). */
public final class TelemetryBootstrap {

    private static final Logger LOGGER = System.getLogger(TelemetryBootstrap.class.getName());

    /** Arquivo yaml (chaves planas) carregado do diretório de trabalho quando existir. */
    public static final String CONFIG_FILE = "oteltelemetry.yaml";

    private TelemetryBootstrap() {
    }

    public static Telemetry start() {
        return start(builder -> {
        });
    }

    /** Uma linha é suficiente: {@code TelemetryBootstrap.start(b -> b.serviceName("meu-app"));}. */
    public static Telemetry start(Consumer<TelemetryConfig.Builder> customizer) {
        TelemetryConfig.Builder builder = TelemetryConfig.builder();
        try {
            customizer.accept(builder);
        } catch (RuntimeException e) {
            List<String> diagnostics = new ArrayList<>();
            diagnostics.add("builder de configuração falhou (" + e.getClass().getSimpleName() + "); telemetria no-op");
            return logged(Telemetry.noop(diagnostics));
        }
        return install(ConfigResolver.resolve(System.getenv(), System.getProperties(), Path.of(CONFIG_FILE),
                builder.build()));
    }

    /** Política central de instalação — exposta para testes e para quem já tem a config resolvida. */
    public static Telemetry install(ResolvedConfig config) {
        List<String> diagnostics = new ArrayList<>(config.diagnostics());

        if (!config.valid()) {
            diagnostics.add("configuração inválida; telemetria no-op");
            return logged(Telemetry.noop(diagnostics));
        }
        if (config.preset().requiresCredential() && !config.credentialPresent()) {
            diagnostics.add("preset " + config.preset().id() + " com credencial ausente (env "
                    + config.preset().credentialEnvNames() + "); telemetria no-op");
            return logged(Telemetry.noop(diagnostics));
        }

        TelemetryRuntimeProvider provider = null;
        try {
            for (TelemetryRuntimeProvider candidate : ServiceLoader.load(TelemetryRuntimeProvider.class)) {
                provider = candidate;
                break;
            }
        } catch (RuntimeException e) {
            diagnostics.add("falha ao carregar TelemetryRuntimeProvider (" + e.getClass().getSimpleName() + ")");
        }
        if (provider == null) {
            diagnostics.add("nenhum TelemetryRuntimeProvider no classpath (adicione otel-telemetry-exporters); telemetria no-op");
            return logged(Telemetry.noop(diagnostics));
        }

        try {
            TelemetryRuntime runtime = provider.create(config);
            return logged(Telemetry.real(runtime, diagnostics));
        } catch (RuntimeException e) {
            diagnostics.add("falha ao montar exporters (" + sanitize(e.toString(), config.credentialValue())
                    + "); telemetria no-op");
            return logged(Telemetry.noop(diagnostics));
        }
    }

    /** Evita ecoar segredos em mensagens de exceção (AC 8). */
    static String sanitize(String message, String secret) {
        if (message == null) {
            return "";
        }
        if (secret != null && !secret.isBlank() && message.contains(secret)) {
            return message.replace(secret, "***");
        }
        return message;
    }

    private static Telemetry logged(Telemetry telemetry) {
        for (String diagnostic : telemetry.diagnostics()) {
            LOGGER.log(Logger.Level.WARNING, "{0}", diagnostic);
        }
        return telemetry;
    }
}
