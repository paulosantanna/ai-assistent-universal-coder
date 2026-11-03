"""Rule-based grapheme-to-phone front end for broadcast pt-BR and General American.

This is an original letter-to-sound layer, not a vendored pronouncing dictionary.
Callers that need a specific pronunciation should pass an explicit phone string.
"""
import re
import unicodedata

from phones import PHONES

TOKEN = re.compile(r"[A-Za-zÀ-ÿ]+|\d+|[?.!,;:]+")
PT_MARK = set("áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ")

EN_WORDS = {
    "a": ["ax"], "an": ["ax", "n"], "the": ["dh", "ax"], "this": ["dh", "i", "s"],
    "that": ["dh", "a", "t"], "they": ["dh", "e", "j"], "them": ["dh", "E", "m"],
    "there": ["dh", "E", "r"], "then": ["dh", "E", "n"], "i": ["a", "j"],
    "hello": ["h", "E", "l", "o"], "hi": ["h", "a", "j"], "hey": ["h", "e", "j"],
    "is": ["i", "z"], "are": ["a", "r"], "am": ["a", "m"], "was": ["w", "ax", "z"],
    "you": ["j", "u"], "your": ["j", "O", "r"], "we": ["w", "i"], "my": ["m", "a", "j"],
    "of": ["ax", "v"], "to": ["t", "u"], "for": ["f", "O", "r"], "and": ["a", "n", "d"],
    "in": ["i", "n"], "on": ["O", "n"], "with": ["w", "i", "th"], "from": ["f", "tap", "ax", "m"],
    "voice": ["v", "O", "j", "s"], "synthetic": ["s", "i", "n", "th", "E", "t", "i", "k"],
    "speech": ["s", "p", "i", "tsh"], "audio": ["O", "d", "i", "o"],
    "hello,": ["h", "E", "l", "o"],
    "zero": ["z", "i", "r", "o"], "one": ["w", "ax", "n"], "two": ["t", "u"],
    "three": ["th", "r", "i"], "four": ["f", "O", "r"], "five": ["f", "a", "j", "v"],
    "six": ["s", "i", "k", "s"], "seven": ["s", "E", "v", "ax", "n"],
    "eight": ["e", "j", "t"], "nine": ["n", "a", "j", "n"],
}

PT_DIGITS = {
    "0": ["z", "E", "tap", "u"], "1": ["u~"], "2": ["d", "o", "j", "s"],
    "3": ["t", "tap", "e", "s"], "4": ["k", "w", "a", "t", "tap", "u"],
    "5": ["s", "i~", "k", "u"], "6": ["s", "e", "j", "s"], "7": ["s", "E", "tsh", "i"],
    "8": ["o", "j", "t", "u"], "9": ["n", "O", "v", "i"],
}
EN_DIGITS = {
    "0": EN_WORDS["zero"], "1": EN_WORDS["one"], "2": EN_WORDS["two"],
    "3": EN_WORDS["three"], "4": EN_WORDS["four"], "5": EN_WORDS["five"],
    "6": EN_WORDS["six"], "7": EN_WORDS["seven"], "8": EN_WORDS["eight"],
    "9": EN_WORDS["nine"],
}

PUNCT = {
    ",": [("sil", False)],
    ";": [("sil", False)],
    ":": [("sil", False)],
    ".": [("sil", False), ("sil", False)],
    "!": [("sil", False), ("sil", False)],
    "?": [("sil", False), ("sil", False)],
}


def looks_portuguese(text):
    return any(char in PT_MARK for char in text)


def parse_phone_string(value):
    phones = []
    for token in value.replace(",", " ").split():
        if token not in PHONES:
            raise ValueError("unknown phone: " + token)
        phones.append((token, token in ("a", "e", "E", "i", "o", "O", "u", "a~", "e~", "o~")))
    if not phones:
        raise ValueError("empty phone string")
    return phones


def text_to_phones(text, language, affricate_ti=True):
    question = text.strip().endswith("?")
    tokens = TOKEN.findall(text)
    phones = []
    for token in tokens:
        if token in PUNCT or (token and token[0] in ".!?,;:"):
            phones.extend(PUNCT.get(token[0], [("sil", False)]))
            continue
        if token.isdigit():
            table = PT_DIGITS if language == "pt-BR" else EN_DIGITS
            for digit in token:
                phones.extend((phone, False) for phone in table[digit])
            continue
        if language == "pt-BR":
            phones.extend(portuguese_word(token, affricate_ti=affricate_ti))
        else:
            phones.extend(english_word(token))
    if not any(phone != "sil" for phone, _stress in phones):
        raise ValueError("no speakable phones")
    return {"phones": phones, "question": question, "language": language}


