#!/usr/bin/env python3
"""Validate current figure identity and derive the delivery index from the textbook."""
from pathlib import Path
import argparse,json,re
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/'textbook/assets/figures'
def catalogue():
    current=json.loads((F/'manifest.json').read_text())
    retired=json.loads((F/'retired.json').read_text())
    ids=[x['id'] for x in current]
    by_id={x['id']:x for x in current}
    assert len(ids)==len(set(ids)), 'Duplicate current figure ID'
    assert not set(ids)&{x['id'] for x in retired}, 'Retired ID reused'
    paths=[ROOT/'textbook/preface.md',*sorted((ROOT/'textbook/chapters').glob('CH0[1-6]-*.md'))]
    occurrences={}
    for path in paths:
        text=path.read_text()
        for match in re.finditer(r'^!\[图 (\d+-\d+)　([^\]]+)\]\(([^)]+)\)$',text,re.M):
            number,label,file=match.groups()
            assert number in by_id,'Unregistered figure: '+number
            title=by_id[number]['title']
            assert number not in occurrences,'Figure appears twice: '+number
            captions=re.findall(r'^图 '+re.escape(number)+r'　(.+)$',text,re.M)
            assert len(captions)==1 and captions[0].startswith(title+'。'),'Caption differs: '+number
            headings=re.findall(r'^#{1,3} (.+)$',text[:match.start()],re.M)
            location=' / '.join([headings[0],headings[-1]])
            occurrences[number]=(title,(path.parent/file).resolve(),path,location)
    assert set(occurrences)==set(ids),f'Figures differ: {set(ids)^set(occurrences)}'
    lines=['# 当前教材图版交付索引','','本表由 `scripts/figures/catalog.py` 从当前正文和 `manifest.json` 生成。图号、图题、文件和插入位置在此统一；历史编号不另作他用。','','| 图号 | 统一图题 | 正文插入位置 | 当前文件 | 大图源 |','|---|---|---|---|---|']
    for record in current:
        n=record['id']; title,file,path,location=occurrences[n]
        assert title==record['title'],'Manifest title differs: '+n
        assert file==(F/record['file']).resolve(),'Manifest file differs: '+n
        assert file.is_file() and file.stat().st_size==record['bytes'],'Asset missing or changed: '+n
        vector=record.get('zoomFile');zoom=f'[SVG]({vector})' if vector else '原像素图'
        lines.append(f"| 图 {n} | {title} | {location} | [WebP]({record['file']}) | {zoom} |")
    lines+=['','## 退出正文的历史图号','','原拟图 0-1、0-2 及附录图 A-1 已在上一轮撤销，不复用。']
    for record in retired:
        lines.append(f"- 图 {record['id']}　{record['title']}：{record['retirementReason']} 历史文件：[WebP]({record['file']})。")
    return '\n'.join(lines)+'\n',len(current),len(retired)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    text,count,retired=catalogue();target=F/'INDEX.md'
    if args.write:target.write_text(text)
    else:assert target.read_text()==text,'Figure index is stale; run --write'
    print(f'PASS: {count} current figures, unique IDs, exact titles/captions/files; {retired} retired IDs')
