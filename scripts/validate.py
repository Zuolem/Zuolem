"""Offline validation of profile assets, local links, and SVG safety."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
assets = list((root / 'assets').glob('*.svg'))
required = {'hero', 'hero-mobile', 'whoami', 'whoami-mobile', 'toolbox', 'toolbox-mobile', 'projects', 'projects-mobile', 'activity', 'activity-mobile', 'zuostation', 'm-spect', 'electrolyser-hmi', 'b9-solar'}
assert {asset.stem for asset in assets} == required, 'Missing or obsolete SVG artwork'
for asset in assets:
    tree = ET.parse(asset)
    assert tree.getroot().get('viewBox'), asset
    for node in tree.iter():
        assert node.tag.split('}')[-1] not in ('script', 'foreignObject', 'image'), asset
        assert not any(key.lower().startswith('on') for key in node.attrib), asset
        assert not any('href' in key for key in node.attrib), asset
    assert tree.find('{http://www.w3.org/2000/svg}title') is not None, asset
readme = (root / 'README.md').read_text(encoding='utf-8')
links = re.findall(r'(?:src|srcset|href)="([^"]+)"|\]\(([^)]+)\)', readme)
for pair in links:
    target = next(value for value in pair if value)
    if target.startswith('https://'):
        assert target == 'https://github.com/Zuolem?tab=overview', target
    else:
        assert (root / target).is_file(), target
assert len(re.findall(r'<img\b', readme)) == 5
assert len(re.findall(r'<source\b', readme)) == 5
assert '```' not in readme, 'Presentation must not have code copy controls'
assert 'javascript:' not in readme.lower()
print(f'Validated {len(assets)} SVGs and every README link. No remote artwork or private project links.')
