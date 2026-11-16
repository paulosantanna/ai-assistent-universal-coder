"""Read the creator and version strings stored in a Windows executable."""

from __future__ import annotations

import struct


def _pad(data: bytes) -> bytes:
    return data + b"\0" * ((4 - (len(data) % 4)) % 4)


def _utf16(text: str) -> bytes:
    return (text + "\0").encode("utf-16-le")


def _block(key: str, value: bytes, value_length: int, kind: int, children: bytes = b"") -> bytes:
    raw = struct.pack("<HHH", 0, value_length, kind) + _utf16(key)
    raw = _pad(raw)
    if value:
        raw += value
        raw = _pad(raw)
    raw += children
    raw = _pad(raw)
    return struct.pack("<H", len(raw)) + raw[2:]


def version_resource(strings: dict[str, str]) -> bytes:
    children = b"".join(
        _block(key, _utf16(value), len(value) + 1, 1) for key, value in strings.items()
    )
    table = _block("040904B0", b"", 0, 1, children)
    info = _block("StringFileInfo", b"", 0, 1, table)
    fixed = struct.pack(
        "<IIIIIIIIIIIII",
        0xFEEF04BD,
        0x00010000,
        0x00010000,
        0x00000000,
        0x00010000,
        0x00000000,
        0,
        0,
        0x00040004,
        1,
        0,
        0,
        0,
    )
    return _block("VS_VERSION_INFO", fixed, len(fixed), 0, info)


def build_pe(timestamp: int, strings: dict[str, str] | None) -> bytes:
    """Minimal PE32 used to prove the reader. File alignment is 0x200."""
    resource = b""
    if strings is not None:
        blob = version_resource(strings)
        resource = bytearray(88 + len(blob))
        for index, (entry_id, child, is_dir) in enumerate(((16, 24, True), (1, 48, True), (0x0409, 72, False))):
            at = (0, 24, 48)[index]
            struct.pack_into("<IIHHHH", resource, at, 0, 0, 0, 0, 0, 1)
            struct.pack_into("<II", resource, at + 16, entry_id, child | (0x80000000 if is_dir else 0))
        struct.pack_into("<IIII", resource, 72, 0x1000 + 88, len(blob), 0, 0)
        resource[88:] = blob
    raw_size = ((len(resource) + 0x1FF) // 0x200) * 0x200 if resource else 0
    optional = bytearray(224)
    struct.pack_into("<H", optional, 0, 0x10B)
    struct.pack_into("<I", optional, 28, 0x00400000)
    struct.pack_into("<II", optional, 32, 0x1000, 0x200)
    struct.pack_into("<I", optional, 56, 0x2000)
    struct.pack_into("<I", optional, 60, 0x200)
    struct.pack_into("<H", optional, 66, 3)
    struct.pack_into("<I", optional, 92, 16)
    if resource:
        struct.pack_into("<II", optional, 96 + 16, 0x1000, len(resource))
    section = bytearray(40)
    if resource:
        section[0:8] = b".rsrc\0\0\0"
        struct.pack_into("<IIII", section, 8, len(resource), 0x1000, raw_size, 0x200)
    pe = bytearray(0x200 + raw_size)
    pe[0:2] = b"MZ"
    struct.pack_into("<I", pe, 0x3C, 0x80)
    pe[0x80:0x84] = b"PE\0\0"
    # Machine, sections, timestamp, symbols, optional size, characteristics.
    struct.pack_into("<HHIIIHH", pe, 0x84, 0x14C, 1 if resource else 0, timestamp, 0, 0, len(optional), 0x0102)
    pe[0x98:0x98 + len(optional)] = optional
    if resource:
        pe[0x98 + len(optional):0x98 + len(optional) + 40] = section
        pe[0x200:0x200 + len(resource)] = resource
    return bytes(pe)


def _rva_to_offset(sections, rva: int) -> int:
    for virtual, raw, raw_size, virtual_size in sections:
        span = max(raw_size, virtual_size)
        if virtual <= rva < virtual + span:
            return raw + (rva - virtual)
    raise ValueError("rva fora das secoes")


def parse_pe(data: bytes) -> dict:
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("nao e um executavel PE")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if e_lfanew + 24 > len(data) or data[e_lfanew:e_lfanew + 4] != b"PE\0\0":
        raise ValueError("assinatura PE ausente")
    coff = e_lfanew + 4
    _machine, sections_count, timestamp, _sym, _nsym, optional_size, _flags = struct.unpack_from("<HHIIIHH", data, coff)
    optional = coff + 20
    if optional + optional_size > len(data):
        raise ValueError("cabecalho opcional truncado")
    magic = struct.unpack_from("<H", data, optional)[0]
    number_at = optional + (92 if magic == 0x10B else 108 if magic == 0x20B else -1)
    if number_at < 0:
        raise ValueError("magic PE desconhecido")
    directories = struct.unpack_from("<I", data, number_at)[0]
    resource_rva = resource_size = 0
    if directories > 2:
        resource_rva, resource_size = struct.unpack_from("<II", data, number_at + 4 + 16)
    section_table = optional + optional_size
    sections = []
    for index in range(sections_count):
        at = section_table + index * 40
        _name, virtual_size, virtual, raw_size, raw = struct.unpack_from("<8sIIII", data, at)
        sections.append((virtual, raw, raw_size, virtual_size))
    strings = {}
    if resource_rva and resource_size:
        strings = _version_strings(data, sections, resource_rva)
    return {"timestamp": timestamp, "strings": strings}


def _version_strings(data: bytes, sections, resource_rva: int) -> dict:
    base = _rva_to_offset(sections, resource_rva)

    def entries(offset: int):
        named, ids = struct.unpack_from("<HH", data, offset + 12)
        found, cursor = [], offset + 16
        for _ in range(named + ids):
            entry_id, child = struct.unpack_from("<II", data, cursor)
            cursor += 8
            found.append((entry_id, bool(child & 0x80000000), base + (child & 0x7FFFFFFF)))
        return found

    blob = b""
    for entry_id, is_dir, child in entries(base):
        if entry_id != 16 or not is_dir:
            continue
        for _name_id, name_is_dir, name_child in entries(child):
            if not name_is_dir:
                continue
            for _lang, lang_is_dir, lang_child in entries(name_child):
                if lang_is_dir:
                    continue
                data_rva, size, _codepage, _reserved = struct.unpack_from("<IIII", data, lang_child)
                start = _rva_to_offset(sections, data_rva)
                blob = data[start:start + size]
    if not blob:
        return {}
    text = blob.decode("utf-16-le", errors="ignore")
    found = {}
    for key in ("CompanyName", "FileVersion", "ProductVersion", "ProductName", "OriginalFilename", "FileDescription"):
        at = text.find(key + "\0")
        if at < 0:
            continue
        value = text[at + len(key) + 1:].lstrip("\0").split("\0", 1)[0].strip()
        if value:
            found[key] = value
    return found
