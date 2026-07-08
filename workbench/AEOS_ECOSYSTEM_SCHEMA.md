# AEOS Ecosystem Schema — v1.0.0

## 1. Propósito

Define o schema do mapa de ecossistema gerado pelo Scanner. Este documento serve como contrato de dados entre Scanner, Report Generators e ferramentas de análise.

## 2. Ecosystem Map Schema

```yaml
ecosystem_map:
  version: "1.0.0"
  scan_timestamp: "ISO 8601"
  project_root: "path/to/project"
  
  metadata:
    project_name: "string"
    project_type: "string"
    total_files: number
    total_dirs: number
    total_lines: number
    languages: ["language", ...]
    
  stacks:
    - name: "java"
      detected: true
      confidence: 0.95
      evidence:
        - "pom.xml found"
        - "src/main/java/ found"
      frameworks: ["spring-boot", "spring-mvc"]
      build_tools: ["maven", "gradle"]
      version: "21"
      files_count: 150
      
  languages:
    - name: "Java"
      version: "21"
      files: 120
      lines: 15000
    - name: "TypeScript"
      version: "5.5"
      files: 30
      lines: 4000
      
  dependencies:
    - name: "spring-boot-starter-web"
      version: "3.3.0"
      type: "maven"
      scope: "compile"
      licenses: ["Apache-2.0"]
    - name: "express"
      version: "4.19.0"
      type: "npm"
      scope: "production"
      
  architecture:
    patterns: ["microservices", "clean-architecture"]
    layers: ["presentation", "application", "domain", "infrastructure"]
    api: ["rest", "graphql"]
    database: ["postgresql", "mongodb"]
    messaging: ["kafka", "rabbitmq"]
    
  services:
    - name: "api-gateway"
      type: "spring-cloud-gateway"
      port: 8080
      language: "java"
      dependencies: ["service-a", "service-b"]
      
  risks:
    - id: "risk-001"
      category: "security"
      severity: "high"
      description: "Dependency CVE-2024-XXXX"
      affected: ["spring-boot-starter-web:3.3.0"]
      recommendation: "Update to 3.3.1+"
      
  docker:
    has_dockerfile: true
    dockerfiles: ["Dockerfile", "Dockerfile.dev"]
    compose: ["docker-compose.yml"]
    images: ["openjdk:21", "node:20-alpine"]
    
  ci:
    providers: ["github-actions", "gitlab-ci"]
    configs: [".github/workflows/ci.yml"]
    
  tests:
    frameworks: ["junit5", "jest", "pytest"]
    coverage: 0.72
    total_tests: 350
```

## 3. Tipos de Evidência para Scanner

| Tipo | Descrição | Exemplos |
|------|-----------|----------|
| file | Arquivo encontrado | pom.xml, build.gradle, package.json |
| config | Configuração detectada | spring.application.name, server.port |
| pattern | Padrão arquitetural | @RestController, @Service, @Repository |
| dependency | Dependência identificada | spring-boot-starter-web:3.3.0 |
| metric | Métrica coletada | 150 Java files, 72% coverage |

## 4. Confidence Scoring

| Score | Significado |
|-------|-------------|
| 1.0 | Certeza absoluta (ex: pom.xml presente) |
| 0.9 | Evidência forte (pacote Java + Maven + Spring) |
| 0.7-0.8 | Evidência moderada (arquivos típicos) |
| 0.5-0.6 | Evidência fraca (arquivos isolados) |
| < 0.5 | Palpite (nenhuma evidência direta) |
