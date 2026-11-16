// Deterministic engine shared by the AWS and Azure architecture MCPs.
// Decisions are code: the knowledge base supplies cited facts (claim ids) and the price snapshot supplies
// SKU prices. JEV probabilities are triage metadata and never drive a decision here.
import { readFileSync } from "node:fs";
import { join } from "node:path";

export const HOURS_PER_MONTH = 730;
// Async inference scales to zero only for cases that tolerate a cold start of a few minutes (AWS ML blog, Medidata).
export const COLD_START_TOLERANCE_S = 300;

const KINDS = new Set(["http-api", "model-server", "worker-jobs", "otlp-receiver", "desktop-app", "mcp-stdio"]);
const STATES = new Set(["postgres", "vector", "object", "object-audit", "graph", "jsonl", "none"]);
const CLASSES = new Set(["public", "internal", "personal", "sensitive"]);
const PROVIDERS = new Set(["aws", "azure"]);
const SENSITIVE = new Set(["personal", "sensitive"]);

const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));
const items = (value) => (Array.isArray(value) ? value : value === undefined || value === null ? [] : [value]);
const round2 = (value) => Math.round(value * 100) / 100;

export function createKb(root) {
  const evidence = readJson(join(root, "evidence", "claims.json"));
  const claims = new Map(evidence.claims.map((claim) => [claim.id, claim]));
  const knowledge = {};
  const prices = {};
  for (const provider of PROVIDERS) {
    knowledge[provider] = readJson(join(root, "providers", provider, "knowledge.json"));
    prices[provider] = readJson(join(root, "providers", provider, "prices.json"));
  }
  return { claims, knowledge, prices, evidence_meta: { jev_question_run: evidence.jev_question_run, jev_thresholds: evidence.jev_thresholds } };
}

function claimView(kb, id) {
  const claim = kb.claims.get(id);
  if (!claim) throw new Error(`Unknown claim id: ${id}`);
  return { id, claim: claim.claim, source_url: claim.source_url, final_label: claim.final_label, control: claim.control };
}

export function listPatterns(kb, provider, { category } = {}) {
  return kb.knowledge[provider].patterns
    .filter((pattern) => !category || pattern.category === category)
    .map(({ id, title, category: cat, use_when }) => ({ id, title, category: cat, use_when }));
}

export function getPattern(kb, provider, id) {
  const pattern = kb.knowledge[provider].patterns.find((item) => item.id === id);
  if (!pattern) throw new Error(`Unknown pattern id: ${id}`);
  return { ...pattern, claims: pattern.claims.map((claimId) => claimView(kb, claimId)) };
}

export function listPitfalls(kb, provider) {
  return kb.knowledge[provider].pitfalls.map((pitfall) => ({
    id: pitfall.id,
    title: pitfall.title,
    wrong_assumption: pitfall.wrong_assumption,
    correct_fact: pitfall.correct_fact,
    rule_ids: pitfall.rule_ids,
    claims: pitfall.claims.map((id) => claimView(kb, id)),
    rejected_claims: pitfall.trap_claims.map((id) => claimView(kb, id)),
    evidence_note: pitfall.evidence_note ?? null,
    project_sources: pitfall.project_sources ?? [],
  }));
}

