"""Compact fixed GOSD course SVG exports; never regenerate factual content.

Usage: python scripts/figures/optimize_gosd.py INPUT_EXPORT_FOLDER
Requires Pillow. Input hashes and transformations are recorded alongside assets.
"""
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / 'textbook/assets/figures'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')


def optimize(source):
    raw = source.read_bytes()
    tree = ET.fromstring(raw)
    number = source.name.split('_')[1].split('-')[-1]
    texts = [el.text for el in tree.iter()]
    styles = {}
    images = 0
    for el in tree.iter():
        if 'style' in el.attrib:
            style = el.attrib.pop('style')
            cls = styles.setdefault(style, f'gosd{number}s{len(styles)}')
            el.set('class', (el.get('class', '') + ' ' + cls).strip())
        if el.tag.split('}')[-1] != 'image':
            continue
        key = 'href' if 'href' in el.attrib else '{http://www.w3.org/1999/xlink}href'
        href = el.get(key, '')
        if not href.startswith('data:image/'):
            raise ValueError('Unexpected external image reference')
        original = base64.b64decode(href.split(',', 1)[1])
        im = Image.open(io.BytesIO(original)).convert('RGBA')
        # Four source pixels per native displayed pixel, twice what 2x view needs.
        bounds = tuple(max(1, math.ceil(float(el.get(k)) * 4)) for k in ('width', 'height'))
        im.thumbnail(bounds, Image.Resampling.LANCZOS)
        compressed = io.BytesIO()
        im.save(compressed, format='WEBP', quality=92, method=6)
        encoded = 'data:image/webp;base64,' + base64.b64encode(compressed.getvalue()).decode()
        if len(encoded) < len(href):
            el.set(key, encoded)
            images += 1
    assert texts == [el.text for el in tree.iter()], 'Source text changed'
    style_el = ET.Element('{' + NS + '}style')
    style_el.text = ''.join('.' + cls + '{' + style + '}' for style, cls in styles.items())
    tree.insert(0, style_el)
    out = FIGURES / 'vector' / source.name.replace('_v01.svg', '_v02.svg')
    out.write_bytes(ET.tostring(tree, encoding='utf-8'))
    return {'id': '3-' + str(int(number)), 'sourceFile': source.name,
            'sourceSha256': hashlib.sha256(raw).hexdigest(), 'sourceBytes': len(raw),
            'file': out.relative_to(FIGURES).as_posix(), 'bytes': out.stat().st_size,
            'stylesDeduplicated': len(styles), 'iconsCompressed': images,
            'textAndGeometry': 'unchanged', 'iconPolicy': 'WebP quality 92; up to 4x native display dimensions'}


if __name__ == '__main__':
    source_dir = Path(sys.argv[1])
    results = [optimize(next(source_dir.glob(f'AIOS101_Fig-03-{n:02d}_*_v01.svg')))
               for n in (2, 3, 6, 7)]
    (FIGURES / 'sources/gosd-vector-optimization.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))
