# iDentifyer

Updated: 2026-10-29. Entry point: `E:/Github/iDentifyer/README.md`.

- Projeto novo instalado em `E:/Github/iDentifyer`; núcleo Rust/Axum loopback 18741, SQLite para metadados manuais, câmera getUserMedia e COCO-SSD/TFJS locais. Fontes e executável Windows no destino; sem Node/Python/Rust no runtime do pacote.
- Verificado: release GNU/Rust1.99.1, 12 testes Rust, clippy/fmt; browser10+3 cenários com câmera sintética e inferência real; zero conexão remota no fluxo testado; npm zero advisories e OSV76 Rust deps zero retornados. Recibo e hashes: `docs/evidence/installation.json`, `change-manifest.json` do destino.
- Limites: webcam física/Linux/precisão do domínio seguem sem validação específica; imagem térmica/CSI/RF sem provedor/hardware calibrado. Parecer de produção continua NÃO. O erro Wi-Fi da entrega inicial foi resolvido pela revisão nativa descrita abaixo.
- Build-only: `.work/identifyer/toolchain` contém LLVM-MinGW portátil SHA verificado; GNU rustup adicionado sem mudar default; sem Visual Studio. Staging `.work/identifyer/project` permanece espelho documentado; scripts raiz verificam pacote novo sem sobrescrever destino.
- Aprendizado comprovado: TFJS4.22 espera headers de todos os shards antes de ler corpos; 17 shards4MB podem travar após seis conexões HTTP/1. `scripts/pack_model.py` concatena em ordem e preserva hashes upstream; modelo local passa a dois artefatos, inferência comprovada. Não alterar valores tensoriais.

## Revisão de sensores Windows
Updated: 2026-10-29. Entry point: `E:/Github/iDentifyer/src/wifi_windows.rs`.
- Fato verificado: MediaTek MT7925 Wi-Fi7 já habilitada/AdminUp; rádio hardware/software on, desconectada; Ethernet ativo. WLAN nativa substitui netsh e independe de idioma. Qualidade/RSSI só quando conectado e permitido, sem zeros fabricados.
- GPU NVIDIA fornece temperatura real via nvidia-smi System32,38°C na amostra instalada. ACPI sem suporte/LHM ausente; nenhum dispositivo IR/SDR reconhecido no inventário.
- Patch instalado com18 arquivos alterados/backup/banco preservado; manifesto final75 arquivos conferidos. Executável instalado reiniciado após autorização de encerrar teste em identifyer-posture; processo atual servido em http://127.0.0.1:18741. Evidências: docs/evidence/{sensor-upgrade,sensor-deployment,sensors-installed}.json no destino; teste UI real em .work/identifyer/sensors-ui.json.
- Verificado:14 testes Rust/check/clippy/fmt/release e bundle/sintaxeJS; UI real Wi-Fi/GPU disponível sem erro JS. Revisão: docs/SENSORS_REVIEW.md. Limite: driver WLAN bloqueado pode segurar Ctrl+C; prazo limita resposta e semáforo limita uma chamada nativa pendente.

## Postura observável
Updated: 2026-10-29. Entry point: `E:/Github/iDentifyer/web/src/posture.js`.
- MoveNet SinglePose Lightning TFJSv4 local, sem npm novo; geométricas de braços/tronco a score de ponto0.3. Gate exige uma pessoa COCO>=0.3 independente do limiar de exibição. Geometria não infere emoção, idade, personalidade, agressividade, ataque ou intenção/criminalidade. Demonstração de postura; vigilância está fora do uso pretendido do modelo.
- Sem persistência de pose. Carregar postura junto aos controles evita deslocamento de botão por resultados variáveis. Gate do harness proíbe POST/DELETE nesse fluxo.
- Instalação27 arquivos/backup e manifesto88 verificados. Revisão nativa WLAN/NVIDIA concorrente incorporada, binário/dados/processo preservados. Staging antigo .work/identifyer/project não contém esta atualização do frontend; comparar hashes antes de reaplicar.
- Evidência: docs/POSTURE.md, docs/evidence/{posture-browser,posture-multiple,posture-installation}.json no destino; .work/identifyer-posture/deployment.json confirma servidor instalado. Testes7 geometria+8 postura+2 múltiplos+13 regressões; câmera sintética/inferência real, sem avaliação de precisão de campo.

## Kit e plano de fusão externa
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/docs/HARDWARE_KIT.md.
- Operador aceitou sensores externos. Kit proposto Lepton3.5 radiométrico500-0771-01+PureThermal3,2xESP32-C6-DevKitC-1-N8,cabos/suporte/alvo dualband. Compra/firmware/adapters/captura física não executados.
- Arquitetura e gates em FUSION_PLAN.md; manifesto design-only fusion-hardware.json; revisão FUSION_REVIEW.md. CSI inicialmentescene-only; IR portrack depende calibração/tempo e observabilidade de validade espacial. Kit mínimo sem profundidade: ensaio controlado; volume exige método adicional validado.
- Instalados4 documentos e links/continuidade, sem alterar binário/modelos/postura/banco/processo;93 hashes conferidos. Próximo: hardware real e identificação de revisão/SDK; não alegar fusão já funcional.

## Sinais faciais visíveis
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/web/src/face-signals.js.
- tasks-vision1.2.0+FaceLandmarker float16/1 e WASM locais; somente sorriso aparente/boca aberta/olhos fechados. Barra de sorriso é menor coeficiente dos dois lados0–100, nunca probabilidade de felicidade ou emoção. Indeterminado em rosto pequeno/múltiplo/associação ambígua; no máximo4 caixas por quadro. Pontos faciais/corporais ocultos; postura continua funcionando.
- Mapa separado do payload save; nenhum sinal/landmark/vídeo persiste. Sem classificação de emoções/choro/frio/calor sentidos. Nova dependência motivada por ausência desses sinais em COCO/MoveNet; versões npm prévias preservadas.
- Instalação29 arquivos/manifesto110 conferidos, binário/dados/processo/sensores/fusão preservados.13 contratos+7 postura+10 checks browser instalado com câmera sintética e inferência real; audit sem advisories retornados. Fontes/limites: docs/FACE_SIGNALS.md, recibo docs/evidence/face-signals-installation.json, .work/identifyer-visible-signals/deployment.json.
- Stagings anteriores de posture/sensores não incluem esta atualização; reconciliar antes de reaplicar. Usar Ctrl+F5 e Carregar sinais faciais. Sem validação de webcam física/generalização/segurança.

## Visor Wi-Fi global
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/docs/WIFI_VIEW.md.
- Instalado overlay no vídeo com estado/conexão/%/RSSI e horário do /api/sensors real. Sem RF porpixel/objeto ou falso mapa; CSI segue plano futuro. Falha/stale/horário inválido retira números, stop oculta epagehide limpa timer.
- Ramo conectado foi observado em amostras reais85%/-47dBm e87%/-46dBm; esses valores variam. ContratosNode +postura +face13 e7 cenáriosbrowser instalado PASS; câmera sintética somente no teste, Wi-Fi real.
- Conflito com atualização facial bloqueado antes de escrita; patch refeito sobre instaladoatual. Binário/postura/face/deps/dados/processo preservados;116 hashes. Recibo docs/evidence/wifi-view-installation.json; backup .work/identifyer-wifi-view/backup.
