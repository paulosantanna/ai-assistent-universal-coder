<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included
- `E:/GitHub/aidiabetic-research/src/main.py` — entrypoint do treino contínuo
- `E:/GitHub/aidiabetic-research/src/continual/` — todo o ecossistema de treino contínuo
- `E:/GitHub/aidiabetic-research/pyproject.toml` — dependências do projeto
- `E:/GitHub/aidiabetic-research/requirements*.txt` — requirements
- `E:/GitHub/aidiabetic-research/Dockerfile` — se impactar o treino
- `E:/GitHub/aidiabetic-research/docker-compose.yml` — se impactar o treino

### Excluded
- Qualquer arquivo fora dos caminhos acima
- `data/`, `models/`, `checkpoints/` — dados e artefatos
- `secrets/`, `.env` — credenciais
- `frontend/`, `ui/` — frontend
- `api/`, `server/` — API e servidores
- `infra/` — infraestrutura não relacionada a treino
- `tests/` fora de `src/continual/` (a menos que impactado pela mudança)

---
