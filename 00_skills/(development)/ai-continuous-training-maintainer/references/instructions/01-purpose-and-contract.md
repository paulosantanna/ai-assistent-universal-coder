<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# AI Continuous Training Maintainer

> **Skill MCP-connected para manter o treino contínuo de IA sempre atualizado com melhores práticas, arquiteturas, CVEs, SAST e bibliotecas seguras.**
>
> Atualiza gradualmente `E:/GitHub/aidiabetic-research/src/main.py` e o ecossistema de treino contínuo sem gerar regressões.

---

```yaml
skill:
  name: AI Continuous Training Maintainer
  slug: ai-continuous-training-maintainer
  version: 2.0.0
  description: >
    Mantém o pipeline de treino contínuo de IA atualizado com melhores práticas,
    CVEs de múltiplas fontes, SAST/Trivy, libs atualizadas, SOLID, OWASP,
    OWASP AI, sem gerar novos bugs. Usa subagentes especializados e persiste
    conhecimento. Inclui avaliador recursivo independente (Quality-Judge) que
    exige score 10.0/10 em rubric determinístico para aprovação final.
    Se score < 10.0, reentra em ciclo de melhoria até MAX_RECURSION.
  category: HYBRID
  architecture_level: 3
  risk_level: HIGH
  max_recursion: 3
  activation:
    - "update continuous training"
    - "atualizar treino contínuo"
    - "maintain ai training pipeline"
    - "check cvEs on training code"
    - "audit training security"
    - "update libraries training"
    - "aplicar melhores práticas treino IA"
    - "continuous training health check"
    - "verificar CVEs no continuous training"
    - "trivy scan training"
    - "sast training analysis"
    - "manter main.py atualizado"
    - "atualizar continuous_daemon"
    - "gradual training improvement"
    - "rollback training change"
  exclusions:
    - alterações fora do diretório src/continual/ ou src/main.py
    - deploy em produção sem aprovação humana
    - modificação de credenciais ou secrets
    - alteração de arquitetura sem handoff ao ROOT
    - mudanças em domínios não relacionados a treino contínuo
    - operações destrutivas sem aprovação explícita
  inputs:
    - comando do usuário (intenção de atualização, auditoria ou rollback)
    - opcional: escopo específico (ex: "só CVEs", "só libs", "só main.py")
    - opcional: max_recursion (default: 3)
  outputs:
    - relatório de análise pré-alteração (baseline)
    - diff das alterações realizadas
    - relatório de CVEs encontradas e resolvidas
    - relatório SAST/Trivy pré e pós
    - snapshot de rollback (estado anterior)
    - score final (0.0-10.0) com rubric detalhado
    - log de recursão (cada iteração: o que mudou, score parcial)
    - candidatos a conhecimento (do/don't, lessons learned)
    - status: COMPLETED | REWORK_REQUIRED | BLOCKED | WAITING_APPROVAL | MAX_RECURSION_REACHED
  tools:
    - filesystem-readonly
    - filesystem-write-sandbox
    - git-readonly
    - git-controlled
    - test-runner-controlled
    - package-local
  memory: true
  human_approval: conditional
  maintainer: AEOS / Aidabetic Research
```

---
