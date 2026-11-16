"""Normalização de pronúncia PT-BR para narração documental.

Converte abreviaturas, iniciais, notação científica e números para a forma
que um locutor humano diria em português brasileiro, de modo que a síntese de
fala (Kokoro, Google Cloud TTS, Piper) reproduza uma narração fluida e natural.

Regras de negócio (não negociáveis):
- Apenas idioma pt-BR. Nunca produz nem permite texto em outro idioma.
- A normalização aplica-se ao que é FALADO (síntese) e às legendas, para que
  áudio e SRT fiquem sincronizados. Não altera fontes/claims (project.json/sources.json).
"""
from __future__ import annotations

import re

__all__ = ['normalize_for_speech', 'numero_por_extenso', 'normalize_numbers']

# ---------------------------------------------------------------------------
# Números por extenso (inteiros 0 a 999.999.999), português brasileiro
# ---------------------------------------------------------------------------

_UNIDADES = [
    'zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove',
]
_TEENS = [
    'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete',
    'dezoito', 'dezenove',
]
_DEZENAS = [
    'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta',
    'noventa',
]
_CENTOS = [
    '', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos',
    'setecentos', 'oitocentos', 'novecentos',
]


def _grupo_por_extenso(n: int) -> str:
    """Escreve um grupo de 0 a 999 por extenso, com conectores 'e' corretos."""
    if n == 0:
        return ''
    partes = []
    centena = n // 100
    resto = n % 100
    if centena == 1 and resto == 0:
        partes.append('cem')
    elif centena:
        partes.append(_CENTOS[centena])
    if resto:
        if centena:
            partes.append('e')
        if resto < 10:
            partes.append(_UNIDADES[resto])
        elif resto < 20:
            partes.append(_TEENS[resto - 10])
        else:
            dezena = resto // 10
            unidade = resto % 10
            partes.append(_DEZENAS[dezena - 2])
            if unidade:
                partes.append('e ' + _UNIDADES[unidade])
    return ' '.join(partes)


def numero_por_extenso(n: int) -> str:
    """Escreve um inteiro não-negativo por extenso em PT-BR (0 a 999.999.999).

    1000 -> mil; 2020 -> dois mil e vinte; 1836 -> mil oitocentos e trinta e seis.
    """
    if not 0 <= n <= 999_999_999:
        return str(n)
    if n == 0:
        return 'zero'
    partes = []
    milhao = n // 1_000_000
    resto_milhao = n % 1_000_000
    mil = resto_milhao // 1_000
    resto = resto_milhao % 1_000

    if milhao:
        grupo = _grupo_por_extenso(milhao) or 'um'
        partes.append(grupo + (' milhão' if milhao == 1 else ' milhões'))
    if mil:
        grupo = _grupo_por_extenso(mil) or 'um'
        partes.append('mil' if mil == 1 else grupo + ' mil')
    if resto:
        if partes:
            partes.append('e' if resto < 100 else '')
        grupo = _grupo_por_extenso(resto)
        if grupo:
            partes.append(grupo)
    return ' '.join(p for p in partes if p)


def _extenso_decimal(text: str) -> str:
    """Escreve um decimal PT-BR dígito a dígito (ex.: 1,602 -> um vírgula seis zero dois)."""
    texto = text.replace('.', ',')
    if ',' in texto:
        inteira, frac = texto.split(',', 1)
        return f'{numero_por_extenso(int(inteira))} vírgula ' + ' '.join(
            _UNIDADES[int(d)] for d in frac if d.isdigit()
        )
    return numero_por_extenso(int(texto))


# ---------------------------------------------------------------------------
# Regras de substituição (ordem importa: do mais específico para o geral)
# ---------------------------------------------------------------------------

# Iniciais com ponto lidas pelo nome da letra em PT-BR.
INICIAL = {
    'J': 'Jota',
    'G': 'Gê',
    'T': 'Tê',
}

