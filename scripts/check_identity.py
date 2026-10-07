# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Offline component/table/AMD isolation check; published RC1 is immutable input."""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from public_release import source_paths

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugin/mod_videolessonstream'


def validate():
    component = re.search(r"\$plugin->component\s*=\s*'([^']+)'", (PLUGIN / 'version.php').read_text())
    if not component or component[1] != 'mod_videolessonstream' or not re.fullmatch(r'mod_[a-z][a-z0-9]*', component[1]):
        raise ValueError('Invalid Moodle activity identity; module names cannot contain underscores')
    if PLUGIN.name != component[1]:
        raise ValueError('Component directory differs from version metadata')
    xml = ET.parse(PLUGIN / 'db/install.xml').getroot()
    tables = [t.attrib['NAME'] for t in xml.findall('TABLES/TABLE')]
    legacy = ET.parse(ROOT / 'docs/release/rc1/COLLISION-SCHEMA.xml').getroot()
    old = {t.attrib['NAME'] for t in legacy.findall('TABLES/TABLE')}
    if len(tables) != 13 or set(tables) & old or any(len(n) > 28 for n in tables):
        raise ValueError('Colliding or unsafe table namespace')
    if len(set(tables)) != len(tables):
        raise ValueError('Duplicate tables')
    if not (PLUGIN / 'lang/en/videolessonstream.php').is_file():
        raise ValueError('Missing component language')
    old_component = re.compile(r'mod_videolesson(?!stream)|/mod/videolesson/|mod/videolesson:|'
        r'\bvideolesson_(?:add_instance|update_instance|delete_instance)\b')
    for n in source_paths():
        p = ROOT / n
        if not n.startswith('plugin/mod_videolessonstream/') or p.suffix == '.png':
            continue
        text = p.read_text()
        if old_component.search(text) or re.search('codefortex', text, re.I):
            raise ValueError('Unexpected active old identity: ' + p.relative_to(ROOT).as_posix())
        if p.suffix in ('.php', '.xml') and any(re.search(r"[{'\"]" + re.escape(n) + r"[}'\"]", text) for n in old):
            raise ValueError('Legacy table/name: ' + p.relative_to(ROOT).as_posix())
    sources = list((PLUGIN / 'amd/src').glob('*.js'))
    for p in sources:
        build = PLUGIN / 'amd/build' / (p.stem + '.min.js')
        source_map = json.loads(build.with_suffix('.js.map').read_text())
        if source_map['sourcesContent'] != [p.read_text()]:
            raise ValueError('Stale AMD map: ' + p.name)
        if 'mod_videolessonstream/' + p.stem not in build.read_text():
            raise ValueError('Wrong AMD module: ' + p.name)
    return {'component': 'mod_videolessonstream', 'tables': tables,
            'legacy_tables_overlap': [], 'amd_modules': len(sources), 'result': 'PASS'}


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
