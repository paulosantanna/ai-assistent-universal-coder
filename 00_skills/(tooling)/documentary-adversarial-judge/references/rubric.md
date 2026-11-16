# Rubrica e limiar — como o juiz pontua

Updated: 2026-10-31. Módulo de [`documentary-adversarial-judge`](../SKILL.md).

Seis dimensões, peso igual, nota 0–10 cada. **Limiar do operador: ≥ 9,5**. Cada dimensão precisa
atingir o limiar e a média também. Uma dimensão isolada abaixo de 9,5 reprova o pacote inteiro.

## Ancoragem das notas

A nota não é impressão. Cada nível tem condição verificável:

- **0–3** — defeito grave e evidente: ausente, falso, quebrado, ou violando regra inviolável.
- **4–6** — existe mas falha em requisito declarado: audível porém abafa, bonito porém fora do tema.
- **7–8,9** — funciona e é competente, mas há defeito real identificável (repetição localizada,
  trecho curto de silêncio, amostra de voz irregular, claim fraca).
- **9,0–9,4** — bom com um desvio menor que o operador notaria.
- **9,5–10** — requisito cumprido com evidência; nenhum defeito identificável pelos métodos de
  amostragem; o desvio remanescente é indeterminável, não tolerado.

Arredondar para cima para atingir 9,5 é fraude de critério. Se a evidência permite 9,4, a nota é 9,4.

## Dimensões

### `musica`
Calma presente e audível durante o vídeo; nunca abafa o narrador; ducking operante sob a voz; não é
drone disfarçado de música; cobre a duração; licença real por faixa do ledger.
Reprova: trilha ausente, inaudível, agitada, abafando a voz, ou com licença não comprovada.

### `voz`
PT-BR correto na pronúncia, naturalidade documental, ritmo constante, sem artefato de síntese,
timbre consistente entre cenas distantes, sem aceleração global que soe artificial.
Reprova: pronúncia errada, robótica, inconsistência de timbre, numeração/abreviação mal falada.

### `fluencia`
Narração preenche a cena; zero trecho mudo; silêncios apenas respiratórios e curtos; legenda
coerente com o que é falado; transições encadeando sem corte abrupto de raciocínio.
Reprova: cena subnarrada, silêncio prolongado, mudez parcial, legenda divergente.

### `enredo`
Rigor do domínio: sem erro factual, sem simplificação que engana, sem hipótese vendida como
resultado; arco com capítulos que abrem, desenvolvem e fecham; uma cena = um fenômeno; sem
repetição e sem fragmento; `claim` sempre lastreada em `sources.json`.
Reprova: erro factual, certeza falsa, capítulo sem fechamento, claim sem fonte.

### `visual_tematico`
Cada quadro amostrado mostra o fenômeno da sua cena; orientação e proporção corretas; zero marca
d'água, logo, selo, URL sobreposta, texto falso gerado por IA, gameplay/filme/série; zero
espelhamento ou rotação para disfarçar reuso.
Reprova: asset fora do tema, marca d'água presente, reuso disfarçado.

### `direitos`
Ledger completo para assets e música; licença individual conferida; atribuições exigidas presentes
nos créditos; nada de terceiros sem licença.
Reprova: licença presumida, item sem ledger, atribuição devida e ausente.

## Cálculo e veredito

```
media = (musica + voz + fluencia + enredo + visual_tematico + direitos) / 6
APROVADO   se media >= 9.5 E min(dimensoes) >= 9.5
REPROVADO  caso contrário
INCONCLUSAO se a evidência de alguma dimensão estiver ausente ou inválida
```

`INCONCLUSAO` nunca é aprovação. Evidência ausente exige produzir a evidência antes do veredito.

## Saída do veredito

Para cada dimensão: nota, evidência citada (comando + artefato), e o defeito concreto se houver.
No fim: veredito, média, e a lista priorizada de causas raiz com a etapa de produção que cada uma
exige refazer. Causa raiz sem etapa acionável não serve para o reinício.
