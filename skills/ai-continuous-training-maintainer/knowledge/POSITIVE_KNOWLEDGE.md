# POSITIVE_KNOWLEDGE.md — O Que Fazer

## Propósito

Práticas validadas que funcionam na manutenção do pipeline de treino contínuo.

## Práticas Recomendadas

### ✅ Avaliador independente (Quality-Judge)
Nunca deixar quem implementou avaliar o próprio trabalho. Quality-Judge é subagente separado, sem permissão de escrita.

### ✅ Recursão com limite
MAX_RECURSION = 3 previne loop infinito. Cada iteração foca apenas nos gaps da anterior.

### ✅ Rollback entre iterações
Antes de re-entrar em recursão, sempre restaurar snapshot. Iterações são independentes.

### ✅ Score com evidência obrigatória
Cada ponto do score deve ter evidência reproduzível. Score sem evidência = 0.

### ✅ Snapshot pré-alteração
Sempre calcular SHA-256 de cada arquivo antes de modificar. Armazenar em `memory/rollback/<execution_id>/`.

### ✅ Testes focados antes de teste completo
Após cada alteração individual, rodar apenas testes do módulo alterado. Só rodar bateria completa ao final.

### ✅ Uma CVE por vez
Para cada CVE identificada:
1. Verificar se a correção é compatível
2. Atualizar dependência
3. Rodar testes do módulo
4. Avançar

### ✅ SAST como pré-commit
Rodar bandit + ruff + mypy antes de cada alteração. Comparar com baseline.

### ✅ Uso de subagentes
Cada subagente tem escopo limitado e verificável. A coordenação central (esta skill) garante consistência.

### ✅ Documentar rollback
Toda alteração deve ter snapshot. Rollback deve restaurar estado original e verificar com SHA-256.

### ✅ Gradual é melhor que completo
Alterações grandes aumentam risco de regressão. Prefira 5 alterações pequenas e testadas a 1 grande.

## Validações

- pip-audit: pacotes Python
- bandit: SAST Python (OWASP Top 10)
- ruff: linter + formatter
- mypy: type safety
- pytest: functional tests
