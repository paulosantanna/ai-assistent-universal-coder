#!/usr/bin/env python3
"""Verify the installed TLC workspace contract without invoking external providers."""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[4]
CATALOG_ROOT = ROOT / '00_skills'


def digest(path):
    data = path.read_bytes()
    if b'\0' not in data:
        try:
            data.decode('utf-8')
            data = data.replace(b'\r\n', b'\n')
        except UnicodeDecodeError:
            pass
    return hashlib.sha256(data).hexdigest()


def markdown_links(text):
    """Read balanced Markdown destinations, including category parentheses."""
    fence = None
    lines = []
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    text = '\n'.join(lines)
    # Inline code documents paths/examples; it is not a Markdown hyperlink.
    text = re.sub(r'(`+)(.*?)\1', '', text)
    for start in re.finditer(r'\]\(', text):
        pos, depth, escaped = start.end(), 1, False
        end = pos
        while end < len(text) and depth:
            char = text[end]
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            end += 1
        if depth == 0:
            value = text[pos:end - 1].strip()
            if value.startswith('<') and '>' in value:
                value = value[1:value.index('>')]
            else:
                value = re.split(r'\s+[\"\']', value, maxsplit=1)[0]
            yield re.sub(r'\\([() ])', r'\1', value)


def validate(root):
    global ROOT, CATALOG_ROOT
    ROOT, CATALOG_ROOT = root.resolve(), root.resolve() / '00_skills'
    errors, warnings = [], []
    counts = {'active': 0, 'aliases': 0, 'tlc': 0, 'upstream_files': 0,
              'images': 0, 'distinct_images': 0, 'discovery': 0,
              'skill_entries': 0, 'local_links': 0, 'max_lines': 0}

    def require(condition, scope, detail):
        if not condition:
            errors.append({'scope': str(scope), 'detail': detail})

    def read_json(path):
        return json.loads(path.read_text(encoding='utf-8'))

    architect_path = CATALOG_ROOT / '(creation)/skill-architect/scripts/validate_skill.py'
    module_spec = importlib.util.spec_from_file_location('tlc_architect', architect_path)
    architect = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(architect)

    def frontmatter(path):
        text = path.read_text(encoding='utf-8-sig')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.S)
        if not match:
            raise ValueError('Missing YAML delimiters')
        return architect.parse_frontmatter(match[1])[0], text

    catalog = read_json(CATALOG_ROOT / 'catalog.json')
    upstream = read_json(CATALOG_ROOT / 'upstream.manifest.json')
    images = read_json(CATALOG_ROOT / 'images.manifest.json')
    entries = catalog['skills']
    ids = [entry['id'] for entry in entries]
    require(len(ids) == len(set(ids)), 'catalog', 'Duplicate canonical IDs')
    counts['active'] = len(entries)
    counts['aliases'] = sum(len(entry['aliases']) for entry in entries)
    visited, queue = set(), []
    for entry in entries:
        path = ROOT / entry['path']
        require(path.is_file(), entry['id'], 'Missing canonical entry')
        require(re.fullmatch(r'00_skills/\([a-z0-9-]+\)/[a-z0-9-]+/SKILL\.md', entry['path']),
                entry['id'], 'Incorrect category/package hierarchy')
        if not path.is_file():
            continue
        try:
            fm, text = frontmatter(path)
        except (ValueError, TypeError) as exc:
            require(False, entry['id'], str(exc))
            continue
        require(fm.get('name') == entry['id'] == path.parent.name,
                entry['id'], 'Name differs from canonical folder/ID')
        metadata = fm.get('metadata', {})
        require(list(fm)[:4] == ['name', 'description', 'license', 'metadata'],
                entry['id'], 'Incorrect frontmatter field order')
        require(list(metadata)[:2] == ['author', 'version'],
                entry['id'], 'Incorrect author/version order')
        require(bool(fm.get('license')) and bool(metadata.get('author')) and bool(metadata.get('version')),
                entry['id'], 'Missing license/author/version')
        require(metadata.get('owner_agent') == entry['owner_agent'] == 'codenavi-agent',
                entry['id'], 'Incorrect agent ownership')
        require(entry.get('sha256') == digest(path), entry['id'], 'Stale catalog digest')
        require(entry['description'] == fm.get('description'), entry['id'], 'Stale routing description')
        result = architect.validate_skill(str(path.parent))
        for check in result['checks']:
            if not check['passed']:
                item = {'scope': entry['id'], 'detail': check['name'] + ': ' + check['message']}
                (warnings if check['severity'] == 'warning' else errors).append(item)
        queue.append(path)
        for name in [entry['id']] + entry['aliases']:
            adapter = ROOT / '.agents/skills' / name / 'SKILL.md'
            require(adapter.is_file(), name, 'Missing native discovery entry')
            if adapter.is_file():
                afm, adapter_text = frontmatter(adapter)
                require(afm.get('name') == name and entry['path'] in adapter_text,
                        name, 'Discovery entry targets a different package')
                require(afm.get('description') == fm.get('description'),
                        name, 'Native routing description is stale')
                counts['discovery'] += 1

    # Check every entrypoint, including compatibility and retained examples.
    for folder in ('00_skills', 'skills', '.agents/skills', '.codex/skills'):
        for path in (ROOT / folder).rglob('SKILL.md'):
            lines = len(path.read_text(encoding='utf-8-sig').splitlines())
            counts['skill_entries'] += 1
            counts['max_lines'] = max(counts['max_lines'], lines)
            require(lines <= 100, path.relative_to(ROOT), f'{lines} physical lines; maximum is 100')

    # Follow actual module links, avoiding untouched source snapshots/examples.
    while queue:
        path = queue.pop()
        if path in visited or '/references/tlc/' in path.as_posix():
            continue
        visited.add(path)
        for target in markdown_links(path.read_text(encoding='utf-8-sig')):
            if not target or target.startswith('#') or re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I):
                continue
            target = unquote(target.split('#')[0])
            resolved = (path.parent / target).resolve()
            counts['local_links'] += 1
            require(resolved.is_relative_to(ROOT) and resolved.exists(),
                    path.relative_to(ROOT), 'Missing local link: ' + target)
            if resolved.is_file() and resolved.suffix == '.md' and resolved.is_relative_to(ROOT):
                queue.append(resolved)

    counts['tlc'] = len(upstream['skills'])
    require(counts['tlc'] > 0 and len({item['installed_path'] for item in upstream['skills']}) == counts['tlc'],
            'TLC snapshot', 'Source packages must be nonempty and unique')
    for entry in upstream['skills']:
        package = ROOT / entry['installed_path']
        require(package.name in ids, entry['name'], 'Upstream package missing from active catalog')
        for resource in entry['files']:
            path = package / resource['installed']
            counts['upstream_files'] += 1
            require(path.is_file() and digest(path) == resource['sha256'],
                    entry['name'], 'Upstream resource changed/missing: ' + resource['installed'])

    counts['distinct_images'] = len(images['images'])
    source_ids = [sid for image in images['images'] for sid in image['source_ids']]
    counts['images'] = len(source_ids)
    require(len(source_ids) == len(set(source_ids)) == images['files'] == 770,
            'image inventory', 'Missing or duplicated Drive IDs')
    require(counts['distinct_images'] == images['distinct_images'] == 389,
            'image inventory', 'Incorrect distinct image count')
    require([image['title'] for image in images['images']] == [f'IMG_{i}.jpg' for i in range(2112, 2501)],
            'image order', 'Photo order is incomplete or incorrect')
    require([image['order'] for image in images['images']] == list(range(1, 390)),
            'image order', 'Nonsequential image order')
    require(len({image['sha256'] for image in images['images']}) == 389,
            'image inventory', 'Duplicate image hashes')

    # New photographic updates are accounted separately from the immutable first batch.
    supplement_path = CATALOG_ROOT / 'images.2026-10-13.manifest.json'
    require('impeccable' not in ids or supplement_path.is_file(),
            'additional image inventory', 'Missing photographic-update manifest')
    if supplement_path.exists():
        supplement = read_json(supplement_path)
        additional = supplement['images']
        counts['additional_images'] = len(additional)
        additional_ids = [item['id'] for item in additional]
        require(len(additional_ids) == len(set(additional_ids)) == supplement['files'] == 77,
                'additional image inventory', 'Missing or duplicated additional Drive IDs')
        require([item['title'] for item in additional] == [f'IMG_{i}.jpg' for i in range(2700, 2777)],
                'additional image order', 'Additional photo order is incomplete or incorrect')
        require(all(re.fullmatch(r'[a-f0-9]{64}', item.get('sha256', ''))
                    and re.fullmatch(r'[a-f0-9]{64}', item.get('ocr_sha256', ''))
                    and item.get('visual_review') is True for item in additional),
                'additional image evidence', 'Missing image/OCR digest or visual-review accounting')

    imported_path = CATALOG_ROOT / '(design)/impeccable/source.manifest.json'
    require('impeccable' not in ids or imported_path.is_file(),
            'impeccable provenance', 'Missing imported-source manifest')
    if imported_path.exists():
        imported = read_json(imported_path)
        counts['impeccable_resources'] = len(imported['files'])
        for item in imported['files']:
            path = (ROOT / item['path']).resolve()
            require(path.is_relative_to((CATALOG_ROOT / '(design)/impeccable').resolve())
                    and path.is_file() and digest(path) == item['sha256'],
                    'impeccable provenance', 'Imported resource changed/missing: ' + item['path'])
    return {'status': 'PASS' if not errors else 'FAIL', 'counts': counts,
            'errors': errors, 'warnings': warnings,
            'scope': 'Installed instructions, local module links, native discovery, source integrity and image accounting. External provider execution is outside this check.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json-out', type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {'status': 'FAIL', 'errors': [{'scope': 'validator inputs', 'detail': str(exc)}]}
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'warnings'}, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
