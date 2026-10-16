"""Exact runtime inventory and download verification; rejects transfer leftovers."""
from pathlib import Path
import hashlib, json, sys, tarfile
from zipfile import ZipFile

MANIFEST = 'runtime-manifest.json'
def digest(data): return hashlib.sha256(data).hexdigest()
def inventory(root):
    data = {}
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root); name = rel.as_posix()
        if p.is_symlink(): raise ValueError('Symlink in release: ' + name)
        if any(part in {'.rsync-tmp', '.git', 'node_modules', '__pycache__'} or part.endswith('.tmp') for part in rel.parts): raise ValueError('Temporary path in release: ' + name)
        if not p.is_file(): continue
        if name in {MANIFEST, 'download-checksums.json', '.openai/hosting.json'} or rel.parts[0] == 'downloads': continue
        data[name] = digest(p.read_bytes())
    return data

def check(root, archive=None):
    expected = json.loads((root / MANIFEST).read_text())['files']
    actual = inventory(root)
    if actual != expected:
        raise ValueError(json.dumps({'missing': sorted(expected.keys()-actual.keys()), 'extra': sorted(actual.keys()-expected.keys()), 'changed': [k for k in expected.keys() & actual.keys() if expected[k]!=actual[k]]}))
    receipts = json.loads((root/'download-checksums.json').read_text())
    if {r['path'] for r in receipts} != {'lantern-inn-static.zip','corresponding-source.zip','lantern-inn-project.zip'}: raise ValueError('Required downloads missing')
    if {p.name for p in (root/'downloads').iterdir()} != {r['path'] for r in receipts}: raise ValueError('Download inventory differs')
    for r in receipts:
        p = root/'downloads'/r['path']
        if p.stat().st_size != r['bytes'] or digest(p.read_bytes()) != r['sha256']: raise ValueError('Download hash differs: '+p.name)
        with ZipFile(p) as z:
            if z.testzip(): raise ValueError('Invalid ZIP: '+p.name)
            if any('/.rsync-tmp/' in n or n.startswith('.rsync-tmp/') for n in z.namelist()): raise ValueError('Temporary file in ZIP')
            manifest = {'lantern-inn-static.zip':MANIFEST,'corresponding-source.zip':'SOURCE-MANIFEST.json','lantern-inn-project.zip':'PROJECT-MANIFEST.json'}.get(p.name)
            if not manifest: raise ValueError('Unexpected download name')
            entries = [n for n in z.namelist() if not n.endswith('/')]
            if len(entries) != len(set(entries)): raise ValueError('Duplicate ZIP member')
            sealed = json.loads(z.read(manifest))['files']
            contained = {n:digest(z.read(n)) for n in entries if n!=manifest}
            if sealed != contained: raise ValueError('ZIP inner inventory differs: '+p.name)
            if p.name == 'lantern-inn-static.zip':
                if set(sealed) != set(expected)|{'DOWNLOADS.md'}: raise ValueError('Static ZIP runtime set differs')
                for n, h in expected.items():
                    data = z.read(n)
                    if n in {'index.html','help.html','pilot/index.html','chapter/index.html'}:
                        prefix='../downloads/' if n in {'pilot/index.html','chapter/index.html'} else 'downloads/'
                        data = data.decode().replace('href="https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/downloads/','href="'+prefix).encode()
                    if digest(data)!=h: raise ValueError('Static ZIP runtime content differs: '+n)
    if archive:
        with tarfile.open(archive) as t:
            members = {}
            for m in t:
                if m.issym() or m.islnk(): raise ValueError('Archive link rejected')
                if not m.isfile(): continue
                if not m.name.startswith('dist/'): raise ValueError('Unexpected archive root')
                name = m.name[len('dist/'):]
                if '/.rsync-tmp/' in name: raise ValueError('Temporary archive path')
                if name == '.openai/hosting.json': continue
                if name in members: raise ValueError('Duplicate archive member')
                members[name] = digest(t.extractfile(m).read())
            wanted = {p.relative_to(root).as_posix():digest(p.read_bytes()) for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix()!='.openai/hosting.json'}
            if members != wanted: raise ValueError('Deployment archive inventory differs from verified output')
    return {'status':'PASS', 'runtime_files':len(expected), 'downloads':len(receipts), 'archive_checked':bool(archive)}

if __name__ == '__main__':
    command, folder, *rest = sys.argv[1:]; root = Path(folder)
    if command == 'write':
        files = inventory(root); (root/MANIFEST).write_text(json.dumps({'version':1,'files':files},indent=2)+'\n'); print('RUNTIME_INVENTORY_WRITTEN',len(files))
    elif command == 'check': print(json.dumps(check(root,rest[0] if rest else None)))
    else: raise ValueError('Expected write or check')
