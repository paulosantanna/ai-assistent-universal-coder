"""Stack Detector — identifies technology stacks with real file indicators and evidence."""

import re
import os


STACK_DEFINITIONS = {
    "java-spring": {
        "name": "Java / Spring Boot",
        "languages": ["java"],
        "indicators": ["pom.xml", "build.gradle", "build.gradle.kts", "application.yml", "application.properties"],
        "frameworks": ["spring", "spring-boot", "spring-mvc", "spring-cloud"],
        "frameworks_patterns": [
            (r"spring-boot-starter", "spring-boot-starter dependency"),
            (r"@SpringBootApplication", "@SpringBootApplication annotation"),
            (r"@RestController", "@RestController annotation"),
            (r"spring-cloud", "spring-cloud dependency"),
            (r"@EnableAutoConfiguration", "@EnableAutoConfiguration"),
            (r"SpringApplication\.run", "SpringApplication.run()"),
            (r"@SpringBootTest", "@SpringBootTest annotation"),
        ],
        "negative_patterns": [],
        "build_tools": ["maven", "gradle"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "java-ee": {
        "name": "Java EE / Jakarta",
        "languages": ["java"],
        "indicators": ["pom.xml", "build.gradle", "src/main/webapp/WEB-INF/web.xml"],
        "frameworks": ["jakarta-ee", "java-ee", "jakarta"],
        "frameworks_patterns": [
            (r"jakarta\.ws", "jakarta.ws import"),
            (r"jakarta\.persistence", "jakarta.persistence import"),
            (r"javax\.persistence", "javax.persistence import (legacy)"),
            (r"@Entity", "@Entity annotation"),
            (r"@Stateless", "@Stateless annotation (EJB)"),
            (r"javax\.ws", "javax.ws import (legacy JAX-RS)"),
        ],
        "negative_patterns": [r"spring-boot-starter", r"@SpringBootApplication"],
        "build_tools": ["maven", "gradle"],
        "confidence_base": 0.85,
        "min_indicators": 1,
    },
    "python-fastapi": {
        "name": "Python / FastAPI",
        "languages": ["python"],
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
        "frameworks": ["fastapi", "uvicorn", "pydantic"],
        "frameworks_patterns": [
            (r"from fastapi", "from fastapi import"),
            (r"FastAPI\(\)", "FastAPI() app instance"),
            (r"@app\.(get|post|put|delete|patch)", "FastAPI route decorator"),
            (r"APIRouter", "APIRouter usage"),
            (r"uvicorn\.run", "uvicorn.run()"),
        ],
        "negative_patterns": [r"from django", r"from flask"],
        "build_tools": ["pip", "poetry"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "python-django": {
        "name": "Python / Django",
        "languages": ["python"],
        "indicators": ["requirements.txt", "pyproject.toml", "manage.py", "setup.cfg", "uwsgi.ini"],
        "frameworks": ["django", "django-rest-framework"],
        "frameworks_patterns": [
            (r"from django", "from django import"),
            (r"django\.urls", "django.urls module"),
            (r"django\.contrib", "django.contrib module"),
            (r"django\.db", "django.db module"),
            (r"django\.http", "django.http module"),
            (r"WSGI_APPLICATION", "WSGI_APPLICATION config"),
            (r"ROOT_URLCONF", "ROOT_URLCONF config"),
        ],
        "negative_patterns": [r"from fastapi", r"from flask"],
        "build_tools": ["pip", "poetry"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "python-flask": {
        "name": "Python / Flask",
        "languages": ["python"],
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py"],
        "frameworks": ["flask", "jinja2", "werkzeug"],
        "frameworks_patterns": [
            (r"from flask", "from flask import"),
            (r"Flask\(", "Flask() app instance"),
            (r"@app\.route", "Flask route decorator"),
            (r"flask\.Blueprint", "flask.Blueprint"),
            (r"flask_sqlalchemy", "Flask-SQLAlchemy"),
        ],
        "negative_patterns": [r"from django", r"from fastapi"],
        "build_tools": ["pip", "poetry"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "python-ai-rag": {
        "name": "Python / AI + RAG",
        "languages": ["python"],
        "indicators": ["requirements.txt", "pyproject.toml"],
        "frameworks": ["langchain", "llamaindex", "openai", "rag", "vector-db", "chroma", "pinecone"],
        "frameworks_patterns": [
            (r"from langchain", "LangChain import"),
            (r"from llama_index", "LlamaIndex import"),
            (r"from openai", "OpenAI import"),
            (r"Chroma", "Chroma vector DB usage"),
            (r"Pinecone", "Pinecone vector DB usage"),
            (r"RetrievalQA", "LangChain RetrievalQA"),
            (r"VectorStore", "VectorStore implementation"),
            (r"OpenAIEmbeddings", "OpenAI Embeddings"),
            (r"ChatOpenAI", "ChatOpenAI usage"),
            (r"from transformers", "HuggingFace Transformers"),
            (r"AutoModelForCausalLM", "AutoModelForCausalLM"),
        ],
        "negative_patterns": [],
        "build_tools": ["pip", "poetry"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "typescript-react": {
        "name": "TypeScript / React",
        "languages": ["typescript", "javascript"],
        "indicators": ["package.json", "tsconfig.json", "vite.config.ts", "vite.config.js"],
        "frameworks": ["react", "next.js", "remix", "vite"],
        "frameworks_patterns": [
            (r"from ['\"]react['\"]", "React import"),
            (r"from ['\"]next/", "Next.js import"),
            (r"React\.createElement", "React.createElement"),
            (r"react-dom", "react-dom import"),
            (r"useState", "React useState hook"),
            (r"useEffect", "React useEffect hook"),
        ],
        "negative_patterns": [r"from ['\"]vue['\"]", r"from ['\"]angular"],
        "build_tools": ["npm"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "typescript-vue": {
        "name": "TypeScript / Vue.js",
        "languages": ["typescript", "javascript"],
        "indicators": ["package.json", "tsconfig.json", "vue.config.js", "nuxt.config.ts"],
        "frameworks": ["vue", "vuex", "pinia", "nuxt", "vite"],
        "frameworks_patterns": [
            (r"from ['\"]vue['\"]", "Vue import"),
            (r"createApp\(", "Vue createApp()"),
            (r"\.vue", "Vue single-file component (.vue)"),
            (r"v-bind", "Vue v-bind directive"),
            (r"v-model", "Vue v-model directive"),
            (r"defineComponent", "Vue defineComponent"),
        ],
        "negative_patterns": [r"from ['\"]react['\"]"],
        "build_tools": ["npm"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "typescript-node": {
        "name": "TypeScript / Node.js",
        "languages": ["typescript", "javascript"],
        "indicators": ["package.json", "tsconfig.json"],
        "frameworks": ["express", "fastify", "nestjs", "hono", "koa"],
        "frameworks_patterns": [
            (r"from ['\"]express['\"]", "Express import"),
            (r"require\(['\"]express['\"]\)", "Express require"),
            (r"@nestjs", "NestJS import"),
            (r"from ['\"]fastify['\"]", "Fastify import"),
            (r"app\.(get|post|put|delete|listen)", "Express route handler"),
            (r"Router\(\)", "Express Router"),
        ],
        "negative_patterns": [r"from ['\"]react['\"]", r"from ['\"]vue['\"]"],
        "build_tools": ["npm"],
        "confidence_base": 0.85,
        "min_indicators": 1,
    },
    "go": {
        "name": "Go",
        "languages": ["go"],
        "indicators": ["go.mod", "go.sum"],
        "frameworks": ["gin", "echo", "fiber", "chi", "gorilla", "gorm"],
        "frameworks_patterns": [
            (r"github\.com/gin-gonic/gin", "Gin web framework"),
            (r"github\.com/labstack/echo", "Echo web framework"),
            (r"github\.com/gofiber/fiber", "Fiber web framework"),
            (r"net/http", "net/http standard library"),
        ],
        "negative_patterns": [],
        "build_tools": ["go-mod"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "rust": {
        "name": "Rust",
        "languages": ["rust"],
        "indicators": ["Cargo.toml", "Cargo.lock"],
        "frameworks": ["actix", "axum", "rocket", "tokio", "warp"],
        "frameworks_patterns": [
            (r"actix-web", "Actix Web framework"),
            (r"axum::", "Axum web framework"),
            (r"rocket::", "Rocket web framework"),
            (r"tokio::", "Tokio async runtime"),
            (r"#\[derive\(", "Rust derive macro"),
        ],
        "negative_patterns": [],
        "build_tools": ["cargo"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "dotnet": {
        "name": ".NET / C#",
        "languages": ["csharp"],
        "indicators": [".csproj", "*.sln", "Program.cs", "Startup.cs", "appsettings.json"],
        "frameworks": ["aspnet", "entity-framework", "blazor", "xunit", "nunit"],
        "frameworks_patterns": [
            (r"using System", "System namespace"),
            (r"ConfigureServices", "ASP.NET ConfigureServices"),
            (r"Microsoft\.AspNetCore", "ASP.NET Core import"),
            (r"DbContext", "Entity Framework DbContext"),
        ],
        "negative_patterns": [],
        "build_tools": ["dotnet"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "kotlin-android": {
        "name": "Kotlin / Android",
        "languages": ["kotlin"],
        "indicators": ["build.gradle.kts", "AndroidManifest.xml", "gradle.properties"],
        "frameworks": ["android", "jetpack", "compose", "ktor"],
        "frameworks_patterns": [
            (r"import android", "Android SDK import"),
            (r"@Composable", "Jetpack Compose"),
            (r"MainActivity", "Android MainActivity"),
            (r"onCreate", "Android Activity.onCreate"),
            (r"androidx\.", "AndroidX library"),
        ],
        "negative_patterns": [],
        "build_tools": ["gradle"],
        "confidence_base": 0.90,
        "min_indicators": 1,
    },
    "flutter-dart": {
        "name": "Flutter / Dart",
        "languages": ["dart"],
        "indicators": ["pubspec.yaml", "pubspec.lock", "analysis_options.yaml"],
        "frameworks": ["flutter", "dart", "material-design"],
        "frameworks_patterns": [
            (r"import 'package:flutter", "Flutter package import"),
            (r"MaterialApp\(", "Flutter MaterialApp"),
            (r"Scaffold\(", "Flutter Scaffold widget"),
            (r"runApp\(", "Flutter runApp()"),
            (r"StatelessWidget", "Flutter StatelessWidget"),
            (r"StatefulWidget", "Flutter StatefulWidget"),
        ],
        "negative_patterns": [],
        "build_tools": ["pub"],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "terraform": {
        "name": "Terraform / IaC",
        "languages": ["hcl"],
        "indicators": [".terraform.lock.hcl", "provider.tf", "main.tf", "variables.tf", "outputs.tf"],
        "frameworks": ["terraform", "opentofu"],
        "frameworks_patterns": [
            (r"terraform \{", "Terraform HCL block"),
            (r"provider ", "Terraform provider"),
            (r"resource ", "Terraform resource"),
            (r"variable ", "Terraform variable"),
            (r"output ", "Terraform output"),
            (r"module ", "Terraform module"),
        ],
        "negative_patterns": [],
        "build_tools": [],
        "confidence_base": 0.95,
        "min_indicators": 1,
    },
    "kubernetes": {
        "name": "Kubernetes",
        "languages": ["yaml"],
        "indicators": ["kustomization.yaml", "Chart.yaml", "values.yaml", "kubeconfig"],
        "frameworks": ["kubernetes", "helm", "kustomize", "argocd"],
        "frameworks_patterns": [
            (r"apiVersion: apps/v1", "K8s apps/v1 API version"),
            (r"kind: Deployment", "K8s Deployment resource"),
            (r"kind: Service", "K8s Service resource"),
            (r"kind: Ingress", "K8s Ingress resource"),
            (r"kind: ConfigMap", "K8s ConfigMap resource"),
        ],
        "negative_patterns": [],
        "build_tools": [],
        "confidence_base": 0.85,
        "min_indicators": 1,
    },
    "fullstack-docker": {
        "name": "Fullstack / Docker",
        "languages": ["all"],
        "indicators": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"],
        "frameworks": ["docker", "docker-compose"],
        "frameworks_patterns": [
            (r"FROM ", "Dockerfile FROM instruction"),
            (r"COPY ", "Dockerfile COPY instruction"),
            (r"RUN ", "Dockerfile RUN instruction"),
            (r"CMD ", "Dockerfile CMD instruction"),
            (r"docker-compose", "docker-compose reference"),
            (r"services:", "docker-compose services block"),
        ],
        "negative_patterns": [],
        "build_tools": [],
        "confidence_base": 0.80,
        "min_indicators": 0,
    },
}


class StackDetector:
    def __init__(self, scan_result):
        self.scan_result = scan_result
        self.files = scan_result.get("files", [])
        self.languages = scan_result.get("languages", {})
        self.file_paths = [f["path"] for f in self.files]
        self.file_names = [f["name"] for f in self.files]

        self._file_contents = {}
        self._file_by_language = {}
        for f in self.files:
            lang = f.get("language", "other")
            if lang not in self._file_by_language:
                self._file_by_language[lang] = []
            self._file_by_language[lang].append(f)

    def _get_file_text(self, f):
        path = f.get("path", "")
        if path in self._file_contents:
            return self._file_contents[path]
        full_path = os.path.join(self.scan_result.get("project_root", ""), path)
        try:
            if os.path.isfile(full_path) and os.path.getsize(full_path) < 512 * 1024:
                with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                    self._file_contents[path] = text
                    return text
        except Exception:
            pass
        self._file_contents[path] = ""
        return ""

    def _check_indicator_file(self, indicator, f):
        path = f.get("path", "")
        name = f.get("name", "")
        if indicator.startswith("*."):
            return f.get("ext", "") == indicator[1:]
        return indicator in path or indicator == name

    def _check_indicator_file_path(self, indicator):
        if indicator.startswith("*."):
            ext = indicator[1:]
            return any(f["ext"] == ext for f in self.files)
        return any(indicator in p for p in self.file_paths) or any(
            indicator == n for n in self.file_names
        )

    def _check_pattern_in_scope(self, pattern, language):
        relevant_files = self._file_by_language.get(language, [])
        if language == "all":
            relevant_files = self.files
        matched_files = []
        for f in relevant_files:
            text = self._get_file_text(f)
            if re.search(pattern, text, re.IGNORECASE):
                matched_files.append(f)
        return matched_files

    def _check_language(self, lang):
        if lang == "all":
            return True
        return lang in self.languages

    def detect(self):
        detected = []
        for stack_id, definition in STACK_DEFINITIONS.items():
            score = 0.0
            indicators: list[dict] = []
            files_inspected: list[str] = []

            if not self._check_language(definition["languages"][0]) and definition["languages"][0] != "all":
                continue

            for indicator in definition["indicators"]:
                if self._check_indicator_file_path(indicator):
                    score += 0.2
                    matching_files = [f for f in self.files if self._check_indicator_file_path(indicator)]
                    for mf in matching_files:
                        if indicator.startswith("*."):
                            ev = f"File with extension {indicator}: {mf['path']}"
                        else:
                            ev = f"Found file: {mf['path']}"
                        indicators.append({
                            "file": mf["path"],
                            "evidence": ev,
                        })
                        files_inspected.append(mf["path"])

            pattern_lang = definition["languages"][0]
            pattern_matches = 0
            for pattern, label in definition["frameworks_patterns"]:
                matched_files = self._check_pattern_in_scope(pattern, pattern_lang)
                for mf in matched_files:
                    mf_path = mf.get("path", "")
                    if mf_path not in files_inspected:
                        files_inspected.append(mf_path)
                    indicators.append({
                        "file": mf_path,
                        "evidence": label,
                    })
                    pattern_matches += 1

            score += min(pattern_matches * 0.2, 0.6)

            for npattern in definition.get("negative_patterns", []):
                if self._check_pattern_in_scope(npattern, pattern_lang):
                    score -= 0.4

            if definition.get("build_tools"):
                for bt in definition["build_tools"]:
                    if bt in str(self.scan_result.get("file_categories", {})):
                        score += 0.1

            lang_key = definition["languages"][0]
            file_count = 0
            if lang_key == "all":
                file_count = self.scan_result.get("total_files", 0)
            else:
                file_count = self.languages.get(lang_key, {}).get("files", 0)

            if file_count > 100:
                score += 0.1
            elif file_count > 30:
                score += 0.05

            confidence = min(score, 1.0) * definition["confidence_base"] if score > 0 else 0.0
            confidence = round(confidence, 2)

            min_conf = 0.3 if stack_id == "fullstack-docker" else 0.4

            has_real_indicator = len(indicators) > 0

            if confidence >= min_conf and has_real_indicator:
                detected.append({
                    "stack_name": stack_id,
                    "name": definition["name"],
                    "category": "framework",
                    "confidence": confidence,
                    "fact_or_assumption": "fact" if len([i for i in indicators if "File" in i["evidence"] or "import" in i["evidence"]]) > 0 else "assumption",
                    "indicators": indicators,
                    "files_inspected": list(dict.fromkeys(files_inspected)),
                    "frameworks": definition["frameworks"],
                    "build_tools": definition["build_tools"],
                    "language": definition["languages"][0],
                    "detected": True,
                })

        detected.sort(key=lambda s: s["confidence"], reverse=True)

        self._add_evidence(detected)
        return detected

    def _add_evidence(self, stacks):
        ev = self.scan_result.setdefault("evidence", [])
        for stack in stacks:
            indicator_count = len(stack.get("indicators", []))
            ev.append({
                "evidence_id": "evt-stack-" + stack["stack_name"],
                "type": "config",
                "claim": "Stack detected: " + stack["name"] + " (confidence: " + str(stack["confidence"]) + ", indicators: " + str(indicator_count) + ")",
                "reference": "stack." + stack["stack_name"],
                "hash": self.scan_result.get("scan_id", "unknown"),
                "timestamp": self.scan_result.get("scan_timestamp", ""),
                "verified": True,
            })