def portuguese_word(word, affricate_ti=True):
    raw = word.lower()
    pieces = []
    stress_at = None
    index = 0
    while index < len(raw):
        pair = raw[index:index + 2]
        if pair in ("ão", "õe"):
            pieces.append(("a~" if pair == "ão" else "o~", True))
            pieces.append(("w" if pair == "ão" else "j", False))
            stress_at = len(pieces) - 2
            index += 2
            continue
        if pair in ("ãe", "ãi"):
            pieces.append(("a~", True))
            pieces.append(("j", False))
            stress_at = len(pieces) - 2
            index += 2
            continue
        if pair in ("nh", "lh", "ch", "rr", "ss"):
            pieces.append(({"nh": "nh", "lh": "lh", "ch": "sh", "rr": "h", "ss": "s"}[pair], False))
            index += 2
            continue
        if pair in ("qu", "gu") and index + 2 < len(raw) and raw[index + 2] in ("e", "i", "é", "í"):
            pieces.append(("k" if pair == "qu" else "g", False))
            index += 2
            continue
        if pair in ("qu", "gu") and index + 2 < len(raw) and raw[index + 2] in ("a", "á", "o", "ó", "u", "ú"):
            pieces.append(("k" if pair == "qu" else "g", False))
            pieces.append(("w", False))
            index += 2
            continue
        char = raw[index]
        if char in "áàâéêíóôú":
            phone = {"á": "a", "à": "a", "â": "a", "é": "E", "ê": "e", "í": "i", "ó": "O", "ô": "o", "ú": "u"}[char]
            pieces.append((phone, True))
            stress_at = len(pieces) - 1
            index += 1
            continue
        if char in "ãõ":
            pieces.append(("a~" if char == "ã" else "o~", True))
            stress_at = len(pieces) - 1
            index += 1
            continue
        if char in "aeiou":
            nxt = raw[index + 1] if index + 1 < len(raw) else ""
            if char + nxt in ("ai", "ei", "oi", "ui", "au", "eu", "ou", "iu"):
                diph = "j" if nxt == "i" else "w"
                pieces.append((_pt_oral(char), False))
                pieces.append((diph, False))
                index += 2
                continue
            nasal = False
            if nxt in ("m", "n"):
                after = raw[index + 2] if index + 2 < len(raw) else ""
                if not _vowel_letter(after):
                    nasal = True
            phone = _pt_oral(char)
            if nasal:
                phone = {"a": "a~", "e": "e~", "i": "i~", "o": "o~", "u": "u~"}.get(phone, phone)
                pieces.append((phone, False))
                index += 2
                continue
            pieces.append((phone, False))
            index += 1
            continue
        mapped = _pt_consonant(raw, index)
        if mapped is None:
            index += 1
            continue
        phone, consumed = mapped
        pieces.append((phone, False))
        index += consumed
    if not pieces:
        return []
    vowel_positions = [pos for pos, (phone, _marked) in enumerate(pieces) if _is_vowel(phone)]
    if stress_at is None and vowel_positions:
        if _penultimate(raw) and len(vowel_positions) >= 2:
            stress_at = vowel_positions[-2]
        else:
            stress_at = vowel_positions[-1]
    elif stress_at is not None and not _is_vowel(pieces[stress_at][0]) and vowel_positions:
        stress_at = vowel_positions[-1]
    reduced = []
    for pos, (phone, _marked) in enumerate(pieces):
        stress = pos == stress_at
        if not stress and pos == len(pieces) - 1 and phone == "e":
            phone = "i"
        elif not stress and pos == len(pieces) - 1 and phone == "o":
            phone = "u"
        if affricate_ti and phone in ("t", "d"):
            nxt = pieces[pos + 1][0] if pos + 1 < len(pieces) else ""
            if nxt == "i" or (not stress and pos + 1 == len(pieces) - 1 and pieces[pos + 1][0] in ("e", "i")):
                phone = "tsh" if phone == "t" else "dzh"
        reduced.append((phone, stress if _is_vowel(phone) else False))
    # Re-apply affrication after final-e reduction.
    if affricate_ti:
        fixed = []
        for pos, (phone, stress) in enumerate(reduced):
            nxt = reduced[pos + 1][0] if pos + 1 < len(reduced) else ""
            if phone in ("t", "d") and nxt == "i":
                phone = "tsh" if phone == "t" else "dzh"
            fixed.append((phone, stress))
        reduced = fixed
    return [(phone, stress) for phone, stress in reduced if phone in PHONES]


