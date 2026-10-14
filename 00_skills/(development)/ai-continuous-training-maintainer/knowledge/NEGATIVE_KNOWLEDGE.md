# NEGATIVE_KNOWLEDGE.md — O Que Não Fazer

## Propósito

Registro de falhas, anti-patterns e práticas que devem ser evitadas na manutenção do treino contínuo.

## Anti-Patterns

### ❌ Deixar implementador avaliar a própria qualidade
**Problema**: Viés de confirmação. Quem implementa sempre acha que está bom.
**Alternativa**: Quality-Judge independente, sem permissão de escrita.

### ❌ Recursão sem limite
**Problema**: Loop infinito se score nunca chega a 10.0.
**Alternativa**: MAX_RECURSION = 3. Após 3, reportar MAX_RECURSION_REACHED.

### ❌ Score inferido sem evidência
**Problema**: "Confiança" substitui facts.
**Alternativa**: Cada critério do score exige comando + output como evidência.

### ❌ Modificar código na mesma iteração após avaliação
**Problema**: Ciclo eval → implement → eval sem rollback corrompe o baseline.
**Alternativa**: Rollback completo antes de re-entrar em Phase 2.

### ❌ Atualizar múltiplas dependências simultaneamente
**Problema**: Quebra de compatibilidade impossível de rastrear.
**Alternativa**: Uma dependência por vez, testando cada alteração.

### ❌ Ignorar SAST findings "porque é só treino"
**Problema**: Código de treino executa em produção. Injection via dados de treino pode comprometer o modelo.
**Alternativa**: Tratar código de treino com mesmo nível de segurança que código de produção.

### ❌ Remover funcionalidade sem verificar dependentes
**Problema**: Módulos podem depender de funções removidas.
**Alternativa**: grep por imports antes de qualquer remoção.

### ❌ Commit direto em main/master
**Problema**: Sem chance de revisão ou rollback parcial.
**Alternativa**: Sempre usar branch, mesmo para "correções rápidas".

### ❌ Confiar em única fonte de CVE
**Problema**: PyPA não cobre todas as vulnerabilidades (ex: GHSA sem CVE).
**Alternativa**: Múltiplas fontes: pip-audit, trivy, NVD, OSV.dev, GitHub Advisory.

## Falhas Registradas

<!-- Adicionado automaticamente a cada execução -->
| Data | Falha | Causa | Correção |
|------|-------|-------|----------|
