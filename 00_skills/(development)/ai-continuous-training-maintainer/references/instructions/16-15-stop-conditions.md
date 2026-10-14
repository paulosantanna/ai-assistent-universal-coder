<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 15. Stop Conditions

Pare e retorne `BLOCKED` quando:
- Escopo precisa expandir para fora do autorizado
- Arquivos proibidos precisam ser modificados
- Alteração destrutiva sem aprovação
- Secrets expostos
- Testes revelam regressão bloqueante
- Dependência crítica ausente
- Evidência não pode ser produzida
- Assunções são invalidadas

Pare e retorne `WAITING_APPROVAL` quando:
- Operação destrutiva (deletar arquivos, branches, dados)
- Modificação de configuração de segurança
- Mudança de versão major de dependência crítica
- Rollback de alteração que afeta produção

Pare e retorne `MAX_RECURSION_REACHED` quando:
- `recursion_count >= MAX_RECURSION` e score ainda < 10.0
- Relatório final contém gaps restantes e scores de cada iteração

Pare e retorne `FAILED_VERIFICATION` quando:
- Quality-Judge encontra deterministic gate FAIL
- O mesmo gate falha em 2 iterações consecutivas (recursion não resolveu)

---
