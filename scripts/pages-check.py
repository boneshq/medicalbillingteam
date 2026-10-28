#!/usr/bin/env python3
"""pages-check: verify what GitHub Pages publishes from this repo.

Usage (from the repo root): python3 scripts/pages-check.py <built-site-dir>

<built-site-dir> is the output of the same Jekyll build GitHub Pages runs
(actions/jekyll-build-pages, see .github/workflows/pages-check.yml). Fails when
  - an internal file would be published (_build/, docs/, scripts/, README.md, source/config types),
  - .nojekyll is back (Pages would skip Jekyll and publish every file in the repo),
  - a public file is missing from the build or the build changed its bytes,
  - the build produced a file that is not in the repo.
Stdlib only.
"""
import pathlib, subprocess, sys

INTERNAL = ('_build/', 'docs/', 'scripts/', '.github/', 'README.md', '_config.yml', '.nojekyll')
INTERNAL_EXT = {'.md', '.py', '.pyc', '.sh', '.gs', '.yml', '.yaml', '.toml', '.env'}


def main(site_dir):
    site = pathlib.Path(site_dir)
    if not site.is_dir(): sys.exit(f'pages-check: no built site at {site}')
    out = subprocess.run(['git', 'ls-files', '-z'], capture_output=True, text=True, check=True).stdout
    tracked = [p for p in out.split('\0') if p]
    public = {p for p in tracked if not p.startswith(INTERNAL)}
    built = {f.relative_to(site).as_posix() for f in site.rglob('*') if f.is_file()}

    errors = []
    if '.nojekyll' in tracked:
        errors.append('.nojekyll is tracked: Pages would skip Jekyll and publish every file in the repo')
    for p in sorted(built):
        if p.startswith(INTERNAL) or pathlib.PurePosixPath(p).suffix.lower() in INTERNAL_EXT:
            errors.append(f'internal file would be published: {p}')
        elif p not in public:
            errors.append(f'build produced a file that is not in the repo: {p}')
    for p in sorted(public - built):
        errors.append(f'public file missing from the build: {p}')
    for p in sorted(public & built):
        if (site / p).read_bytes() != pathlib.Path(p).read_bytes():
            errors.append(f'build changed a public file: {p}')

    for e in errors: print('pages-check:', e)
    if errors: sys.exit(f'pages-check: FAIL ({len(errors)} problem(s))')
    print(f'pages-check: ok, {len(built)} files published, none internal, all byte-identical')


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
