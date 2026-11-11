package com.aeos.telemetry.devtools;

import java.time.Duration;
import java.util.Map;

/** Configuração do sink offline (env OTELTELEMETRY_SINK_*). Defaults: 127.0.0.1:14318,
 *  dir otlp-sink, 32 MB, 5 arquivos, 24 h. authRequired quando token configurado OU host
 *  não-loopback. O token nunca aparece em toString(). */
public final class SinkConfig {

    private final String host;
    private final int port;
    private final String token;
    private final boolean disabled;
    private final String dir;
    private final long maxBytes;
    private final int maxFiles;
    private final Duration maxAge;

    private SinkConfig(String host, int port, String token, boolean disabled, String dir,
                       long maxBytes, int maxFiles, Duration maxAge) {
        this.host = host;
        this.port = port;
        this.token = token;
        this.disabled = disabled;
        this.dir = dir;
        this.maxBytes = maxBytes;
        this.maxFiles = maxFiles;
        this.maxAge = maxAge;
    }

    public static SinkConfig fromEnv() {
        return fromEnv(System.getenv());
    }

    public static SinkConfig fromEnv(Map<String, String> env) {
        String host = value(env, "OTELTELEMETRY_SINK_HOST", "127.0.0.1");
        int port = intOf(value(env, "OTELTELEMETRY_SINK_PORT", "14318"), 14318);
        String token = env.get("OTELTELEMETRY_SINK_TOKEN");
        boolean disabled = Boolean.parseBoolean(value(env, "OTELTELEMETRY_SINK_DISABLED", "false"));
        String dir = value(env, "OTELTELEMETRY_SINK_DIR", "otlp-sink");
        long maxMb = longOf(value(env, "OTELTELEMETRY_SINK_MAX_MB", "32"), 32);
        int maxFiles = intOf(value(env, "OTELTELEMETRY_SINK_MAX_FILES", "5"), 5);
        long maxAgeMinutes = longOf(value(env, "OTELTELEMETRY_SINK_MAX_AGE_MINUTES", "1440"), 1440);
        return new SinkConfig(host, port, blankToNull(token), disabled, dir,
                maxMb * 1024 * 1024, Math.max(1, maxFiles), Duration.ofMinutes(Math.max(0, maxAgeMinutes)));
    }

    /** Construção programática (testes e embeds). */
    public static SinkConfig of(String host, int port, String token, boolean disabled, String dir,
                                long maxBytes, int maxFiles, Duration maxAge) {
        return new SinkConfig(host, port, token, disabled, dir, maxBytes,
                Math.max(1, maxFiles), maxAge);
    }

    public String host() {
        return host;
    }

    public int port() {
        return port;
    }

    public String token() {
        return token;
    }

    public boolean disabled() {
        return disabled;
    }

    public String dir() {
        return dir;
    }

    public long maxBytes() {
        return maxBytes;
    }

    public int maxFiles() {
        return maxFiles;
    }

    public Duration maxAge() {
        return maxAge;
    }

    /** Exige Authorization quando um token está configurado OU o bind não é loopback. */
    public boolean authRequired() {
        return token != null || !isLoopback(host);
    }

    static boolean isLoopback(String host) {
        return "127.0.0.1".equals(host) || "localhost".equals(host) || "::1".equals(host)
                || "[::1]".equals(host);
    }

    private static String value(Map<String, String> env, String key, String fallback) {
        String v = env.get(key);
        return v == null || v.isBlank() ? fallback : v.trim();
    }

    private static String blankToNull(String value) {
        return value == null || value.isBlank() ? null : value;
    }

    private static int intOf(String value, int fallback) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    private static long longOf(String value, long fallback) {
        try {
            return Long.parseLong(value);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    @Override
    public String toString() {
        return "SinkConfig{host=" + host + ", port=" + port + ", authRequired=" + authRequired()
                + ", disabled=" + disabled + ", dir=" + dir + ", maxBytes=" + maxBytes
                + ", maxFiles=" + maxFiles + ", maxAge=" + maxAge + "}";
    }
}
