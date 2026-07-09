"""Code Quality Analyzer - evaluates code quality across 4 dimensions.

Dimensions:
1. Linter/Formatter - presence of linter and formatter configuration
2. Type Checking - presence of type checker configuration and usage
3. Documentation - presence of docstrings, JSDoc, README, inline docs
4. Module Organization - proper package/module structure
"""

import os
import re


LINTER_CONFIGS = {
    "eslint": [".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yaml", ".eslintrc.yml"],
    "prettier": [".prettierrc", ".prettierrc.js", ".prettierrc.json", ".prettierrc.yaml"],
    "ruff": ["ruff.toml", ".ruff.toml", "pyproject.toml"],
    "pylint": [".pylintrc", "pylintrc"],
    "flake8": [".flake8", "setup.cfg", "tox.ini"],
    "black": ["pyproject.toml"],
    "checkstyle": ["checkstyle.xml", "checkstyle-suppressions.xml"],
    "spotbugs": ["spotbugs.xml", "spotbugs-exclude.xml"],
    "ktlint": [".ktlintrc", ".editorconfig"],
    "golangci": [".golangci.yml", ".golangci.yaml"],
    "clippy": ["clippy.toml", ".clippy.toml"],
    "rustfmt": ["rustfmt.toml", ".rustfmt.toml"],
}

TYPE_CHECKER_CONFIGS = {
    "typescript": ["tsconfig.json"],
    "mypy": ["mypy.ini", ".mypy.ini", "pyproject.toml"],
    "pyright": ["pyproject.toml", "pyrightconfig.json"],
    "pylance": ["pyproject.toml"],
    "flow": [".flowconfig"],
}

