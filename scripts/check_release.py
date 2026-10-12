# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Fast, offline release regression; never connects to an LMS or object store."""
import ast
import importlib.util
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import public_release as release


def run(args, **kwargs):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, **kwargs)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def main():
    identity, names = release.verify_source()
    python_tests = run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    php = shutil.which('php')
    if not php:
        raise RuntimeError('PHP must be on PATH; do not claim skipped lint as PASS')
    phpfiles = [n for n in names if n.endswith('.php')]
    for n in phpfiles:
        run([php, '-l', str(ROOT / n)])
    compatibility = run([php, 'tests/test_compatibility.php'])
    guidance = run([php, 'tests/test_installation_guidance.php'])
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Node must be on PATH')
    js = [n for n in names if n.endswith(('.js', '.cjs'))]
    for n in js:
        if '/amd/src/' in n:
            run([node, '--input-type=module', '--check'], input=(ROOT / n).read_text())
        else:
            run([node, '--check', str(ROOT / n)])
    uploader = run([node, 'tests/test_upload_urls.cjs'])
    upload_errors = run([node, 'tests/test_upload_errors.cjs'])
    for n in [n for n in names if n.endswith('.py')]:
        ast.parse((ROOT / n).read_text(), filename=n)
    xml = [n for n in names if n.endswith('.xml')]
    for n in xml:
        ET.parse(ROOT / n)
    svg = [n for n in names if n.endswith('.svg')]
    for n in svg:
        text = (ROOT / n).read_text()
        root = ET.fromstring(text)
        if root.tag != '{http://www.w3.org/2000/svg}svg' or '<!DOCTYPE' in text or '\\n' in text:
            raise RuntimeError('Invalid or unsafe SVG: ' + n)
        for element in root.iter():
            for key, value in element.attrib.items():
                if (key == 'href' or key.endswith('}href')) and not value.startswith('#'):
                    raise RuntimeError('Non-local SVG asset: ' + n)
    with tempfile.TemporaryDirectory() as directory:
        run([node, 'scripts/build_upload_amd.cjs', directory])
        for filename in sorted(p.name for p in Path(directory).iterdir()):
            if (Path(directory) / filename).read_bytes() != (ROOT / 'plugin/mod_videolessonstream/amd/build' / filename).read_bytes():
                raise RuntimeError('AMD output differs')
    result = {'result': 'PASS', 'plugin_version': identity['plugin_version'],
              'service_version': identity['service_version'], 'php_files': len(phpfiles),
              'js_files': len(js), 'xml_files': len(xml),
              'svg_files': len(svg),
              'python_tests': int(re.search(r'Ran (\d+) tests', python_tests).group(1)),
              'amd': 'reproduced exact bytes/map',
              'compatibility': compatibility.strip(), 'onboarding': guidance.strip(),
              'uploader': uploader.strip(), 'upload_errors': upload_errors.strip(),
              'python': run([sys.executable, '--version']).strip(), 'php': run([php, '-v']).splitlines()[0],
              'node': run([node, '--version']).strip(), 'phpcs_available': bool(shutil.which('phpcs')),
              'public_scan': release.scan({n: (ROOT / n).read_bytes() for n in names}),
              'media_matrix_repeated': False}
    target = ROOT / '.lab/evidence/development/installation-ux/FAST-REGRESSIONS.json'
    release.write(target, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
