#!/usr/bin/env python3
"""Print a file-level audit from local full-history upstream clones; never modify skills."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def tree(repo, revision, directory):
    result = {}
    for record in git(repo, 'ls-tree', '-rz', revision, '--', directory).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        relative = str(Path(path.decode()).relative_to(directory))
        result[relative] = meta.decode().split()[2]
    return result


def worktree(directory):
    result = {}
    for path in sorted(directory.rglob('*')):
        if path.is_file() and path.name != '.DS_Store':
            content = path.read_bytes()
            blob = b'blob ' + str(len(content)).encode() + b'\0' + content
            result[str(path.relative_to(directory))] = hashlib.sha1(blob).hexdigest()
    return result


def changes(before, after):
    return {name: 'added' if name not in before else 'deleted' if name not in after else 'modified'
            for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)}


def skill_paths(repo, revision):
    paths = git(repo, 'ls-tree', '-r', '--name-only', revision).decode().splitlines()
    return {Path(p).parent.name: str(Path(p).parent) for p in paths
            if p.startswith('skills/') and p.endswith('/SKILL.md')}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('matt', type=Path)
parser.add_argument('cursor', type=Path)
parser.add_argument('--matt-ref', default='HEAD')
parser.add_argument('--cursor-ref', default='HEAD')
args = parser.parse_args()
local = Path(__file__).resolve().parents[2]
sources = {
    'matt': (args.matt, '885e2ca', args.matt_ref),
    'pstack': (args.cursor, 'fd6dd6f', args.cursor_ref),
}
metadata = {key: {'base': git(repo, 'rev-parse', base).decode().strip(),
                  'head': git(repo, 'rev-parse', head).decode().strip()}
            for key, (repo, base, head) in sources.items()}
matt_base = skill_paths(args.matt, metadata['matt']['base'])
matt_head = skill_paths(args.matt, metadata['matt']['head'])
pstack_names = set('architect arena blast-radius bro create-verification-skill maintain-verification-skill recall reflect figure-it-out how no-comments show-me-your-work swarm technical-writing unslop why'.split())
rows = []
for directory in sorted((local / 'skills').iterdir()):
    name = directory.name
    if not (directory / 'SKILL.md').exists():
        continue
    if name in pstack_names or name.startswith('principle-'):
        source = 'pstack'
        base_path = head_path = f'pstack/skills/{name}'
    else:
        upstream_name = 'setup-matt-pocock-skills' if name == 'setup-axostack' else name
        if upstream_name not in matt_base:
            rows.append({'skill': name, 'source': 'local', 'note': 'Review related upstream workflows manually.'})
            continue
        source = 'matt'
        base_path = matt_base[upstream_name]
        head_path = matt_head.get(upstream_name, base_path)
    repo = sources[source][0]
    base = tree(repo, metadata[source]['base'], base_path)
    head = tree(repo, metadata[source]['head'], head_path)
    installed = worktree(directory)
    rows.append({'skill': name, 'source': source, 'base_path': base_path, 'head_path': head_path,
                 'upstream_changes': changes(base, head), 'local_changes_since_base': changes(base, installed),
                 'local_differs_from_head': changes(head, installed)})
print(json.dumps({'local_head': git(local, 'rev-parse', 'HEAD').decode().strip(),
                  'sources': metadata, 'skills': rows}, indent=2))