_SUBSTITUICOES = [
    # Nomes abreviados com ponto: "Thomas J. J." -> "Thomas Jota Jota"
    (r'Thomas\s+J\.\s*J\.', 'Thomas Jota Jota', 0),
    (r'G\.\s*J\.\s+Stoney', 'Gê Jiota Stoney', 0),
    (r'J\.\s*J\.\s+Thomson', 'Jota Jota Thomson', 0),
    (r'J\.\s+Thomson', 'Jota Thomson', 0),
    (r'\bJ\.\b', 'Jota', 0),

    # Ano com ponto como separador de milhar: "2.020" -> "dois mil e vinte"
    # (antes da fração, para não comer "020/2020")
    (r'\b([1-9])\.(\d{3})\b',
     lambda m: _ano_ponto(m.group(1), m.group(2)), 0),

    # Frações simples "X/Y" (antes dos anos plain, para não comer o denominador):
    # "1/1836" -> "um sobre mil oitocentos e trinta e seis"
    (r'\b(\d+)\s*/\s*(\d+)\b',
     lambda m: f'{numero_por_extenso(int(m.group(1)))} sobre {numero_por_extenso(int(m.group(2)))}', 0),

    # Notação científica completa primeiro (senão o "10^-" solto consome sozinho):
    # "1,602 x 10^-19" / "2 x 10^-20" / "10^-19"
    (r'(\d[.,]\d+)\s*x\s*10\s*\^\s*-\s*(\d+)',
     lambda m: f'{_extenso_decimal(m.group(1))} vezes dez menos {numero_por_extenso(int(m.group(2)))}', 0),
    (r'(\d[.,]\d+)\s*vezes\s*10\s*menos\s*(\d+)',
     lambda m: f'{_extenso_decimal(m.group(1))} vezes dez menos {numero_por_extenso(int(m.group(2)))}', 0),
    (r'(\d+)\s*x\s*10\s*\^\s*-\s*(\d+)',
     lambda m: f'{numero_por_extenso(int(m.group(1)))} vezes dez menos {numero_por_extenso(int(m.group(2)))}', 0),
    (r'(\d[.,]\d+)\s*x\s*10\s*\^\s*(\d+)',
     lambda m: f'{_extenso_decimal(m.group(1))} vezes dez {numero_por_extenso(int(m.group(2)))}', 0),
    (r'10\s*\^\s*-\s*(\d+)',
     lambda m: f'dez menos {numero_por_extenso(int(m.group(1)))}', 0),

    # Bilhões com ponto/vírgula: "13.5bi" / "13,5 bilhões de anos luz"
    # -> "treze bilhões e meio de anos luz"
    (r'(\d+)[.,](\d)\s*bi(?:lhões?)?\s*(?:de\s*)?(anos\s*-?\s*luz)?',
     lambda m: _bilhoes_fracao(m.group(1), m.group(2), bool(m.group(3))), 0),
    (r'(\d+)\s*bilhões?\s*(?:de\s*)?(anos\s*-?\s*luz)?',
     lambda m: f'{numero_por_extenso(int(m.group(1)))} bilhões{" de anos luz" if m.group(2) else ""}', 0),

    # Ano com ponto como separador de milhar: "2.020" -> "dois mil e vinte"
    (r'\b([1-9])\.(\d{3})\b',
     lambda m: _ano_ponto(m.group(1), m.group(2)), 0),

    # Anos de 4 dígitos (1000-2099): "2020" -> "dois mil e vinte", "1897" -> ...
    (r'\b(1\d{3}|20\d{2})\b', lambda m: numero_por_extenso(int(m.group(0))), 0),

    # g-2 (momento magnético anômalo) -> "g menos dois"
    (r'\bg\s*-\s*2\b', 'g menos dois', 0),
    # Siglas lidas letra por letra (conservativo)
    (r'\bEDM\b', 'É E DÊ EM', 0),
    (r'\bACME\b', 'A CÊ M É', 0),
]


def _ano_ponto(milhar: str, resto: str) -> str:
    n = int(milhar + resto)
    if 1000 <= n <= 2099:
        return numero_por_extenso(n)
    return milhar + '.' + resto


def _bilhoes_fracao(inteira: str, frac: str, anos_luz: bool) -> str:
    inteiro = int(inteira)
    sufixo = ' de anos luz' if anos_luz else ''
    if frac == '5':
        return f'{numero_por_extenso(inteiro)} bilhões e meio{sufixo}'
    return f'{numero_por_extenso(inteiro)} vírgula {_UNIDADES[frac]} bilhões{sufixo}'


def _aplica_substituicoes(texto: str) -> str:
    resultado = texto
    for padrao, repl, _flags in _SUBSTITUICOES:
        resultado = re.sub(padrao, repl, resultado)
    return resultado


def normalize_for_speech(texto: str, language: str = 'pt-BR') -> str:
    """Normaliza `texto` para a forma falada naturalmente em PT-BR.

    Nunca altera o idioma: exige pt-BR e devolve sempre PT-BR.
    """
    if not isinstance(texto, str):
        return texto
    if language != 'pt-BR':
        raise ValueError('ptbr_pronunciation_only_ptbr: language deve ser pt-BR')
    return _aplica_substituicoes(texto)


def normalize_numbers(texto: str) -> str:
    """Alias explícito para normalização de números PT-BR (sem alterar idioma)."""
    return normalize_for_speech(texto, language='pt-BR')


if __name__ == '__main__':  # pragma: no cover - demonstração rápida de linha de comando
    exemplos = [
        '2.020/2020',
        'Em 1897, J. J. Thomson anunciou o descobrimento dos elétrons.',
        '13.5bilhões de anos luz',
        '13.5bi anos-luz',
        '1,602 x 10^-19 coulombs',
        '2 x 10^-20 metros',
        '1/1836 da massa do próton',
        'Thomas J. J.',
        'G. J. Stoney',
        'g-2 do elétron',
        'EDM e ACME',
        'Entre 1909 e 1910',
    ]
    for ex in exemplos:
        print(f'{ex!r} -> {normalize_for_speech(ex)!r}')