def _pt_oral(char):
    return {"a": "a", "e": "e", "i": "i", "o": "o", "u": "u"}[char]


def _vowel_letter(char):
    return len(char) == 1 and char in "aeiouáàâãéêíóôõú"


def _is_vowel(phone):
    return phone in {"a", "e", "E", "i", "o", "O", "u", "ax", "a~", "e~", "i~", "o~", "u~"}


def _penultimate(word):
    plain = "".join(char for char in unicodedata.normalize("NFD", word) if unicodedata.category(char) != "Mn")
    return plain.endswith(("a", "e", "o", "as", "es", "os", "am", "em"))


def _pt_consonant(word, index):
    char = word[index]
    nxt = word[index + 1] if index + 1 < len(word) else ""
    prev = word[index - 1] if index else ""
    if char == "ç":
        return "s", 1
    if char == "c":
        return ("s" if nxt in ("e", "i", "é", "í") else "k"), 1
    if char == "g":
        return ("zh" if nxt in ("e", "i", "é", "í") else "g"), 1
    if char == "r":
        if index == 0 or not _vowel_letter(prev):
            return "h", 1
        return "tap", 1
    if char == "s":
        if _vowel_letter(prev) and _vowel_letter(nxt):
            return "z", 1
        return "s", 1
    if char == "x":
        if index == 0:
            return "sh", 1
        if _vowel_letter(prev) and _vowel_letter(nxt):
            if word.startswith("ex") and index == 1:
                return "z", 1
            return "sh", 1
        return "s", 1
    if char == "l":
        if nxt in ("",) or (nxt != "h" and not _vowel_letter(nxt)):
            return "w", 1
        return "l", 1
    if char in "pbtdfvkmnz":
        return char, 1
    if char == "j":
        return "zh", 1
    if char == "h":
        return None
    if char in "w":
        return "w", 1
    if char == "y":
        return "j", 1
    return None


def english_word(word):
    key = word.lower()
    if key in EN_WORDS:
        phones = EN_WORDS[key]
        vowels = [pos for pos, phone in enumerate(phones) if _is_vowel(phone)]
        stress = vowels[-2] if len(vowels) >= 2 else (vowels[-1] if vowels else None)
        return [(phone, pos == stress) for pos, phone in enumerate(phones)]
    raw = key
    if raw.endswith("e") and len(raw) > 3 and raw[-2] not in "aeiou":
        raw = raw[:-1]
    pieces = []
    index = 0
    while index < len(raw):
        chunk = raw[index:index + 4]
        if chunk == "tion":
            pieces.extend(["sh", "ax", "n"])
            index += 4
            continue
        pair = raw[index:index + 2]
        if pair == "sh":
            pieces.append("sh"); index += 2; continue
        if pair == "ch":
            pieces.append("tsh"); index += 2; continue
        if pair == "th":
            pieces.append("th"); index += 2; continue
        if pair == "ph":
            pieces.append("f"); index += 2; continue
        if pair == "ee":
            pieces.append("i"); index += 2; continue
        if pair == "oo":
            pieces.append("u"); index += 2; continue
        if pair == "ea":
            pieces.append("i"); index += 2; continue
        if pair in ("ay", "ai"):
            pieces.extend(["e", "j"]); index += 2; continue
        if pair in ("ow", "ou"):
            pieces.extend(["a", "w"]); index += 2; continue
        if pair == "ng":
            pieces.append("n"); index += 2; continue
        char = raw[index]
        nxt = raw[index + 1] if index + 1 < len(raw) else ""
        if char == "c":
            pieces.append("s" if nxt in ("e", "i") else "k")
        elif char == "g":
            pieces.append("zh" if nxt in ("e", "i") else "g")
        elif char == "r":
            pieces.append("r")
        elif char == "a":
            pieces.append("a")
        elif char == "e":
            pieces.append("E")
        elif char == "i":
            pieces.append("i")
        elif char == "o":
            pieces.append("o")
        elif char == "u":
            pieces.append("ax")
        elif char == "y":
            pieces.append("i" if index else "j")
        elif char in PHONES:
            pieces.append(char)
        index += 1
    vowels = [pos for pos, phone in enumerate(pieces) if _is_vowel(phone)]
    stress = vowels[0] if vowels else None
    return [(phone, pos == stress) for pos, phone in enumerate(pieces) if phone in PHONES]