// Knowledge integrity: references resolve, supporting claims are supported, rejected claims are not.
export function validateKnowledge(kb) {
  const problems = [];
  const ruleIds = new Set(RULES.map((rule) => rule.id));
  const supported = (id) => kb.claims.get(id)?.final_label.startsWith("supported");
  for (const provider of PROVIDERS) {
    for (const pattern of kb.knowledge[provider].patterns) {
      for (const id of pattern.claims) {
        if (!kb.claims.has(id)) problems.push(`${pattern.id}: unknown claim ${id}`);
        else if (!supported(id)) problems.push(`${pattern.id}: claim ${id} is not supported`);
      }
    }
    for (const pitfall of kb.knowledge[provider].pitfalls) {
      for (const id of pitfall.claims) {
        if (!kb.claims.has(id)) problems.push(`${pitfall.id}: unknown claim ${id}`);
        else if (!supported(id)) problems.push(`${pitfall.id}: supporting claim ${id} is not supported`);
      }
      for (const id of pitfall.trap_claims) {
        if (!kb.claims.has(id)) problems.push(`${pitfall.id}: unknown rejected claim ${id}`);
        else if (supported(id)) problems.push(`${pitfall.id}: rejected claim ${id} is supported`);
      }
      for (const ruleId of pitfall.rule_ids) if (!ruleIds.has(ruleId)) problems.push(`${pitfall.id}: unknown rule ${ruleId}`);
      const hasEvidence = pitfall.claims.length + pitfall.trap_claims.length > 0 || pitfall.evidence_note || pitfall.project_sources;
      if (!hasEvidence) problems.push(`${pitfall.id}: no evidence`);
    }
  }
  for (const rule of RULES) {
    for (const id of rule.claims) {
      if (!kb.claims.has(id)) problems.push(`${rule.id}: unknown claim ${id}`);
      else if (!supported(id)) problems.push(`${rule.id}: supporting claim ${id} is not supported`);
    }
    for (const id of rule.trapClaims ?? []) {
      if (!kb.claims.has(id)) problems.push(`${rule.id}: unknown rejected claim ${id}`);
      else if (supported(id)) problems.push(`${rule.id}: rejected claim ${id} is supported`);
    }
  }
  return problems;
}

