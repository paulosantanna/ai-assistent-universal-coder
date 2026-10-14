# Cofre externo e referências de runtime

Updated: 2026-10-13
Entry point: [local-secret-vault](../../../00_skills/(security)/local-secret-vault/SKILL.md).
Fonte: IMG_2774–IMG_2776. Nenhum cofre ou credencial foi lido nesta atualização.

O arquivo fica fora do workspace, fornecido por caminho/provedor autorizado. O caminho fotografado em LOCALAPPDATA é um exemplo, não prova de existência ou autorização deste usuário.
Registros por seção começam em linha @ROTULO e terminam no próximo marcador. Normalize CRLF e CR isolado para LF antes de interpretar, mantendo o rótulo completo (serviço/ambiente/região). Valide formato antes de qualquer preview.
OpenShift pode conter um comando oc login com token/server; ServiceNow pode conter um header Cookie. Interprete somente em processo autorizado, nunca por shell eval. Retorne metadados permitidos/mascarados ou uma referência opaca, não o texto bruto do bloco.
Credencial, token, cookie ou senha nunca entra em chat/prompt, logs, evidência, notebook, código ou argumentos de comando expostos. Passe segredo em processo ou pelo mecanismo seguro da ferramenta. Credencial exposta é comprometida. Rotação é um procedimento próprio, nunca inferida desta leitura.
401/403 exige distinguir expiração, escopo e método de autenticação com evidência; não atribua todo erro a expiração. Host/região/namespace são verificados no ambiente real. Exemplos de Dynatrace/JFrog nas fotos são observações de outro ambiente, não bindings disponíveis aqui.
O parser ler-cofre.js fotografado não foi fornecido e não é anunciado como instalado. Use a skill local e o provedor efetivamente disponível; falta de formato/acesso bloqueia autenticação. Leitura de arquivo por seções não o torna automaticamente um cookie jar Netscape.
