package com.aeos.telemetry.devtools;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Gravação JSONL por sinal com rotação por teto de tamanho e idade e limite de arquivos.
 *  Arquivo ativo: {signal}.jsonl; rotacionados: {signal}.1.jsonl (mais recente) até
 *  {signal}.{maxFiles-1}.jsonl. Total mantido ≤ maxFiles. */
public final class JsonlStore {

    /** Primeira marca temporal embutida na linha (int64s do proto-JSON podem vir com aspas). */
    private static final Pattern TIME_NANOS = Pattern.compile(
            "\"(?:startTimeUnixNano|timeUnixNano)\"\\s*:\\s*\"?(\\d+)\"?");

    private final Path dir;
    private final String signal;
    private final long maxBytes;
    private final int maxFiles;
    private final Duration maxAge;
    private final Clock clock;
    private final Object lock = new Object();
    private Path active;
    private Instant activeCreated;

    private JsonlStore(Path dir, String signal, long maxBytes, int maxFiles, Duration maxAge, Clock clock) {
        this.dir = dir;
        this.signal = signal;
        this.maxBytes = Math.max(1, maxBytes);
        this.maxFiles = Math.max(1, maxFiles);
        this.maxAge = maxAge;
        this.clock = clock;
    }

    public static JsonlStore create(SinkConfig config, String signal, Clock clock) throws IOException {
        Path dir = Path.of(config.dir());
        Files.createDirectories(dir);
        return new JsonlStore(dir, signal, config.maxBytes(), config.maxFiles(), config.maxAge(), clock);
    }

    /** Anexa uma linha JSON (já em OTLP-JSON). Rotaciona quando o teto de tamanho ou idade é atingido. */
    public void append(String jsonLine) throws IOException {
        synchronized (lock) {
            if (active == null) {
                active = dir.resolve(signal + ".jsonl");
                if (Files.exists(active)) {
                    activeCreated = Files.getLastModifiedTime(active).toInstant();
                } else {
                    activeCreated = clock.instant();
                }
            }
            if (Files.exists(active) && Files.size(active) >= maxBytes) {
                rotate();
            } else if (Duration.between(activeCreated, clock.instant()).compareTo(maxAge) >= 0) {
                rotate();
            }
            Files.writeString(active, jsonLine + System.lineSeparator(),
                    StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        }
    }

    private void rotate() throws IOException {
        if (maxFiles > 1) {
            for (int i = maxFiles - 1; i >= 1; i--) {
                if (i == 1) {
                    moveIfExists(active, dir.resolve(signal + ".1.jsonl"));
                } else {
                    moveIfExists(dir.resolve(signal + "." + (i - 1) + ".jsonl"),
                            dir.resolve(signal + "." + i + ".jsonl"));
                }
            }
        } else if (active != null) {
            Files.deleteIfExists(active);
        }
        activeCreated = clock.instant();
    }

    private static void moveIfExists(Path from, Path to) throws IOException {
        if (from != null && Files.exists(from)) {
            Files.move(from, to, StandardCopyOption.REPLACE_EXISTING);
        }
    }

    /** Linhas mais recentes primeiro (ativo → rotações), com filtro por timestamp embutido (ms) e teto. */
    public List<String> readRecent(Long sinceEpochMs, int limit) throws IOException {
        synchronized (lock) {
            List<String> result = new ArrayList<>();
            List<Path> files = new ArrayList<>();
            Path activePath = dir.resolve(signal + ".jsonl");
            if (Files.exists(activePath)) {
                files.add(activePath);
            }
            for (int i = 1; i <= maxFiles - 1; i++) {
                Path rotated = dir.resolve(signal + "." + i + ".jsonl");
                if (Files.exists(rotated)) {
                    files.add(rotated);
                }
            }
            for (Path file : files) {
                if (result.size() >= limit) {
                    break;
                }
                List<String> lines = Files.readAllLines(file, StandardCharsets.UTF_8);
                for (int i = lines.size() - 1; i >= 0 && result.size() < limit; i--) {
                    String line = lines.get(i).strip();
                    if (line.isEmpty()) {
                        continue;
                    }
                    if (sinceEpochMs != null && lineTimeMs(line) < sinceEpochMs) {
                        continue;
                    }
                    result.add(line);
                }
            }
            return result;
        }
    }

    /** Timestamp da primeira marca temporal da linha em ms (0 quando ausente — aproximado por design). */
    static long lineTimeMs(String line) {
        Matcher matcher = TIME_NANOS.matcher(line);
        if (matcher.find()) {
            try {
                return Long.parseLong(matcher.group(1)) / 1_000_000L;
            } catch (NumberFormatException e) {
                return 0;
            }
        }
        return 0;
    }

    /** true quando nenhum arquivo do sinal existe ainda (C14: arquivo íntegro). */
    public boolean isEmpty() {
        synchronized (lock) {
            if (active == null) {
                return !Files.exists(dir.resolve(signal + ".jsonl"));
            }
            return false;
        }
    }

    /** Conta as linhas do arquivo ativo (uso em testes). */
    long activeLineCount() throws IOException {
        synchronized (lock) {
            Path activePath = active == null ? dir.resolve(signal + ".jsonl") : active;
            if (!Files.exists(activePath)) {
                return 0;
            }
            return Files.readAllLines(activePath, StandardCharsets.UTF_8).stream()
                    .filter(l -> !l.isBlank())
                    .count();
        }
    }
}
