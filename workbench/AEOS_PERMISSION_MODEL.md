# AEOS Permission Model — v1.0.0

## 1. Propósito

Define o modelo de permissões que controla o que cada agente pode fazer, com quais recursos e sob quais condições.

## 2. Níveis de Acesso

| Nível | Nome | Descrição | Exige Aprovação |
|-------|------|-----------|-----------------|
| 0 | NONE | Sem acesso | N/A |
| 1 | READ | Leitura apenas | Não |
| 2 | READ_WRITE | Leitura e escrita | Não |
| 3 | EXECUTE | Execução de comandos | Sim (ações destrutivas) |
| 4 | ADMIN | Administração do sistema | Sim (sempre) |
| 5 | ROOT | Acesso irrestrito | Sim + justificativa |

## 3. Matriz de Permissões

### Filesystem
| Ação | Nível Requerido | Aprovação |
|------|-----------------|-----------|
| Listar diretório | READ | Não |
| Ler arquivo | READ | Não |
| Escrever arquivo | READ_WRITE | Não |
| Editar arquivo | READ_WRITE | Não |
| Deletar arquivo | EXECUTE | Humana |
| Mover arquivo | READ_WRITE | Não |
| Copiar arquivo | READ | Não |

### Shell
| Ação | Nível Requerido | Aprovação |
|------|-----------------|-----------|
| Comando read-only | READ | Não |
| Comando com efeito colateral | EXECUTE | Não |
| Comando destrutivo | EXECUTE | Humana |
| Script não verificado | ADMIN | Humana |

### Git
| Ação | Nível Requerido | Aprovação |
|------|-----------------|-----------|
| status/log/diff | READ | Não |
| add/commit | READ_WRITE | Não |
| push | READ_WRITE | Não |
| reset --hard | EXECUTE | Humana |
| delete branch | EXECUTE | Humana |
| force push | ADMIN | Humana |

### Rede
| Ação | Nível Requerido | Aprovação |
|------|-----------------|-----------|
| Web fetch (documentado) | READ | Não |
| Web fetch (não verificado) | EXECUTE | Humana |
| API call (configurada) | READ_WRITE | Não |
| Network scan | ADMIN | Humana |

## 4. Delegação

Agentes podem delegar tarefas apenas a subagentes com nível igual ou inferior de permissão. Um agente READ não pode delegar a um agente EXECUTE.

## 5. Escalação

Quando um agente requer acesso a um nível que não possui:
1. Solicita ao Root Agent.
2. Root Agent avalia justificativa.
3. Se aprovado, permissão temporária é concedida.
4. Permissão expira após a tarefa.
5. Tudo é registrado em auditoria.

## 6. Bloqueio

O Permission Model BLOQUEIA qualquer ação que:
- Não tenha nível mínimo requerido.
- Exija aprovação e não tenha obtido.
- Venha de agente não registrado.
- Tente escalar privilégio sem justificativa.
- Tente acessar recurso fora do escopo do agente.
