import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Set, List

SUPPORTED_LANG_EXTS = {
    'python': {'.py'},
    'java': {'.java'},
    'javascript': {'.js', '.jsx'},
    'typescript': {'.ts', '.tsx'},
    'cpp': {'.cpp', '.cc', '.cxx', '.c++', '.hpp', '.h', '.c'},
    'c': {'.c', '.h'},
}

CTAGS_KINDS = {'function', 'method', 'class', 'struct'}


def run_ctags(project_path: str, target_dir: str) -> str:
    """Run ctags on project_path/target_dir and return path to tags file (JSON lines).
    Returns empty string on failure."""
    src = os.path.join(project_path, target_dir) if target_dir else project_path
    if not os.path.exists(src):
        src = project_path

    fd, tags_path = tempfile.mkstemp(prefix='ctags_', suffix='.tags')
    os.close(fd)

    cmd = [
        'ctags',
        '--output-format=json',
        '--fields=+n',
        '--extras=+r',
        '--recurse',
        '-f', tags_path,
        src,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return tags_path
    except FileNotFoundError:
        print('Error: ctags not found on PATH. Install universal-ctags or exuberant-ctags.', file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print('ctags failed:', e, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)

    try:
        os.remove(tags_path)
    except Exception:
        pass
    return ''


def parse_ctags_jsonlines(tags_path: str) -> Set[str]:
    """Return a set of user-defined names (functions/methods/classes/structs) found in ctags output."""
    names = set()
    try:
        with open(tags_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    tag = json.loads(line)
                except json.JSONDecodeError:
                    continue

                kind = tag.get('kind', '')
                name = tag.get('name', '')
                if kind in CTAGS_KINDS and name:
                    # normalize C++ method names like Class::method -> method
                    simple = name.split('::')[-1]
                    simple = simple.split('.')[-1]
                    names.add(simple)
    except Exception as e:
        print(f'Error reading tags file: {e}', file=sys.stderr)
    return names


def detect_language_from_ext(path: str) -> str:
    ext = Path(path).suffix.lower()
    for lang, exts in SUPPORTED_LANG_EXTS.items():
        if ext in exts:
            return lang
    return 'unknown'


CALL_PATTERN = re.compile(r'([A-Za-z_][A-Za-z0-9_\.:$]*)\s*\(')


def find_user_calls_in_file(file_path: str, user_names: Set[str]) -> List[str]:
    """Scan file and return sorted list of user-defined names that are called in it."""
    try:
        content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f'Error reading {file_path}: {e}', file=sys.stderr)
        return []

    matches = CALL_PATTERN.findall(content)
    found = set()

    for call in matches:
        # call can be: func, obj.method, ns::func, obj$method (JS), etc.
        # extract the final identifier and check against user_names
        # handle :: first
        final = call.split('::')[-1]
        final = final.split('.')[-1]
        final = final.split('$')[-1]
        if final in user_names:
            found.add(final)

    return sorted(found)


def function_detector(project_path: str, target_dir: str="src", src_file: str="") -> List[str] | None:

    if not os.path.exists(project_path):
        print('Project path does not exist:', project_path, file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(src_file):
        print('Source file not found:', src_file, file=sys.stderr)
        sys.exit(2)

    tags_path = run_ctags(project_path, target_dir)
    if not tags_path:
        sys.exit(2)

    try:
        user_names = parse_ctags_jsonlines(tags_path)
        calls = find_user_calls_in_file(src_file, user_names)
        return calls

    finally:
        try:
            os.remove(tags_path)
        except Exception:
            return None

print(function_detector(os.path.join("tmp", "gameOfLife.gl"), "src", os.path.join("tmp", "gameOfLife.gl", "src", "main.cpp")))