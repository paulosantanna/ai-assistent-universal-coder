# Plano Staff III para Tornar o AEOS Pronto para Producao

## Resumo

Direcao escolhida: **hardening incremental com rigor enterprise**. A decisao tecnica e manter a arquitetura AEOS atual, porque a auditoria mostrou que os componentes centrais existem; o risco real esta na cadeia de execucao: testes quebrados, CI teatral, readiness fraco, Judge bloqueado, registries derivados ausentes e rota de merge incompatível com a governanca.

Perguntas norteadoras que devem acompanhar cada fase:

- **Estou caminhando pelo caminho correto?** Sim, se a proxima mudanca reduz incerteza verificavel e melhora a capacidade de bloquear erro real.
- **Esse e o jeito certo de fazer?** So se o gate final depender de execucao real, nao de presenca de arquivos, mocks ou confianca.
- **Nao seria melhor outra direcao?** Rebuild completo nao e justificado agora: ha arquitetura suficiente para recuperar. A direcao correta e endurecer o sistema existente ate ele falhar fechado.
- **Estou consertando causa raiz ou sintoma?** A causa raiz e a ausencia de uma cadeia confiavel de evidencia. Corrigir so um teste ou so um workflow nao basta.
- **Um Staff Engineer aprovaria isso para producao?** Apenas quando quick/full suite, CI, Judge, readiness, evidence manifests, seguranca e aprovacao humana estiverem verdes com evidencia reproduzivel.

## Mudancas Principais

- Estabilizar execucao local antes de qualquer gate de release:
  - Corrigir a estrategia de temporarios do `verify.py` para Windows e CI.
  - Usar diretorios unicos, limpos e controlados para `pytest`, preferencialmente via `--basetemp`.
  - Fazer a quick suite deixar de falhar com `PermissionError`.
  - Padronizar launcher Python para nao depender de `python` no PATH; usar resolvedor portatil ja existente ou wrapper consistente.

- Substituir CI aparente por CI real:
  - Trocar todos os `run: echo ...` do workflow enterprise por comandos verificaveis.
  - Executar registry validate, structural guard, quick suite, testes de politicas/permissoes, evidence verify, package verify, Judge e readiness.
  - Fazer o workflow falhar fechado quando qualquer gate obrigatorio falhar.
  - Publicar artefatos redigidos de teste, readiness, Judge e evidencia.

- Fechar rota insegura de merge:
  - Remover `merge-pr` e `create-and-merge` do workflow de bot ou protege-los por ambiente de release com aprovacao humana.
  - Exigir status checks verdes, Judge `PASS`, readiness `PASS`, branch protection e auditoria antes de qualquer merge.
  - Alinhar workflow real com `block_merge_always`, `no_auto_merge` e aprovacao explicita.

- Endurecer readiness e Judge:
  - Alterar readiness para nao pontuar categorias criticas por mera presenca de arquivos.
  - `tests`, `package_supply_chain`, `runbooks`, `production_safety`, `security`, `observability` e `evidence_integrity` devem depender de artefatos executados.
  - Resolver o Judge `BLOCKED` por `permission_denied`.
  - Exigir runtime result real e manifestos staged/final validos.

- Consolidar registries derivados:
  - Criar ou recuperar comando deterministico para gerar `.aeos/derived/registries`.
  - Validar schemas, duplicidades, referencias quebradas e overlay.
  - Decidir uma politica unica: derivados versionados ou gerados em CI; recomendacao: gerar em CI e verificar hash deterministico.

## Sequencia de Implementacao

1. **Registrar o plano**
   - Criar `SOLUCAO.md` com este conteudo.
   - Manter `MEMORY.md` como evidencia da auditoria e `SOLUCAO.md` como plano de execucao.

2. **Corrigir base de execucao**
   - Corrigir temporarios e permissoes.
   - Ajustar scripts NPM para entrada Python portatil.
   - Validar `py -3 aeos\scripts\verify.py --suite quick`.
   - Criterio de saida: quick suite sem erros.

3. **Tornar CI confiavel**
   - Substituir steps `echo` por comandos reais.
   - Garantir cache apenas para dependencias, nao para esconder falhas.
   - Publicar relatorios como artifacts.
   - Criterio de saida: CI falha quando um gate real falha.

4. **Remover bypass de governanca**
   - Bloquear merge automatizado sem Judge/readiness.
   - Reduzir permissoes do token do bot.
   - Adicionar protecao operacional documentada.
   - Criterio de saida: nenhum merge ocorre sem evidencia e aprovacao.

5. **Reforcar readiness**
   - Readiness deve ler resultados reais, nao contar arquivos.
   - Categorias criticas com evidencia ausente devem ser `BLOCKED`.
   - Adicionar recomendacoes automaticas quando blockers forem detectados.
   - Criterio de saida: readiness `PASS` somente quando a cadeia inteira passar.

6. **Resolver cadeia Judge/runtime/evidence**
   - Corrigir causa do `permission_denied`.
   - Gerar runtime result real.
   - Verificar manifestos finais e imutabilidade.
   - Criterio de saida: Judge `PASS`, runtime `PASS`, manifests validos.

7. **Fechar producao**
   - Executar full suite.
   - Rodar secret scan, dependency/security audit, package verify e evidence verify.
   - Atualizar README/runbooks com comandos reais.
   - Criterio de saida: readiness `PASS >= 0.95`, CI real verde, sem blocker critico aberto.

## Plano de Testes

- Local obrigatorio:
  - `py -3 aeos\scripts\verify.py --suite quick`
  - `py -3 aeos\scripts\verify.py --suite full`
  - `py -3 aeos\scripts\run_readiness_audit.py`
  - Judge latest ou comando equivalente do repositorio para produzir `judge-result.json`.
  - Evidence verify para manifestos staged e final.
  - Package verify para release candidate.

- CI obrigatorio:
  - PR deve executar os mesmos gates locais criticos.
  - Push em branch protegida deve bloquear se qualquer gate falhar.
  - Workflow de merge deve ser impossivel sem checks verdes e aprovacao humana.

- Cenarios negativos:
  - Temporario inacessivel deve produzir erro claro e nao mascarar teste.
  - Manifesto adulterado deve bloquear Judge/readiness.
  - Registry derivado ausente deve bloquear readiness.
  - Workflow com merge automatico deve ser detectado como blocker.
  - Categoria sem evidencia real nao pode receber score `1.0000`.

## Assuncoes e Defaults

- Manter a arquitetura atual do AEOS; nao fazer rebuild do core.
- Barra final: rigor enterprise.
- Nao declarar producao com qualquer blocker critico aberto.
- Nao aceitar adapter de contrato como substituto de toolchain real quando o componente afetado exigir compilacao/teste real.
- `SOLUCAO.md` foi criado na raiz fora do Plan Mode.
- `MEMORY.md` permanece como registro de auditoria; nao deve ser tratado como conhecimento institucional promovido sem revisao independente.
