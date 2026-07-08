"""Stack Detector - identifies technology stacks from scan results with file-scoped accuracy."""

import re
import os


STACK_DEFINITIONS = {
    "java-spring": {
        "name": "Java / Spring Boot",
        "languages": ["java"],
        "indicators": ["pom.xml", "build.gradle", "build.gradle.kts", "application.yml", "application.properties"],
        "frameworks": ["spring", "spring-boot", "spring-mvc", "spring-cloud"],
        "frameworks_patterns": [
            r"spring-boot-starter", r"@SpringBootApplication", r"@RestController",
            r"spring-cloud", r"spring-boot-maven-plugin", r"SpringApplication",
            r"@EnableAutoConfiguration", r"@SpringBootTest",
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
            r"jakarta\.ws", r"jakarta\.persistence", r"javax\.persistence",
            r"@Entity", r"@Stateless", r"@Stateful", r"javax\.ws",
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
            r"from fastapi", r"import fastapi", r"FastAPI\(\)",
            r"@app\.(get|post|put|delete|patch)", r"APIRouter", r"uvicorn\.run",
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
            r"from django", r"django\.urls", r"django\.contrib", r"django\.db",
            r"django\.http", r"django\.conf", r"WSGI_APPLICATION", r"ROOT_URLCONF",
            r"python manage\.py", r"django-admin",
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
            r"from flask", r"import flask", r"Flask\(", r"@app\.route",
            r"flask\.Blueprint", r"flask_sqlalchemy", r"flask_login",
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
            r"from langchain", r"from llama_index", r"import openai",
            r"from openai", r"Chroma", r"Pinecone", r"Weaviate", r"FAISS",
            r"RetrievalQA", r"VectorStore", r"Embedding", r"OpenAIEmbeddings",
            r"ChatOpenAI", r"from transformers", r"import torch",
            r"AutoModelForCausalLM", r"RAGPipeline",
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
            r"from ['\"]react['\"]", r"import React", r"from ['\"]next/",
            r"@vite", r"React\.createElement", r"jsx", r"tsx",
            r"create-react-app", r"react-dom", r"useState", r"useEffect",
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
            r"from ['\"]vue['\"]", r"import Vue", r"createApp\(", r"\.vue",
            r"v-bind", r"v-model", r"v-if", r"v-for", r"<template>",
            r"Vue\.component", r"defineComponent",
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
            r"from ['\"]express['\"]", r"require\(['\"]express['\"]\)",
            r"@nestjs", r"from ['\"]fastify['\"]", r"from ['\"]koa['\"]",
            r"app\.(get|post|put|delete|listen)", r"Router\(\)",
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
            r"github\.com/gin-gonic/gin", r"github\.com/labstack/echo",
            r"github\.com/gofiber/fiber", r"package main", r"fmt\.Print",
            r"net/http", r"database/sql", r"github\.com/gorilla",
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
            r"actix-web", r"axum::", r"rocket::", r"tokio::",
            r"fn main", r"let mut", r"-> Result", r"#\[derive\(",
            r"cargo", r"impl ", r"match ", r"use ",
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
            r"using System", r"namespace ", r"class Program", r"static void Main",
            r"ConfigureServices", r"Configure\(", r"app\.[A-Z]",
            r"Microsoft\.AspNetCore", r"DbContext",
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
            r"import android", r"@Composable", r"fun \w+\(\)",
            r"MainActivity", r"onCreate", r"setContent",
            r"androidx\.", r"R\.layout\.",
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
            r"import 'package:flutter", r"MaterialApp\(", r"Scaffold\(",
            r"runApp\(", r"StatelessWidget", r"StatefulWidget",
            r"@override", r"Widget build",
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
            r"terraform \{", r"provider ", r"resource ", r"data ",
            r"variable ", r"output ", r"module ", r"terraform\.",
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
            r"apiVersion: apps/v1", r"kind: Deployment", r"kind: Service",
            r"kind: Ingress", r"kind: ConfigMap", r"kind: Secret",
            r"spec:\n\s+containers:", r"kubectl",
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
            r"FROM ", r"COPY ", r"RUN ", r"CMD ", r"EXPOSE ",
            r"docker-compose", r"services:",
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

    def _check_indicator(self, indicator):
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
        for f in relevant_files:
            text = self._get_file_text(f)
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _check_language(self, lang):
        if lang == "all":
            return True
        return lang in self.languages

    def detect(self):
        detected = []

        for stack_id, definition in STACK_DEFINITIONS.items():
            score = 0.0
            reasons = []
            missing = []

            if not self._check_language(definition["languages"][0]) and definition["languages"][0] != "all":
                if definition["languages"][0] != "all":
                    continue

            for indicator in definition["indicators"]:
                if self._check_indicator(indicator):
                    score += 0.2
                    reasons.append("Found " + indicator)

            pattern_lang = definition["languages"][0]
            pattern_matches = 0
            for pattern in definition["frameworks_patterns"]:
                if self._check_pattern_in_scope(pattern, pattern_lang):
                    pattern_matches += 1
                    if pattern_matches <= 3:
                        reasons.append("Pattern: " + pattern)

            score += min(pattern_matches * 0.2, 0.6)

            for npattern in definition.get("negative_patterns", []):
                if self._check_pattern_in_scope(npattern, pattern_lang):
                    score -= 0.4
                    reasons.append("Negative match (anti-pattern): " + npattern)

            if definition.get("build_tools"):
                for bt in definition["build_tools"]:
                    if bt in str(self.scan_result.get("file_categories", {})):
                        score += 0.1
                        reasons.append("Build tool: " + bt)

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
            if confidence >= min_conf:
                detected.append({
                    "id": stack_id,
                    "name": definition["name"],
                    "confidence": confidence,
                    "evidence": reasons,
                    "missing": missing,
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
            ev.append({
                "evidence_id": "evt-stack-" + stack["id"],
                "type": "config",
                "claim": "Stack detected: " + stack["name"] + " (confidence: " + str(stack["confidence"]) + ")",
                "reference": "stack." + stack["id"],
                "hash": self.scan_result.get("scan_id", "unknown"),
                "timestamp": self.scan_result.get("scan_timestamp", ""),
                "verified": True,
            })