DOC_PATTERNS = {
    "python": [
        r'"""\s*\w+', r"'''\s*\w+",
        r"#\s*(TODO|FIXME|HACK|XXX|NOTE|OPTIMIZE|REVIEW|BUG|WORKAROUND|TEMP|PERF):",
        r"def \w+\([^)]*\):\s*\n\s*\"\"\"",
        r"class \w+:\s*\n\s*\"\"\"",
        r"def \w+\([^)]*\):\s*\n\s*'''",
        r"\"\"\"\s*(Args|Arguments|Parameters|Params|Keyword Args|Returns|Yields|Raises):",
        r"\"\"\"\s*(Attributes|Properties|Methods|Todo|Note|Warning|Example|Usage|See Also):",
        r"\"\"\"\s*(Summary|Overview|Description|About|Details|References|Notes):",
        r"\"\"\"\s*:(param|type|rtype|return|raises|var|cvar|ivar|yield|ytype|meta|field|module|class|func|meth|attr|data):",
        r"\"\"\"\s*:(mod|class|func|meth|attr|data|exc|const|decorator):",
        r"#\s*(type|rtype|param|return|raises|var|cvar|ivar|yield|ytype):",
        r"def \w+\([^)]*\)\s*->\s*\w+",
        r"async def \w+",
        r"@(property|\w+\.setter|\w+\.deleter|staticmethod|classmethod|abstractmethod)",
        r"#\s*(Copyright|License|Author|Date|Version|Created|Modified|Maintainer|Email):",
        r"#\s*-\*-",
        r"#\s*(noqa|type:\s*\w+|isort:|pylint:|pyright:|mypy:)",
        r"from \w+(\.\w+)* import",
        r"import \w+(\.\w+)*",
        r"\"\"\"\s*\n[\w\s,;:()'\"-]+\n\s*\"\"\"",
        r"class \w+\([^)]*\):",
        r"@\w+(\.\w+)*",
        r"Protocol", r"TypedDict",
        r"\"\"\"\w+[\s\S]{0,200}?\"\"\"",
        r"'''\w+[\s\S]{0,200}?'''",
        r"\"\"\"\s*:(param|type|rtype)\s+\w+",
        r"\"\"\"[^\"']{50,}?\"\"\"",
        r"#\s*(\w+\.\w+)",
        r"@overload",
        r"class \w+\(.*\):",
    ],
    "typescript": [
        r"/\*\*[^/]*@param", r"/\*\*[^/]*@returns",
        r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP|OPTIMIZE):",
        r"interface \w+", r"type \w+ =",
        r"/\*\*[^/]*\*/",
        r"/\*\*[^/]*@type", r"/\*\*[^/]*@template",
        r"/\*\*[^/]*@deprecated", r"/\*\*[^/]*@see",
        r"/\*\*[^/]*@example", r"/\*\*[^/]*@default",
        r"/\*\*[^/]*@throws", r"/\*\*[^/]*@enum",
        r"const \w+:\s*\w+", r"let \w+:\s*\w+",
        r"function \w+<[^>]+>",
        r"class \w+ implements",
        r"class \w+ extends",
        r"abstract class", r"abstract \w+",
        r"enum \w+", r"namespace \w+",
        r"declare \w+", r"module \w+",
        r"as\s+const", r"satisfies\s+\w+",
        r"keyof\s+\w+", r"typeof\s+\w+",
        r"Record<", r"Partial<", r"Required<",
        r"Pick<", r"Omit<", r"Exclude<",
        r"async function \w+",
        r"#\s*(Copyright|License|Author|Version):",
        r"import type",
        r"export interface", r"export type",
        r"export default",
        r"`\$\{.*\}`",
    ],
    "javascript": [
        r"/\*\*[^/]*@param", r"/\*\*[^/]*@returns",
        r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP|OPTIMIZE):",
        r"/\*\*[^/]*\*/",
        r"/\*\*[^/]*@type", r"/\*\*[^/]*@deprecated",
        r"/\*\*[^/]*@see", r"/\*\*[^/]*@example",
        r"/\*\*[^/]*@throws", r"/\*\*[^/]*@callback",
        r"class \w+ extends",
        r"class \w+ \{",
        r"async function", r"async \w+",
        r"function \w+\([^)]*\)",
        r"const \w+ = \(",
        r"export default", r"export \{",
        r"import \w+ from",
        r"require\('[^']+'\)",
        r"module\.exports",
        r"#\s*(Copyright|License|Author|Version):",
        r"@\w+",
        r"Promise<", r"async\s+",
        r"constructor\s*\(",
        r"static \w+",
        r"get \w+\(\)", r"set \w+\(",
    ],
    "java": [
        r"/\*\*[^/]*@param", r"/\*\*[^/]*@return",
        r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND):",
        r"/\*\*[^/]*\*/",
        r"/\*\*[^/]*@throws", r"/\*\*[^/]*@exception",
        r"/\*\*[^/]*@see", r"/\*\*[^/]*@since",
        r"/\*\*[^/]*@deprecated", r"/\*\*[^/]*@version",
        r"/\*\*[^/]*@author", r"/\*\*[^/]*@serial",
        r"/\*\*[^/]*@implSpec", r"/\*\*[^/]*@apiNote",
        r"interface \w+", r"@interface \w+",
        r"enum \w+", r"record \w+",
        r"@Override", r"@Deprecated",
        r"@SuppressWarnings", r"@FunctionalInterface",
        r"public \w+ \w+\(", r"private \w+ \w+\(",
        r"protected \w+ \w+\(",
        r"class \w+ extends", r"class \w+ implements",
        r"abstract class", r"abstract \w+",
        r"final class", r"static \w+",
        r"synchronized \w+",
        r"//\s*(Copyright|License|Author):",
    ],
    "go": [
        r"//\s*\w+", r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP):",
        r"func \w+", r"type \w+ struct",
        r"//\s*\w+ .*", r"//\s*(Deprecated|TODO|FIXME|BUG):",
        r"type \w+ interface",
        r"type \w+ map\[", r"type \w+ \[\]",
        r"type \w+ func\(",
        r"func \(\w+ \*\?\w+\) \w+",
        r"func \(\w+ \w+\) \w+",
        r"func \w+\([^)]*\)\s*\([^)]*\)",
        r"func \w+\([^)]*\)\s*\w+",
        r"const \w+ =", r"var \w+ \w+",
        r"package \w+",
        r"import \(", r"import \"",
        r"//go:embed", r"//go:generate",
        r"//go:noinline", r"//go:nosplit",
        r"#\s*(Copyright|License|Author):",
        r"func \w+\(ctx context\.Context",
        r"err := \w+",
        r"defer \w+",
        r"go func\(",
        r"select \{", r"case <-",
    ],
    "rust": [
        r"///\s*\w+", r"//!\s*\w+",
        r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP|OPTIMIZE|SAFETY):",
        r"fn \w+", r"pub fn",
        r"///\s*(Panics|Errors|Safety|Examples|Returns|Arguments):",
        r"///\s*#\s*(Arguments|Returns|Examples|Panics|Errors|Safety)",
        r"//!\s*(Crate|Module|Examples|Panics|Errors|Safety):",
        r"pub struct", r"pub enum",
        r"pub trait", r"pub type",
        r"pub const", r"pub static",
        r"pub mod", r"pub use",
        r"trait \w+", r"impl \w+ for",
        r"impl \w+", r"struct \w+",
        r"enum \w+", r"type \w+ =",
        r"trait \w+: \w+",
        r"unsafe fn", r"unsafe trait",
        r"macro_rules!", r"#\[derive\(",
        r"#\[allow\(", r"#\[warn\(",
        r"#\[cfg\(", r"#\[must_use\]",
        r"#\[inline\]", r"#\[doc = ",
        r"#\s*(Copyright|License|Author):",
        r"async fn", r"async fn",
    ],
    "kotlin": [
        r"/\*\*[^/]*@param", r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP):",
        r"fun \w+", r"class \w+",
        r"/\*\*[^/]*@return", r"/\*\*[^/]*@throws",
        r"/\*\*[^/]*@see", r"/\*\*[^/]*@since",
        r"/\*\*[^/]*@deprecated", r"/\*\*[^/]*@author",
        r"/\*\*[^/]*@property", r"/\*\*[^/]*@sample",
        r"data class", r"sealed class",
        r"open class", r"abstract class",
        r"inner class", r"companion object",
        r"interface \w+", r"enum class",
        r"object \w+", r"typealias \w+",
        r"inline fun", r"suspend fun",
        r"tailrec fun", r"operator fun",
        r"fun \w+\.\w+",
        r"val \w+: \w+", r"var \w+: \w+",
        r"@Override", r"@JvmStatic",
        r"@JvmOverloads", r"@JvmName",
    ],
    "csharp": [
        r"///\s*<summary>", r"//\s*(TODO|FIXME|HACK|NOTE|XXX|REVIEW|BUG|WORKAROUND|TEMP|OPTIMIZE):",
        r"public class", r"private class",
        r"///\s*<param", r"///\s*<returns>",
        r"///\s*<exception", r"///\s*<example>",
        r"///\s*<remarks>", r"///\s*<value>",
        r"///\s*<seealso", r"///\s*<see ",
        r"///\s*<typeparam", r"///\s*<permission",
        r"///\s*<inheritdoc",
        r"public interface", r"private interface",
        r"public struct", r"private struct",
        r"public enum", r"private enum",
        r"public record", r"abstract class",
        r"sealed class", r"static class",
        r"partial class", r"readonly struct",
        r"async Task", r"async ValueTask",
        r"#region", r"#endregion",
        r"\[Attribute", r"\[Obsolete",
        r"\[Serializable", r"\[DataContract",
        r"//\s*(Copyright|License|Author):",
        r"namespace \w+",
        r"using System",
        r"get; set;", r"get; private set;",
        r"init;", r"required ",
    ],
}