// ---------- architecture review rules ----------
// violated(model) === true means the rule fires. `pitfall` names the known error the rule guards against.
export const RULES = [
  { id: "AWS-001", provider: "aws", severity: "error", pitfall: "P-AWS-01", title: "App Runner em servico novo",
    violated: (m) => items(m.compute).some((c) => c.service === "app-runner"),
    detail: () => "App Runner esta fechado a novos clientes; use ECS Express Mode (migracao recomendada pela AWS).",
    claims: ["aws-apprunner-closed", "aws-ecs-express-recommended"] },
  { id: "AWS-002", provider: "aws", severity: "error", pitfall: "P-AWS-02", title: "CloudFront sem America do Sul para publico no Brasil",
    violated: (m) => m.cdn?.service === "cloudfront" && items(m.audience_regions).some((r) => ["BR", "SA"].includes(r))
      && ["PriceClass_100", "PriceClass_200"].includes(m.cdn.price_class),
    detail: (m) => `${m.cdn.price_class} nao inclui a America do Sul; use PriceClass_All.`,
    claims: ["aws-cf-priceclassall-sa", "aws-cf-priceclass100-no-sa"], trapClaims: ["aws-cf-priceclass200-sa-trap"] },
  { id: "AWS-003", provider: "aws", severity: "warning", pitfall: "P-AWS-03", title: "Endpoints de interface com custo fixo por AZ",
    violated: (m) => endpointAzCount(m) >= 10,
    detail: (m) => `${endpointAzCount(m)} endpoints x AZ cobram por hora (sa-east-1: US$ 0,021/h cada). Justifique cada um.`,
    claims: ["aws-vpce-hourly-per-az", "aws-vpce-data-processing"] },
  { id: "AWS-004", provider: "aws", severity: "error", pitfall: "P-AWS-05", title: "OpenSearch de producao sem 3 dedicated masters",
    violated: (m) => m.environment === "prod" && items(m.data).some((d) => d.service === "opensearch-managed" && d.dedicated_masters !== 3),
    detail: () => "A AWS recomenda tres dedicated masters em dominio de producao; numero par nao tem quorum tolerante a falha.",
    claims: ["aws-opensearch-3-masters"], trapClaims: ["aws-opensearch-2-masters-trap"] },
  { id: "AWS-005", provider: "aws", severity: "warning", pitfall: "P-AWS-04", title: "Endpoint de GPU sempre ligado para carga intermitente",
    violated: (m) => items(m.ml).some((x) => x.service === "sagemaker-realtime" && x.always_on === true && x.traffic === "intermittent"),
    detail: () => "Endpoint real-time sempre ligado cobra a hora de GPU sem trafego; avalie sagemaker-async com scale-to-zero, se a latencia permitir.",
    claims: ["aws-sagemaker-async-zero"] },
  { id: "AWS-006", provider: "aws", severity: "error", pitfall: "P-AWS-10", title: "CI com chaves estaticas",
    violated: (m) => m.identity?.ci_auth === "static-keys",
    detail: () => "Use OIDC do GitHub com trust policy que restrinja o claim sub.",
    claims: ["aws-oidc-no-static-keys", "aws-oidc-sub-required"] },
  { id: "AWS-007", provider: "aws", severity: "error", pitfall: "P-AWS-07", title: "Traces para o X-Ray com bearer",
    violated: (m) => m.observability?.traces_destination === "xray" && m.observability?.traces_auth === "bearer",
    detail: () => "Traces no endpoint OTLP do X-Ray nao aceitam bearer; configure SigV4 no coletor.",
    claims: ["aws-cwotlp-metrics-bearer"], trapClaims: ["aws-cwotlp-traces-bearer-trap"] },
  { id: "AWS-008", provider: "aws", severity: "error", pitfall: "P-AWS-06", title: "Endpoint externo de LLM contra a regra do projeto",
    violated: (m) => m.llm?.external_endpoint === true && m.constraints?.external_llm_allowed === false,
    detail: () => "O projeto proibe endpoint externo de LLM, embedding ou juiz em workloads governados.",
    claims: [] },
  { id: "AWS-009", provider: "aws", severity: "error", pitfall: null, title: "Banco de dados com acesso publico",
    violated: (m) => items(m.data).some((d) => d.public_access === true),
    detail: () => "Banco acessivel publicamente. Use sub-redes privadas e security group restrito.",
    claims: [] },
  { id: "AWS-010", provider: "aws", severity: "error", pitfall: null, title: "Dado pessoal ou sensivel sem KMS gerenciado pelo cliente",
    violated: (m) => SENSITIVE.has(m.data_classification) && items(m.data).some((d) => d.encryption !== "kms-cmk"),
    detail: () => "Dados pessoais ou sensiveis exigem chave KMS gerenciada pelo cliente.",
    claims: [] },
  { id: "AWS-011", provider: "aws", severity: "error", pitfall: null, title: "Aurora de producao sem Multi-AZ ou sem protecao contra exclusao",
    violated: (m) => m.environment === "prod" && items(m.data).some((d) => d.service === "aurora-postgresql"
      && (d.multi_az !== true || d.deletion_protection !== true)),
    detail: () => "Producao exige instancias em AZs distintas e protecao contra exclusao.",
    claims: [] },
  { id: "AWS-012", provider: "aws", severity: "error", pitfall: "P-AWS-08", title: "S3 Vectors para latencia abaixo de 100 ms",
    violated: (m) => items(m.data).some((d) => d.service === "s3-vectors" && (d.latency_ms_target ?? Infinity) < 100),
    detail: () => "S3 Vectors e recomendado quando latencia de cerca de 100 ms ou mais e aceitavel.",
    claims: ["aws-s3-vectors-ga"], trapClaims: ["aws-s3-vectors-latency-trap"] },
  { id: "AWS-013", provider: "aws", severity: "error", pitfall: "P-AWS-09", title: "Treino Spot sem checkpoint",
    violated: (m) => items(m.ml).some((x) => x.training_spot === true && x.checkpoints !== true),
    detail: () => "Managed Spot exige checkpoint para jobs longos.",
    claims: ["aws-sagemaker-spot-90"], trapClaims: ["aws-sagemaker-spot-no-checkpoint-trap"] },
  { id: "AWS-014", provider: "aws", severity: "warning", pitfall: null, title: "Retencao de logs nao definida",
    violated: (m) => m.observability !== undefined && (m.observability.log_retention_days ?? null) === null,
    detail: () => "Defina retencao de logs; logs sem retencao crescem sem limite.",
    claims: [] },
  { id: "AWS-015", provider: "aws", severity: "opportunity", pitfall: "P-AWS-11", title: "Fargate em x86 quando ARM64 e viavel",
    violated: (m) => items(m.compute).some((c) => ["ecs-express", "ecs-service-fargate"].includes(c.service) && c.arch === "x86_64"),
    detail: () => "Fargate ARM64 custa cerca de 20% menos por vCPU e GB em sa-east-1 (snapshot). Exige imagem multi-arquitetura testada.",
    claims: ["aws-fargate-arm64-setting"] },
  { id: "AWS-016", provider: "aws", severity: "error", pitfall: null, title: "Aplicativo desktop com telemetria",
    violated: (m) => m.project?.kind === "desktop-app" && m.observability?.telemetry !== undefined && m.observability.telemetry !== "none",
    detail: () => "O contrato de privacidade do aplicativo proibe telemetria; a nuvem nao pode coletar dados de uso.",
    claims: [] },
  { id: "AWS-017", provider: "aws", severity: "warning", pitfall: null, title: "Trilha de auditoria com Object Lock em modo governance",
    violated: (m) => items(m.data).some((d) => d.kind === "audit-archive" && d.immutability !== "compliance"),
    detail: () => "Governance pode ser contornada por quem tem s3:BypassGovernanceRetention; compliance nao pode ser removida por ninguem, inclusive root. A escolha e irreversivel no periodo: exige decisao registrada (ADR).",
    claims: [],
    sources: [{ url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html", note: "verificado por aws___search_documentation em 2026-11-14 (fora do dossie JEV)" }] },

  { id: "AZ-001", provider: "azure", severity: "error", pitfall: "P-AZ-01", title: "HA com redundancia de zona em Brazil South para servidor novo",
    violated: (m) => m.regions?.primary === "brazilsouth" && items(m.data).some((d) => d.service === "postgres-flexible" && d.ha === "zone-redundant"),
    detail: () => "HA com redundancia de zona para servidor novo esta temporariamente bloqueado em Brazil South; use HA na mesma zona ou valide a regiao.",
    claims: ["az-pg-brazilsouth-zr-blocked"] },
  { id: "AZ-002", provider: "azure", severity: "error", pitfall: "P-AZ-02", title: "Backup geo-redundante em Brazil South",
    violated: (m) => m.regions?.primary === "brazilsouth" && items(m.data).some((d) => d.backup_geo_redundant === true),
    detail: () => "A tabela oficial marca Brazil South sem backup geo-redundante.",
    claims: ["az-pg-backup-35"], trapClaims: ["az-pg-brazilsouth-geo-trap"] },
  { id: "AZ-003", provider: "azure", severity: "error", pitfall: "P-AZ-03", title: "Artifact Signing para publicador no Brasil",
    violated: (m) => m.signing?.windows_authenticode === "artifact-signing" && m.signing?.publisher_country === "BR",
    detail: () => "Validacao publica do Artifact Signing nao cobre indivíduos fora de EUA e Canada; o Brasil nao consta na lista de organizacoes verificada.",
    claims: ["az-signing-ga"], trapClaims: ["az-signing-brazil-individual-trap"] },
  { id: "AZ-004", provider: "azure", severity: "error", pitfall: "P-AZ-04", title: "Container Apps escalando a zero por CPU ou memoria",
    violated: (m) => items(m.compute).some((c) => c.service === "container-apps" && c.scale_to_zero === true && ["cpu", "memory"].includes(c.scale_metric)),
    detail: () => "Aplicacoes escaladas por CPU ou memoria nao escalam a zero; use escala por HTTP ou evento.",
    claims: ["az-aca-cpu-no-zero"], trapClaims: ["az-aca-cpu-zero-trap"] },
  { id: "AZ-005", provider: "azure", severity: "error", pitfall: "P-AZ-05", title: "Endpoint online do Azure ML assumido como escala a zero",
    violated: (m) => items(m.ml).some((x) => x.service === "azure-ml-online" && x.scale_to_zero === true),
    detail: () => "Escala a zero do endpoint online nao esta documentada no extrato oficial; compute e rede sao cobrados.",
    claims: ["az-aml-online-no-surcharge"], trapClaims: ["az-aml-online-scale-zero-absence"] },
  { id: "AZ-006", provider: "azure", severity: "error", pitfall: "P-AZ-06", title: "Politica WORM nao bloqueada na trilha de auditoria",
    violated: (m) => items(m.data).some((d) => d.kind === "audit-archive" && d.immutability !== "locked"),
    detail: () => "Politica nao bloqueada pode ser apagada; bloqueie a politica de retencao depois do teste.",
    claims: ["az-blob-worm"], trapClaims: ["az-blob-locked-no-delete-trap"] },
  { id: "AZ-007", provider: "azure", severity: "warning", pitfall: "P-AZ-07", title: "Custo de Log Analytics sem estimativa",
    violated: (m) => (m.observability?.log_analytics_gb_month ?? 0) > 10,
    detail: (m) => `${m.observability.log_analytics_gb_month} GB/mes em Analytics Logs custam cerca de US$ ${round2(m.observability.log_analytics_gb_month * 4.6)} so de ingestao (brazilsouth, snapshot).`,
    claims: [] },
  { id: "AZ-008", provider: "azure", severity: "error", pitfall: "P-AZ-12", title: "Banco de dados com acesso publico",
    violated: (m) => items(m.data).some((d) => d.public_access === true),
    detail: () => "Com integracao de VNet, o acesso publico deve ser negado.",
    claims: ["az-pg-vnet-no-public"] },
  { id: "AZ-009", provider: "azure", severity: "error", pitfall: "P-AZ-09", title: "LLM externo do Azure contra a regra do projeto",
    violated: (m) => m.llm?.external_endpoint === true && m.constraints?.external_llm_allowed === false,
    detail: () => "O projeto proibe endpoint externo de LLM, embedding ou juiz em workloads governados.",
    claims: [] },
  { id: "AZ-011", provider: "azure", severity: "error", pitfall: "P-AZ-10", title: "WORM por versao sem versionamento",
    violated: (m) => items(m.data).some((d) => d.kind === "audit-archive" && d.immutability_level === "version" && d.versioning !== true),
    detail: () => "Habilite o versionamento antes de criar politica WORM por versao.",
    claims: ["az-blob-version-worm-needs-versioning"] },
];

function endpointAzCount(model) {
  return (model.network?.interface_endpoints ?? 0) * (model.network?.availability_zones ?? 1);
}

export function reviewArchitecture(kb, model) {
  if (!PROVIDERS.has(model.provider)) throw new Error(`Unknown provider: ${model.provider}`);
  const findings = [];
  const passed = [];
  for (const rule of RULES.filter((item) => item.provider === model.provider)) {
    if (rule.violated(model)) {
      findings.push({
        rule_id: rule.id,
        severity: rule.severity,
        title: rule.title,
        pitfall: rule.pitfall,
        detail: rule.detail(model),
        claims: rule.claims.map((id) => claimView(kb, id)),
        rejected_claims: (rule.trapClaims ?? []).map((id) => claimView(kb, id)),
        sources: rule.sources ?? [],
      });
    } else {
      passed.push(rule.id);
    }
  }
  const errors = findings.filter((f) => f.severity === "error").length;
  const status = errors > 0 ? "fail" : findings.length > 0 ? "pass_with_findings" : "pass";
  return { provider: model.provider, project: model.project ?? null, environment: model.environment ?? null, status, errors, findings, passed_rules: passed };
}

// ---------- local API mapping ----------
export function mapLocalApi(api, provider) {
  if (!PROVIDERS.has(provider)) throw new Error(`Unknown provider: ${provider}`);
  if (!KINDS.has(api.kind)) throw new Error(`Unknown API kind (fail closed): ${api.kind}`);
  const states = items(api.state);
  for (const state of states) if (!STATES.has(state)) throw new Error(`Unknown state kind (fail closed): ${state}`);
  if (!CLASSES.has(api.data_classification)) throw new Error(`Unknown data classification: ${api.data_classification}`);
  return provider === "aws" ? mapAws(api, states) : mapAzure(api, states);
}

function constraintsFor(api, region) {
  const constraints = [
    api.external_llm_allowed === true
      ? { id: "external-llm", status: "ok", detail: "LLM externo permitido por politica." }
      : { id: "external-llm", status: "ok", detail: "Sem endpoint externo de LLM, embedding ou juiz: servicos gerenciados de LLM ficam fora do desenho." },
  ];
  if (SENSITIVE.has(api.data_classification)) {
    constraints.push({ id: "encryption-cmk", status: "ok", detail: "Chave gerenciada pelo cliente, rede privada e trilha de auditoria exigidas." });
  }
  if (api.egress === "none") {
    constraints.push({ id: "egress", status: "risk", detail: "Sem saida a internet: endpoints privados necessarios, cada um com custo por AZ." });
  }
  if (api.latency_p95_target_s !== undefined && api.latency_p95_target_s <= COLD_START_TOLERANCE_S) {
    constraints.push({ id: "latency-vs-scale-to-zero", status: "risk", detail: `p95 alvo de ${api.latency_p95_target_s} s nao tolera cold start de minutos: nao escalar a zero.` });
  }
  if (region === "brazilsouth") {
    constraints.push({ id: "region-brazilsouth", status: "risk", detail: "Backup geo-redundante indisponivel e HA zonal bloqueado para servidor novo na regiao (pagina oficial de 2026-11-14)." });
  }
  return constraints;
}

function mapAws(api, states) {
  const target = {};
  const rationale = [];
  const claims = new Set();
  const privateNetwork = api.egress === "none" || SENSITIVE.has(api.data_classification);
  switch (api.kind) {
    case "http-api":
      target.compute = "ecs-express";
      target.load_balancer = privateNetwork ? "internal-alb (sub-redes privadas)" : "internet-facing-alb com WAF";
      target.arch = "arm64 (imagem multi-arquitetura) com fallback x86_64";
      rationale.push("ECS Express Mode provisiona Fargate, ALB, HTTPS e auto scaling sem servidores; App Runner esta fechado a novos clientes.");
      ["aws-ecs-express-recommended", "aws-ecs-express-no-charge", "aws-fargate-arm64-setting"].forEach((c) => claims.add(c));
      if (api.streams === "sse") rationale.push("SSE: validar timeout do ALB e keepalive com carga antes de producao (nao verificado no dossie).");
      break;
    case "model-server": {
      const tolerantCold = api.latency_p95_target_s === undefined || api.latency_p95_target_s > COLD_START_TOLERANCE_S;
      if (api.traffic === "continuous") {
        target.ml = "sagemaker-realtime (sempre ligado: a hora de GPU e cobrada sem trafego)";
        rationale.push("Carga continua justifica endpoint sempre ligado; medir o custo antes.");
      } else if (tolerantCold) {
        target.ml = "sagemaker-async (scale-to-zero)";
        rationale.push("Carga intermitente ou em lote e latencia tolerante: async escala a zero quando nao ha requisicoes.");
        claims.add("aws-sagemaker-async-zero");
      } else {
        target.ml = "sagemaker-realtime com agenda (minimo 1 instancia nas janelas de uso)";
        rationale.push("Latencia p95 curta nao tolera cold start de minutos; escala a zero ficaria fora do alvo. Agendar capacidade pelas janelas de uso.");
        claims.add("aws-sagemaker-async-zero");
      }
      target.network = "VPC privada; contêiner de inferencia sem rota de internet";
      break;
    }
    case "worker-jobs":
      target.scheduler = "eventbridge-scheduler";
      target.compute = "lambda-container (tarefas curtas) ou sagemaker-training (janelas longas)";
      rationale.push("Agendamento persistido no EventBridge Scheduler; trabalho longo vai para SageMaker Training com Spot e checkpoint.");
      claims.add("aws-sagemaker-spot-90");
      break;
    case "otlp-receiver":
      target.telemetry = "cloudwatch-agent-otlp (metricas e logs) + ADOT com SigV4 (traces)";
      rationale.push("O agente CloudWatch recebe OTLP em 127.0.0.1:4318 por padrao; o sink local usa 14318, entao a porta precisa ser configurada.");
      claims.add("aws-cwotlp-metrics-bearer");
      break;
    case "desktop-app":
      target.distribution = "s3 privado (us-east-1) + cloudfront PriceClass_All";
      target.ci = "github-actions-oidc (sem chaves estaticas)";
      target.runtime = "nenhum: aplicativo local, sem rede";
      rationale.push("Nao ha backend a hospedar: a nuvem serve somente para distribuicao e CI.");
      ["aws-cf-priceclassall-sa", "aws-oidc-no-static-keys", "aws-oidc-sub-required"].forEach((c) => claims.add(c));
      break;
    case "mcp-stdio":
      target.runtime = "local (nao hospedar); expor por ferramenta governada";
      rationale.push("Servidor MCP por stdio roda na maquina do operador.");
      break;
    default:
      break;
  }
  for (const state of states) {
    switch (state) {
      case "postgres":
        target.data = api.environment === "prod"
          ? "aurora-postgresql (2 instancias Multi-AZ, protecao contra exclusao)"
          : "aurora-postgresql (Serverless v2, minimo 0 ACU em nao producao)";
        ["aws-aurora-sv2-zero-acu", "aws-aurora-sv2-min-half-disables-pause"].forEach((c) => claims.add(c));
        break;
      case "vector":
        if (api.latency_ms_target !== undefined && api.latency_ms_target < 100) {
          target.search = "opensearch-managed (BM25 + vetor, 3 dedicated masters em producao)";
          claims.add("aws-opensearch-3-masters");
        } else {
          target.vector = "s3-vectors (consulta pouco frequente, latencia de ~100 ms ou mais)";
          ["aws-s3-vectors-ga", "aws-s3-vectors-kms"].forEach((c) => claims.add(c));
        }
        break;
      case "object-audit":
        target.archive = "s3 com Object Lock em modo compliance + KMS + versionamento (verificar Object Lock antes de uso)";
        break;
      case "object":
        target.storage = "s3 privado + KMS";
        break;
      case "graph":
        target.data = "nao mapeado: backend de grafo nao verificado";
        break;
      case "jsonl":
        target.storage = "arquivo local (sink) substituido pelo agente de telemetria";
        break;
      default:
        break;
    }
  }
  return {
    api: api.id,
    provider: "aws",
    target,
    rationale,
    constraints: constraintsFor(api, api.region ?? "sa-east-1"),
    claims: [...claims].sort(),
    forbidden: api.external_llm_allowed === true ? [] : ["Amazon Bedrock", "Amazon Q", "endpoint externo de LLM, embedding ou juiz"],
  };
}

function mapAzure(api, states) {
  const target = {};
  const rationale = [];
  const claims = new Set();
  // The descriptor's region is the AWS region; the Azure region is its own field (default brazilsouth).
  const region = api.azure_region ?? "brazilsouth";
  const privateNetwork = api.egress === "none" || SENSITIVE.has(api.data_classification);
  switch (api.kind) {
    case "http-api":
      target.compute = "container-apps (consumo ou dedicado)";
      target.ingress = privateNetwork ? "internal (VNet)" : "external com WAF";
      target.scaling = "por HTTP ou evento; nao por CPU ou memoria se precisar escalar a zero";
      rationale.push("Container Apps escala a zero por HTTP e evento; CPU e memoria nao escalam a zero.");
      ["az-aca-scale-zero", "az-aca-cpu-no-zero", "az-aca-internal-ingress"].forEach((c) => claims.add(c));
      if (api.streams === "sse") rationale.push("SSE: validar timeout de ingresso e keepalive com carga antes de producao (nao verificado no dossie).");
      break;
    case "model-server":
      if (api.traffic === "continuous" || (api.latency_p95_target_s !== undefined && api.latency_p95_target_s <= COLD_START_TOLERANCE_S)) {
        target.ml = "azure-ml-online-endpoint (compute e rede cobrados mesmo ocioso)";
        claims.add("az-aml-online-no-surcharge");
      } else {
        target.ml = "azure-ml-batch-endpoint (escala a zero: verificar antes de usar)";
        rationale.push("Escala a zero de endpoint batch nao foi verificada nesta rodada.");
      }
      target.network = "rede gerenciada isolada, sem saida livre";
      break;
    case "worker-jobs":
      target.scheduler = "container-apps-jobs (agendado)";
      rationale.push("Container Apps Jobs roda sob demanda ou por agenda, na visao geral oficial (sem claim JEV dedicado).");
      break;
    case "otlp-receiver":
      target.telemetry = "azure-monitor-opentelemetry-distro-java + application insights";
      claims.add("az-monitor-java-distro");
      break;
    case "desktop-app":
      target.distribution = "blob estatico (verificar) + front door (verificar)";
      target.signing = "artifact-signing somente se o publicador for elegivel; Brasil nao consta na lista verificada";
      claims.add("az-signing-ga");
      rationale.push("Nao ha backend; a nuvem seria so distribuicao e assinatura.");
      break;
    case "mcp-stdio":
      target.runtime = "local (nao hospedar)";
      break;
    default:
      break;
  }
  for (const state of states) {
    switch (state) {
      case "postgres":
        target.data = "postgres-flexible (VNet, acesso publico negado)";
        target.ha = region === "brazilsouth"
          ? "mesma zona (HA com redundancia de zona bloqueado para servidor novo em brazilsouth)"
          : "redundancia de zona (verificar disponibilidade na regiao)";
        if (region === "brazilsouth") claims.add("az-pg-brazilsouth-zr-blocked");
        ["az-pg-vnet-no-public", "az-pg-backup-35"].forEach((c) => claims.add(c));
        break;
      case "vector":
        target.search = "ai-search-hybrid (BM25 + vetor com RRF)";
        claims.add("az-search-hybrid-rrf");
        break;
      case "object-audit":
        target.archive = "blob-immutable (retencao por tempo, bloqueada) + versionamento";
        ["az-blob-worm", "az-blob-no-capacity-charge", "az-blob-version-worm-needs-versioning"].forEach((c) => claims.add(c));
        break;
      case "object":
        target.storage = "blob privado";
        break;
      case "graph":
        target.data = "nao mapeado: backend de grafo nao verificado";
        break;
      default:
        break;
    }
  }
  return {
    api: api.id,
    provider: "azure",
    target,
    rationale,
    constraints: constraintsFor(api, region),
    claims: [...claims].sort(),
    forbidden: api.external_llm_allowed === true ? [] : ["Azure OpenAI", "modelos hospedados do Foundry com endpoint externo", "endpoint externo de LLM, embedding ou juiz"],
  };
}

// ---------- monthly cost from the tracked snapshot (fail closed) ----------
export function estimateMonthlyCost(prices, requestItems) {
  const lines = requestItems.map((item) => {
    const price = prices.skus[item.sku];
    if (!price) throw new Error(`Unknown SKU (fail closed, no guessed price): ${item.sku}`);
    if (typeof item.units_per_month !== "number" || item.units_per_month < 0) throw new Error(`Invalid units_per_month for ${item.sku}`);
    const factor = item.factor ?? 1;
    if (typeof factor !== "number" || factor < 0) throw new Error(`Invalid factor for ${item.sku}`);
    return {
      sku: item.sku,
      units_per_month: item.units_per_month,
      factor,
      unit_usd: price.usd,
      unit: price.unit,
      monthly_usd: round2(item.units_per_month * price.usd * factor),
      note: item.note ?? null,
      source_url: price.source_url,
    };
  });
  const total = lines.reduce((sum, line) => sum + line.monthly_usd, 0);
  return { currency: "USD", provider: prices.provider, prices_retrieved_at_utc: prices.retrieved_at_utc, total_usd: round2(total), lines };
}
