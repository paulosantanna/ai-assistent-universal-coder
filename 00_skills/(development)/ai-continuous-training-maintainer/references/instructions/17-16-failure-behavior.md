<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 16. Failure Behavior

- Se uma alteração individual falha nos testes → **reverter** a alteração, registrar em `memory/FAILURES.md`, tentar abordagem alternativa
- Se 3 tentativas consecutivas falharem → `BLOCKED` com relatório
- Se o baseline não puder ser estabelecido → `BLOCKED`
- Se subagente não responder ou exceder timeout → registrar e tentar nova dispatch ou continuar sem

---
