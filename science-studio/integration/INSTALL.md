# Dark-videos — instalação local

Updated: 2026-10-27. Entry point: [installer](install.py).

O pacote instala a página `/science-studio` no menu Pipeline e o router autenticado `/api/science-studio`. Reutiliza require_operator, sessão/CSRF e proxy same-origin existentes. Jobs longos executam em processo Python separado e não na requisição HTTP. A configuração é local do servidor; a API nunca aceita argv, paths ou provedores enviados pelo navegador. Cada produção tem UUID e lock exclusivo.

O instalador só altera o router, uma entrada de navegação e adiciona três arquivos novos (router, configuração e página). Faz backup e recusa sobrescrever conteúdo inesperado. Mantém runtime compartilhado no workspace; mover esse workspace requer atualizar home na configuração. Não copia credenciais, não altera banco/filas/publicador e não reinicia serviços.

```powershell
python science-studio/integration/install.py --target D:/Git/dark-videos --stage .work/science-studio/dark-install
```

Inspecione manifest/diff no stage e execute verificações antes de instalar. `--apply` grava fora do workspace e requer permissão de filesystem do ambiente:

```powershell
python science-studio/integration/install.py --target D:/Git/dark-videos --stage .work/science-studio/dark-install --apply
```

Se já houver configuração instalada, preserves config. Configure `config` no backend/app/api/science_studio.json com caminho absoluto do JSON criado por `studio.py configure`; null mantém geração automática bloqueada. Diretório projects fica em workspace/.work/science-studio/projects, separado da publicação. Reiniciar/recarregar API e frontend é etapa operacional explícita; instalação no disco não prova ativação.

Se processo morrer durante job, o lock permanece e bloqueia reenvio ambíguo. Verificar worker e eventual fila ComfyUI antes de remover manualmente `.job.lock` do projeto. Aprovação expirada exige novo render/revisão. Para desfazer, restaurar somente os arquivos desse pacote pelos backups no manifest, verificando que não houve edição posterior; não usar reset amplo.

Geradores/pesos locais e qualidade de voz/arte não são instalados nem validados por este pacote. Endpoints são incluídos no mesmo app e não publicam conteúdo automaticamente.