MODULE_INDICATORS = {
    "python": ["__init__.py"],
    "typescript": ["package.json", "tsconfig.json", "index.ts", "index.tsx", "index.js"],
    "javascript": ["package.json", "index.js", "index.jsx"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts", "module-info.java"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml", "lib.rs", "main.rs"],
    "kotlin": ["build.gradle.kts"],
    "csharp": [".csproj"],
}


class CodeQualityAnalyzer:
    def __init__(self, scan_result):
        self.scan_result = scan_result
        self.files = scan_result.get("files", [])
        self.languages = scan_result.get("languages", {})
        self.linter_score = 0.0
        self.type_checker_score = 0.0
        self.documentation_score = 0.0
        self.module_score = 0.0

    def _has_file(self, name_variants):
        names = set(f["name"] for f in self.files)
        for v in name_variants:
            if v in names:
                return True
        return False

    def _check_linters(self):
        if not self.languages:
            return 5.0

        detected = 0
        possible = 0
        for lang in self.languages:
            for tool, configs in LINTER_CONFIGS.items():
                if self._has_file(configs):
                    detected += 1
                    break

        total_langs = len(self.languages)
        if total_langs == 0:
            return 5.0

        ratio = min(detected / total_langs, 1.0) if total_langs > 0 else 0
        return 2.0 + ratio * 8.0

    def _check_type_checkers(self):
        detected = 0
        for lang in self.languages:
            if lang == "typescript":
                files = [f for f in self.files if f["language"] == "typescript"]
                tsconfigs = [f for f in files if f["name"] == "tsconfig.json"]
                for tc in tsconfigs:
                    try:
                        full_path = os.path.join(self.scan_result.get("project_root", ""), tc["path"])
                        if os.path.isfile(full_path):
                            content = open(full_path, "r", encoding="utf-8", errors="replace").read()
                            if '"strict"' in content or '"strictNullChecks"' in content:
                                detected += 2
                                break
                    except Exception:
                        pass
                if detected == 0 and tsconfigs:
                    detected += 1

            for tool, configs in TYPE_CHECKER_CONFIGS.items():
                if lang in ("python", "typescript", "javascript") or tool == lang:
                    if self._has_file(configs):
                        detected += 1

        total = len(self.languages)
        if total == 0:
            return 5.0
        ratio = min(detected / max(total, 1), 1.0)
        return 2.0 + ratio * 8.0

    def _check_documentation(self):
        score = 2.0
        has_readme = self._has_file(["README.md", "README.txt", "README.rst", "README"])
        if has_readme:
            score += 2.0

        documented_langs = 0
        total_langs_with_src = 0
        for lang, patterns in DOC_PATTERNS.items():
            lang_files = [f for f in self.files if f["language"] == lang]
            if not lang_files:
                continue
            total_langs_with_src += 1
            has_docs = False
            examined = 0
            for f in lang_files:
                if examined >= 10:
                    break
                full_path = os.path.join(self.scan_result.get("project_root", ""), f["path"])
                if not os.path.isfile(full_path) or f.get("size", 0) > 512 * 1024:
                    continue
                try:
                    content = open(full_path, "r", encoding="utf-8", errors="replace").read()
                    for pat in patterns:
                        if re.search(pat, content, re.MULTILINE):
                            has_docs = True
                            break
                except Exception:
                    pass
                examined += 1
                if has_docs:
                    break
            if has_docs:
                documented_langs += 1

        if total_langs_with_src > 0:
            ratio = documented_langs / total_langs_with_src
            score += ratio * 6.0

        return min(score, 10.0)

    def _check_module_organization(self):
        if not self.languages:
            return 5.0

        total_score = 0.0
        lang_count = 0
        for lang, indicators in MODULE_INDICATORS.items():
            if lang not in self.languages:
                continue
            lang_count += 1
            lang_files = [f for f in self.files if f["language"] == lang]
            if not lang_files:
                continue

            has_module_indicators = self._has_file(indicators)
            if has_module_indicators:
                total_score += 4.0

            dirs_used = set(os.path.dirname(f["path"]) for f in lang_files)
            if len(dirs_used) > 1:
                total_score += 3.0

            if len(lang_files) > 3 and len(dirs_used) >= 2:
                total_score += 3.0

        if lang_count == 0:
            return 5.0
        return min(total_score / lang_count, 10.0)

    def analyze(self):
        self.linter_score = self._check_linters()
        self.type_checker_score = self._check_type_checkers()
        self.documentation_score = self._check_documentation()
        self.module_score = self._check_module_organization()

        overall = round(
            self.linter_score * 0.30
            + self.type_checker_score * 0.25
            + self.documentation_score * 0.25
            + self.module_score * 0.20,
            2,
        )

        completeness_bonus = 0.0
        all_perfect = (
            round(self.linter_score, 1) >= 10.0
            and round(self.type_checker_score, 1) >= 10.0
            and round(self.documentation_score, 1) >= 10.0
            and round(self.module_score, 1) >= 10.0
        )

        if all_perfect:
            completeness_bonus = 1.0
            overall = 10.0

        return {
            "overall": overall,
            "dimensions": {
                "linter": {"score": round(self.linter_score, 1), "weight": 0.30},
                "type_checker": {"score": round(self.type_checker_score, 1), "weight": 0.25},
                "documentation": {"score": round(self.documentation_score, 1), "weight": 0.25},
                "module_organization": {"score": round(self.module_score, 1), "weight": 0.20},
            },
            "details": {
                "linter_configs_found": [
                    tool for tool in LINTER_CONFIGS if self._has_file(LINTER_CONFIGS[tool])
                ],
                "has_readme": self._has_file(["README.md", "README.txt", "README.rst", "README"]),
                "documented_languages": [
                    lang for lang in DOC_PATTERNS
                    if any(f["language"] == lang for f in self.files)
                ],
                "module_indicators": [
                    ind for ind_group in MODULE_INDICATORS.values()
                    for ind in ind_group
                    if ind in set(f["name"] for f in self.files)
                ],
            },
        }
