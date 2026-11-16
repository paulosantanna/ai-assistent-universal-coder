"""Gate de asset visual do Science Studio, apoiado no detector Rust `assetguard`.

Política: asset com marca d'água suspeita é REJEITADO. Asset sem movimento observável é
`undetermined` e exige inspeção visual — nunca é declarado limpo por omissão. A remoção de marca
d'água só existe para asset próprio ou licenciado, com autorização registrada (`assetguard delogo`).

Uso:
    python science-studio/asset_gate.py .work/electron-factory-90min/project.json
    python science-studio/asset_gate.py .work/projeto/project.json --json report.json

Códigos de saída: 0 todos limpos; 3 marca d'água suspeita; 4 inspeção necessária; 1 erro.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SUSPECT = 'suspect'
UNDETERMINED = 'undetermined'
CLEAN = 'clean'


def binary() -> str:
    """Localiza o `assetguard` sem embutir caminho absoluto no projeto."""
    override = os.environ.get('ASSETGUARD_BIN', '').strip()
    if override:
        return override
    candidates = [
        Path(r'D:\Git\dark-videos\tools\assetguard\target\release\assetguard.exe'),
        Path(r'D:/Git/dark-videos/tools/assetguard/target/release/assetguard'),
        Path(__file__).resolve().parent.parent / 'tools' / 'assetguard' / 'target' / 'release'
        / 'assetguard.exe',
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(
        'assetguard não encontrado; compile com '
        '`cargo build --release` em D:\\Git\\dark-videos\\tools\\assetguard '
        'ou defina ASSETGUARD_BIN'
    )


def detect(asset: Path, *, frames: int = 120, timeout: int = 900) -> dict:
    """Executa a detecção real. Código 3 é resultado, não falha de execução."""
    completed = subprocess.run(
        [binary(), 'detect', str(asset), '--json', '--frames', str(frames)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode not in (0, 3):
        raise RuntimeError(
            f'assetguard falhou em {asset.name} (código {completed.returncode}): '
            f'{completed.stderr.strip()[:400]}'
        )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f'assetguard devolveu JSON inválido para {asset.name}: {error}') from error


def _cache_key(asset: Path) -> str:
    stat = asset.stat()
    return f'{asset.resolve()}|{stat.st_size}|{int(stat.st_mtime)}'


def check_assets(assets: list[Path], *, frames: int = 120, cache_file: Path | None = None) -> dict:
    """Checa uma lista de assets, reaproveitando resultados de arquivos inalterados."""
    cache: dict[str, dict] = {}
    if cache_file and cache_file.is_file():
        try:
            cache = json.loads(cache_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            cache = {}

    results: list[dict] = []
    counts = {CLEAN: 0, SUSPECT: 0, UNDETERMINED: 0}
    for asset in assets:
        if not asset.is_file():
            results.append({'file': str(asset), 'verdict': 'missing', 'error': 'asset ausente'})
            continue
        key = _cache_key(asset)
        report = cache.get(key)
        if report is None:
            report = detect(asset, frames=frames)
            cache[key] = report
        verdict = report.get('verdict', UNDETERMINED)
        counts[verdict] = counts.get(verdict, 0) + 1
        results.append(
            {
                'file': str(asset),
                'verdict': verdict,
                'confidence': report.get('confidence'),
                'method': report.get('method'),
                'regions': report.get('regions', [])[:5],
            }
        )

    if cache_file:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')

    return {
        'checked': len(assets),
        'counts': counts,
        'verdict': (
            SUSPECT if counts[SUSPECT]
            else UNDETERMINED if counts[UNDETERMINED]
            else CLEAN
        ),
        'assets': results,
    }


def project_assets(project_file: Path) -> list[Path]:
    project = json.loads(project_file.read_text(encoding='utf-8'))
    root = project_file.parent
    seen: list[Path] = []
    for scene in project.get('scenes', []):
        for layer in scene.get('layers', []):
            path = (root / layer['path']).resolve()
            if path not in seen:
                seen.append(path)
    return seen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Gate de marca d\'água dos assets do projeto')
    parser.add_argument('project', type=Path)
    parser.add_argument('--json', dest='json_out', type=Path)
    parser.add_argument('--frames', type=int, default=120)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args(argv)

    try:
        assets = project_assets(args.project)
        report = check_assets(assets, frames=args.frames, cache_file=args.cache)
    except (FileNotFoundError, RuntimeError) as error:
        print(f'asset_gate: {error}', file=sys.stderr)
        return 1

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    counts = report['counts']
    print(
        f"assets={report['checked']} limpos={counts[CLEAN]} "
        f"suspeitos={counts[SUSPECT]} indeterminados={counts[UNDETERMINED]}"
    )
    for item in report['assets']:
        if item['verdict'] != CLEAN:
            print(f"  {item['verdict'].upper():13} {Path(item['file']).name} "
                  f"({item.get('method')})")
    return {CLEAN: 0, SUSPECT: 3, UNDETERMINED: 4}.get(report['verdict'], 1)


if __name__ == '__main__':
    raise SystemExit(main())
