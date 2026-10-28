#!/usr/bin/env python3
"""Build or verify an immutable AIOS101 visual baseline; standard library only."""
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def candidate():
    baseline = json.loads((ROOT/'brand/baseline.json').read_text())
    version = baseline['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Baseline version must be semantic x.y.z')
    expected_manifest = f'brand/releases/v{version}.manifest.json'
    expected_archive = f'site/assets/course/aios101-identity-kit-v{version}.zip'
    if baseline['manifest'] != expected_manifest or baseline['archive'] != expected_archive:
        raise ValueError('Version and release paths disagree')
    tokens = json.loads((ROOT/baseline['tokens']).read_text())
    if baseline['status'] != 'approved' or tokens['version'] != version or tokens['status'] != 'approved':
        raise ValueError('Tokens do not match the approved baseline')
    css = (ROOT/'brand/tokens.css').read_text()
    for name, color in tokens['colors'].items():
        if f'--aios-{name}: {color};' not in css:
            raise ValueError(f'CSS / JSON palette drift: {name}')
    sections = css.split("[data-aios-theme='dark']")
    if len(sections) != 2:
        raise ValueError('Expected exactly one light and one dark CSS theme')
    for theme, section in zip(('light', 'dark'), sections):
        for name, color in tokens['themes'][theme].items():
            if f'--aios-{name}: {color};' not in section:
                raise ValueError(f'CSS / JSON theme drift: {theme}.{name}')

    paths = sorted(p for p in (ROOT/'site/assets/course').glob('*.svg') if p.name != 'identity-board.svg')
    if len(paths) != 16:
        raise ValueError('Expected 16 approved production SVGs; review inventory before changing')
    paths += [ROOT/p for p in [
        'site/assets/course/tokens.json', 'site/assets/course/README.md',
        'site/assets/NOTICE.md', 'site/assets/logo-light.svg', 'site/assets/logo-dark.svg',
        'site/assets/full-logo-light.svg', 'site/assets/full-logo-dark.svg',
        'brand/README.md', 'brand/baseline.json', 'brand/tokens.css', 'brand/examples/cobrand.html',
    ]]
    for folder in ['fonts', 'icons']:
        paths += sorted(p for p in (ROOT/'site/assets'/folder).iterdir() if p.is_file())
    files = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in sorted(paths)}
    manifest = {
        'schema': 1, 'id': baseline['id'], 'version': version,
        'status': baseline['status'], 'approvedOn': baseline['approvedOn'],
        'designSourceCommit': baseline['designSourceCommit'],
        'xlabSourceCommit': baseline['xlabSourceCommit'],
        'archive': baseline['archive'], 'productionSvgCount': 16,
        'files': [{'path': p, 'bytes': len(b), 'sha256': sha256(b)} for p, b in files.items()],
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
    files[baseline['manifest']] = manifest_bytes
    sums = ''.join(f'{sha256(b)}  {p}\n' for p, b in sorted(files.items())).encode()
    files['SHA256SUMS.txt'] = sums
    buffer = io.BytesIO()
    date = tuple(map(int, baseline['approvedOn'].split('-'))) + (0, 0, 0)
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, body in sorted(files.items()):
            entry = zipfile.ZipInfo(f'AIOS101-Visual-v{version}/{path}', date_time=date)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, body)
    return baseline, manifest_bytes, buffer.getvalue(), len(manifest['files'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--build', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        baseline, manifest, archive, count = candidate()
        outputs = {
            ROOT/baseline['manifest']: manifest,
            ROOT/baseline['archive']: archive,
            ROOT/(baseline['archive']+'.sha256'): (sha256(archive)+'  '+Path(baseline['archive']).name+'\n').encode(),
        }
        # Validate every existing output before any write: a version is never overwritten.
        for path, body in outputs.items():
            if path.exists() and path.read_bytes() != body:
                raise ValueError(f'Frozen version differs: {path.relative_to(ROOT)}. Review changes and create a new version.')
            if args.check and not path.exists():
                raise ValueError(f'Missing release file: {path.relative_to(ROOT)}')
        if args.build:
            for path, body in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_bytes(body)
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            if z.testzip() is not None:
                raise ValueError('ZIP integrity failure')
        print(f'PASS: visual baseline v{baseline["version"]}; {count} source files; 16 production SVGs; SHA-256 and deterministic ZIP verified')
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f'Baseline check failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
