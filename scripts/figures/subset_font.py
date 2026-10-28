"""Create the local SVG-viewer font. Usage: python3 .../subset_font.py NotoSansCJKsc-Regular.otf

Requires fontTools. Font is licensed under SIL OFL 1.1; see site/figure-fonts/.
Only characters used in the current figure vectors are retained.
"""
import sys,json,xml.etree.ElementTree as ET
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[2];figures=root/'textbook/assets/figures'
records=json.loads((figures/'manifest.json').read_text())
text=''.join(''.join(ET.fromstring((figures/r['zoomFile']).read_text()).itertext()) for r in records if r.get('zoomFile'))
font=TTFont(sys.argv[1]);options=subset.Options();options.flavor='woff';options.desubroutinize=True
subsetter=subset.Subsetter(options=options);subsetter.populate(text=text);subsetter.subset(font)
for record in font['name'].names:
    if record.nameID in (1,4,6):record.string='AIOS101FigureSans'.encode(record.getEncoding())
font.flavor='woff';font.save(root/'site/figure-fonts/figure-sans.woff')
