# AEOS AIDiabetic Urgent Improvement Pack — FINAL v1.0.0

Pacote completo de orquestração, skills, agentes, políticas, schemas, comandos,
quality gates e evidências para executar o plano de melhorias do
`AIDiabetic Research` com o AEOS.

## Objetivo

Converter um plano textual de melhorias em uma execução governada, paralelizável,
auditável e reversível. O pacote não assume que alegações do plano original são
verdadeiras. Cada alegação deve ser confirmada no repositório alvo antes de gerar
mudanças.

## Repositórios esperados

- AEOS: `E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1`
- Projeto alvo: `E:\GitHub\aidiabetic-research`

Os dois repositórios permanecem separados. Este pack é instalado como overlay
no AEOS e executado contra o projeto alvo.

## Conteúdo

- 19 skills AEOS Level 3, cada uma com contrato, agente, conhecimento, memória,
  schema, template, teste estrutural e validador;
- 18 definições de agentes especializados;
- um playbook completo, sem dependência de execução manual fragmentada;
- políticas de execução, segurança clínica, tokens, evidências e rollback;
- schemas JSON para evidência, finding, handoff e gate;
- scripts de instalação em overlay, validação e geração de manifest;
- comandos PowerShell para instalar, validar e acionar o playbook;
- prompt de fallback para runtimes AEOS cuja sintaxe de CLI seja diferente;
- testes do pack e relatório de validação.

## Regra central

Nenhuma alegação vira fato sem evidência do repositório. Nenhuma mudança é
concluída sem testes, diff, rollback e gate correspondente. Falhas determinísticas
não podem ser anuladas por julgamento de LLM.

## Correções aplicadas ao plano original

1. **Fluxos não confirmados**: “pagamento” não é considerado fluxo crítico até
   ser encontrado no código, documentação ou telemetria.
2. **E2E não é line coverage**: o pacote mede cobertura ponderada de jornadas,
   contratos e riscos, além de cobertura de código quando disponível.
3. **Health externo não é liveness**: indisponibilidade de PubMed/OpenAlex não
   deve reiniciar o processo. O estado deve ser readiness/degraded, com timeout,
   circuit breaker e última observação conhecida.
4. **Cache clínico é opt-in**: respostas clínicas personalizadas, dados de
   paciente e resultados de alto risco não entram em cache sem política explícita.
5. **Configuração não vira apenas `.env`**: runtime settings, políticas,
   parâmetros científicos e secrets têm proprietários e fontes distintas.
6. **Modularização não é big bang**: usa mapa de dependências, contratos,
   strangler migration, ADR e checkpoints.
7. **Dashboard clínico sem PHI**: métricas operacionais clínicas devem ser
   agregadas, minimizadas e não podem registrar conteúdo sensível.
8. **Release não implica deploy**: o pack automatiza versionamento e release PR,
   mas não habilita auto-merge ou auto-deploy.
9. **Cronograma vencido removido**: execução é organizada por waves e
   dependências, com reestimativa após baseline verificável.

## Instalação segura

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
py -3 <CAMINHO_DO_PACK>\scripts\install_overlay.py `
  --aeos-root "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  --target-root "E:\GitHub\aidiabetic-research"
```

Por padrão, o instalador cria um overlay e não altera registries centrais.

## Validação

```powershell
py -3 <CAMINHO_DO_PACK>\scripts\validate_package.py
py -3 -m pytest <CAMINHO_DO_PACK>\tests -ra
```

## Execução

```powershell
& <CAMINHO_DO_PACK>\commands\RUN_FULL.ps1 `
  -AeosRoot "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  -TargetRoot "E:\GitHub\aidiabetic-research" `
  -Mode "controlled"
```

`RUN_FULL.ps1` tenta a sintaxe padrão do AEOS e, caso a CLI instalada use outro
contrato, imprime o comando equivalente e aponta para `FULL_EXECUTION_PROMPT.md`.

## Critério final

O pack só retorna `PASS` quando:

- todos os gates críticos passam;
- não há regressão conhecida;
- evidências obrigatórias existem e possuem hash;
- o score ponderado é pelo menos 9.8;
- nenhuma restrição clínica, de segurança ou de privacidade está aberta;
- rollback foi demonstrado para mudanças destrutivas ou estruturais.

Caso contrário, o resultado é `REWORK_REQUIRED` ou `BLOCKED`, nunca um score
fabricado.
