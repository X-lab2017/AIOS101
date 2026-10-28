#!/usr/bin/env python3
"""Run the same repository checks locally and in GitHub Actions."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = [
    [sys.executable, 'scripts/package_course_brand.py', '--check'],
    [sys.executable, 'scripts/sync_status.py'],
    [sys.executable, 'scripts/build_site.py'],
    *[['node', '--check', 'site/'+name] for name in
      ['app.js', 'brand.js', 'learning-data.js', 'learning-core.js', 'figure-viewer.js']],
    ['node', 'scripts/check_learning.js'],
    ['node', 'scripts/check_reading.js'],
    [sys.executable, 'scripts/check_course_markdown.py'],
    [sys.executable, 'scripts/check_repo.py'],
    [sys.executable, 'scripts/check_site.py'],
]
for command in checks:
    print('RUN: '+' '.join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)
print('PASS: all repository and reading-site checks')
