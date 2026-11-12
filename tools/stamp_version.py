"""Add ?v=<git hash> to every local asset URL in index.html and write a build stamp.
Run before committing:  python tools/stamp_version.py
"""
import re, subprocess, datetime, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=root).decode().strip()
# the commit being created will have a different hash; use hash+time of this stamp instead
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
ver = f'{ver}-{stamp}'
# strip old version queries, then add new ones to src/href pointing at assets/
s = re.sub(r'(assets/[^"\'?#\s]+)\?v=[\w\-]+', r'\1', s)
s = re.sub(r'((?<![\w-])(?:src|href)=")(assets/[^"?#]+)"', lambda m: f'{m.group(1)}{m.group(2)}?v={ver}"', s)
s = re.sub(r"window\.ASSET_VER = '[^']*'", f"window.ASSET_VER = '{ver}'", s)
s = re.sub(r'(<span id="build">)[^<]*(</span>)', rf'\g<1>{ver}\g<2>', s)
open(p, 'w', encoding='utf-8').write(s)
print('stamped', ver, '| versioned urls:', s.count(f'?v={ver}'))
