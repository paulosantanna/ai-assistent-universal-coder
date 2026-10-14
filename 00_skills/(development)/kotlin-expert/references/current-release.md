# Current Kotlin release

Entry: `docs-kotlin-current` `language_docs.version_status`.

- Resolved current stable: Kotlin 2.4.20.
- Evidence: JetBrains/kotlin GitHub tag `v2.4.20` (2026-09-07), [What's new in Kotlin 2.4.20](https://kotlinlang.org/docs/whatsnew2420.html), [Kotlin releases](https://kotlinlang.org/docs/releases.html).
- Language/API line: 2.4. Treat `languageVersion`/`apiVersion` 2.5 as experimental unless the repository explicitly enables it.
- Detect the project version from the Kotlin Gradle plugin, Maven compiler plugin, `kotlin-stdlib`, CI images and wrapper properties before using 2.4.20 APIs.
- Reconfirm with `docs-kotlin-current` before treating a newer tag as current. Do not infer currency from model memory.
