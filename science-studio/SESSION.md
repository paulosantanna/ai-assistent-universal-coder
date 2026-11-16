# Sessão dedicada — Science Studio AI v0.2

Updated: 2026-10-27. Entry point: [playbook](PLAYBOOK.md).

Abra uma nova sessão neste workspace e cole:

```text
Use science-studio-expert e science-studio/PLAYBOOK.md como fluxo desta sessão.
Esta sessão é dedicada à produção de vídeos científicos Motion Comic.
Sou o operador e fornecerei temas. Prepare pesquisa com fontes verificadas,
roteiro, storyboard, arte HQ/cartoon em camadas, animação/parallax, efeitos
científicos ilustrativos, voz masculina documental profunda em PT-BR,
legendas discretas e MP4 local. Sem balões de fala.
Padrão: short de 60 segundos, 9:16. Quando eu pedir: youtube=10 minutos,
documentary=60 minutos, full-documentary=90 minutos, em 16:9.
Execute automaticamente as etapas locais disponíveis até preview revisável.
Não invente provedores, fontes nem resultados. Informe pré-requisitos ausentes.
Use o mesmo project.json e CLI que a integração Dark-videos.
Peça minha revisão do resultado antes de registrar aprovação; publicação
só ocorre mediante pedido explícito posterior e gates reais do publicador.
Primeiro tema: [meu tema].
```

É uma especialização de sessão do codenavi-agent, sem criar nova identidade. A sessão usa as skills canônicas e carrega módulos somente quando necessários. Novas skills podem exigir reabrir a sessão para aparecerem na lista automática; os caminhos canônicos funcionam diretamente.

Pela CLI, `init` recebe tema/perfil. Com motores locais e corpus configurados, `generate` prepara o preview. Sem esses pré-requisitos, a sessão pode pesquisar e produzir projeto/roteiro/ativos com ferramentas disponíveis, mas não deve afirmar que a máquina gera tudo offline automaticamente. Serviços em localhost são locais; pesquisa atual pela internet continua online, salvo corpus previamente verificado.
