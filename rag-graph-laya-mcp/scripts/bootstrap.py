"""Acquire verified portable runtimes inside .state; never install a Windows service."""
import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.state' / 'runtime'


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'CodENavi-RGL/0.1'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def download(url, target, expected):
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        return
    data = fetch(url)
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Official download checksum mismatch')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def extract(archive, destination):
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if not (destination / name).resolve().is_relative_to(destination.resolve()):
                raise ValueError('Archive member escapes the runtime destination')
        z.extractall(destination)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', action='store_true')
    parser.add_argument('--assets', action='store_true')
    args = parser.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    records = {}
    existing = json.loads((STATE / 'manifest.json').read_text()) if (STATE / 'manifest.json').exists() else {}
    graph = existing.get('graph', {})
    graph_ready = bool(graph) and (Path(graph['java_home']) / 'bin/java.exe').is_file() and (Path(graph['neo4j_home']) / 'lib').is_dir()
    if args.graph and graph_ready:
        records['graph'] = graph
    elif args.graph:
        release = json.loads(fetch('https://api.github.com/repos/adoptium/temurin21-binaries/releases/latest'))
        asset = next(a for a in release['assets'] if a['name'].startswith('OpenJDK21U-jdk_x64_windows_hotspot_') and a['name'].endswith('.zip'))
        checksum_asset = next(a for a in release['assets'] if a['name'] == asset['name'] + '.sha256.txt')
        package = {'link': asset['browser_download_url'], 'checksum': fetch(checksum_asset['browser_download_url']).decode().split()[0]}
        jdk_archive = STATE / 'jdk.zip'
        download(package['link'], jdk_archive, package['checksum'])
        extract(jdk_archive, STATE / 'java')
        url = 'https://dist.neo4j.org/neo4j-community-5.26.0-windows.zip'
        checksum = fetch(url + '.sha256').decode().strip().split()[0]
        archive = STATE / 'neo4j.zip'
        download(url, archive, checksum)
        extract(archive, STATE / 'neo4j')
        java = next((STATE / 'java').glob('*/bin/java.exe'))
        neo4j = next((STATE / 'neo4j').glob('neo4j-*'))
        records['graph'] = {'java_home': str(java.parents[1]), 'neo4j_home': str(neo4j),
                            'neo4j_sha256': checksum, 'java_sha256': package['checksum'], 'neo4j_version': '5.26.0'}
    if args.assets:
        # Pin the source commit and hash; the script never executes upstream build helpers.
        asset_manifest = ROOT / 'static/vendor/manifest.json'
        commit = (json.loads(asset_manifest.read_text())['revision'] if asset_manifest.exists()
                  else json.loads(fetch('https://api.github.com/repos/cytoscape/cytoscape.js/commits/HEAD'))['sha'])
        url = f'https://raw.githubusercontent.com/cytoscape/cytoscape.js/{commit}/dist/cytoscape.min.js'
        data = fetch(url)
        dest = ROOT / 'static/vendor'
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'cytoscape.min.js').write_bytes(data)
        (dest / 'LICENSE').write_bytes(fetch(f'https://raw.githubusercontent.com/cytoscape/cytoscape.js/{commit}/LICENSE'))
        manifest = {'repository': 'cytoscape/cytoscape.js', 'revision': commit,
                    'sha256': hashlib.sha256(data).hexdigest(), 'license': 'MIT', 'source': url}
        (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        records['visualization'] = manifest
    path = STATE / 'manifest.json'
    old = json.loads(path.read_text()) if path.exists() else {}
    path.write_text(json.dumps({**old, **records}, indent=2), encoding='utf-8')
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
