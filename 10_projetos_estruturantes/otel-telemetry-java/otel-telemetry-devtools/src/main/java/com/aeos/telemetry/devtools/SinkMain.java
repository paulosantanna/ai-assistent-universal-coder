package com.aeos.telemetry.devtools;

import java.io.IOException;

/** Entrada do sink: {@code java -cp ... com.aeos.telemetry.devtools.SinkMain} (ou o jar). */
public final class SinkMain {

    private SinkMain() {
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        SinkConfig config = SinkConfig.fromEnv();
        OtlpSinkServer server = new OtlpSinkServer(config);
        server.start();
        System.out.println("[otel-telemetry-sink] escutando em http://" + config.host() + ":"
                + config.port() + " (dir=" + config.dir() + ", disabled=" + config.disabled() + ")");
        System.out.println("[otel-telemetry-sink] dashboard: http://127.0.0.1:" + config.port() + "/");
        // o processo vive até o owner derrubar (Ctrl+C / stop do terminal)
        Thread.currentThread().join();
    }
}
