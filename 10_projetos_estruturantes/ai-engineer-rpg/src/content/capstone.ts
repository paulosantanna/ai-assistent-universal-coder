import type { Capstone } from '../engine/types'

/**
 * Capstone do certificado: 8 competências no peso JEV fixado no plano
 * (arquitetura 0.16 / criar do zero 0.14 / treino 0.12 / manutenção 0.10 /
 * melhoria 0.14 / performance 0.14 / energia 0.10 / predição-estatística 0.10).
 * Cada rubrica tem 5 níveis Score 0..4; a dissertação é obrigatória.
 */
export const capstone: Capstone = {
  dissertation: {
    prompt:
      'Dissertação de arquitetura: descreva (mínimo 400 caracteres) o sistema de IA que você entregou na trilha. Cobre: objetivo e segmento, dados e base legal, arquitetura (monolítica ou híbrida), treino e avaliação, serviço e observabilidade, risco, energia e próximo passo de melhoria com evidência.',
    minChars: 400,
  },
  tasks: [
    {
      id: 'cap-arq',
      competency: 'Arquitetura de IA (monolítica ou híbrida)',
      weight: 0.16,
      prompt: 'Desenhe e defenda a arquitetura do seu sistema: componentes, fronteiras, porque monolítico ou híbrido, e o que muda se a escala dobrar.',
      options: [
        { text: 'Sem desenho: componentes e fronteiras não declarados.', score: 0 },
        { text: 'Lista de componentes solta, sem fronteiras nem justificativa do modelo arquitetural.', score: 1 },
        { text: 'Arquitetura descrita com componentes e fronteiras; justificativa monolítico/híbrido rasa.', score: 2 },
        { text: 'Arquitetura com fronteiras, justificativa de opção e trade-offs de custo/latência apresentados.', score: 3 },
        { text: 'Arquitetura defendida com fronteiras, caminhos de dado, trade-offs, evolução escalando 10x e plano de reversão.', score: 4 },
      ],
    },
    {
      id: 'cap-zero',
      competency: 'Criar de do zero',
      weight: 0.14,
      prompt: 'Evidencie a criação do zero: dataset, ingestão, representação (features/embeddings) e o primeiro exercício funcional até o serviço mínimo.',
      options: [
        { text: 'Não há evidência de criação do zero.', score: 0 },
        { text: 'Só fragmentos: notebook isolado sem pipeline conectável.', score: 1 },
        { text: 'Caminho do dado ao serviço existe, mas sem versionamento das receitas.', score: 2 },
        { text: 'Caminho reproduzível: dados, receitas versionadas, injeção de dependências do lado do modelo.', score: 3 },
        { text: 'Criação reproduzível ponta a ponta, com testes de contrato no serviço e treinamento seguido em um comando.', score: 4 },
      ],
    },
    {
      id: 'cap-treino',
      competency: 'Treinar o modelo',
      weight: 0.12,
      prompt: 'Explique o treino: split, função de perda, otimizador, hiperparâmetros, computo gasto e como o treino é repetível.',
      options: [
        { text: 'Sem treino real: modelo pronto foi importado sem registro.', score: 0 },
        { text: 'Treino executado sem split claro nem registro de hiperparâmetros.', score: 1 },
        { text: 'Split e hiperparâmetros anotados; reprodutibilidade parcial (sem seed/config versionada).', score: 2 },
        { text: 'Treino com split correto, hiperparâmetros e seed versionados; perda e curvas reportadas.', score: 3 },
        { text: 'Treino repetível em um comando (config + seed + registro), com comparação de baselines e desvio entre rodadas.', score: 4 },
      ],
    },
    {
      id: 'cap-manutencao',
      competency: 'Manutenção do sistema',
      weight: 0.1,
      prompt: 'Mostre a operação contínua: monitoramento, resposta a incidente, atualização de dados e de versões sem parar o produto.',
      options: [
        { text: 'Sem plano de manutenção declarado.', score: 0 },
        { text: 'Checagens manuais informais, sem alerta nem trilha.', score: 1 },
        { text: 'Monitoramento básico de disponibilidade sem resposta documentada.', score: 2 },
        { text: 'Monitoramento com alerta, runbook de incidente e política de atualização de dados/modelo.', score: 3 },
        { text: 'Operação com alerta, runbook testado, janelas de atualização blindadas e post-mortem de incidente real ou simulado.', score: 4 },
      ],
    },
    {
      id: 'cap-melhoria',
      competency: 'Melhoria contínua com evidência',
      weight: 0.14,
      prompt: 'Demonstre um ciclo de melhoria: hipótese, experimento controlado, leitura estatística e decisão documentada.',
      options: [
        { text: 'Nenhuma melhoria demonstrada com método.', score: 0 },
        { text: 'Mudanças por intuição, sem métrica antes e depois.', score: 1 },
        { text: 'Comparação antes/depois em uma métrica, sem controle na confiança.', score: 2 },
        { text: 'Experimento com métrica primária e comparação honesta (mesmo golden set).', score: 3 },
        { text: 'Ciclo completo: hipótese registrada, amostra dimensionada, leitura estatística e decisão documentada com reversão.', score: 4 },
      ],
    },
    {
      id: 'cap-perf',
      competency: 'Performance (latência, custo e serving)',
      weight: 0.14,
      prompt: 'Reporte performance: perfil por etapa, otimização aplicada e ganho medidamente confirmado por benchmark.',
      options: [
        { text: 'Sem perfil de performance.', score: 0 },
        { text: 'Latência média isolada, sem cauda nem etapa.', score: 1 },
        { text: 'Perfil por etapa com p50/p99; otimização sem benchmark de regressão.', score: 2 },
        { text: 'Perfil + otimização (cache/lote/compressão) com benchmark antes/depois.', score: 3 },
        { text: 'Perfil, otimização e benchmark por release com budget de latência e custo; regressão bloqueada no CI.', score: 4 },
      ],
    },
    {
      id: 'cap-energia',
      competency: 'Eficiência energética',
      weight: 0.1,
      prompt: 'Orce energia: consumo por treino/inferência, decisões de right-sizing e trade-off acurácia por joule.',
      options: [
        { text: 'Energia não mencionada.', score: 0 },
        { text: 'Menção genérica de sustentabilidade, sem número.', score: 1 },
        { text: 'Estimativa de energia do treino apenas, sem decisão derivada.', score: 2 },
        { text: 'Energia por treino e por inferência estimada com método; right-sizing discutido.', score: 3 },
        { text: 'Orçamento de energia com método (fator de grid, utilização) e trade-off acurácia por joule explícito na decisão final.', score: 4 },
      ],
    },
    {
      id: 'cap-estatis',
      competency: 'Predição, estatística e acurácia',
      weight: 0.1,
      prompt: 'Defenda as métricas: escolha de acurácia/precisão/recall compatível com a assimetria de custo e calibração candidata.',
      options: [
        { text: 'Sem métrica declarada.', score: 0 },
        { text: 'Acurácia isolada em problema assimétrico.', score: 1 },
        { text: 'Métricas coerentes com o problema; sem calibração nem incerteza.', score: 2 },
        { text: 'Métricas + threshold justificado pela assimetria + checagem de calibração.', score: 3 },
        { text: 'Fim-a-fim: métricas, threshold, calibração medida (Brier) e intervalo de confiança das métricas reportados.', score: 4 },
      ],
    },
  ],
}
