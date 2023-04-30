import json
import os
from pathlib import Path
import subprocess
import sys

import click
from packaging.version import Version

if sys.version_info.minor >= 11 and sys.version_info.major >= 3:
    import tomllib as toml
else:
    import tomli as toml


WHEELS_DIR = Path(__file__).parent.absolute()/'src'/'azure_devops_artifacts_helpers'/'wheels'

DOWNLOAD_INDEX_URL = os.environ.get('PIP_INDEX_URL', "https://pypi.org/simple")




@click.command()
@click.option('--index-url', default=DOWNLOAD_INDEX_URL, help='Index URL to use')
@click.option('--py', 'python_versions', default=None, multiple=True, help='Python versions to populate, defaults to values set in pyproject.toml', type=str)
@click.option('--target-dir', default=str(WHEELS_DIR), help='Target directory to output to')
def populate_wheels(index_url=DOWNLOAD_INDEX_URL, python_versions=[], target_dir=str(WHEELS_DIR)):
    # Load from toml section
    with open('pyproject.toml') as f:
        pyproject_toml = toml.loads(f.read())
    packages = pyproject_toml['project']['optional-dependencies']['vendored']
    required_python_versions = pyproject_toml['project']['requires-python']
    dependencies = pyproject_toml['project']['requires-python']
    if not python_versions:
        # This works for same minor version only - assuming no major version change
        min_version, max_version = required_python_versions.split(',')
        # Version
        if min_version.startswith('>='):
            min_version = Version(min_version.lstrip('>='))
        elif min_version.startswith('>'):
            _v = Version(min_version.lstrip('>'))
            min_version = Version(f'{_v.major}.{_v.minor+1}')
        if max_version.startswith('<='):
            max_version = Version(max_version.lstrip('<='))
        elif max_version.startswith('<'):
            _v = Version(max_version.lstrip('<'))
            max_version = Version(f'{_v.major}.{_v.minor-1}')
        python_versions = [f'{min_version.major}.{minor}' for minor in range(min_version.minor, max_version.minor)]


    for py_version in python_versions:
        print(f'PLATFORM: {sys.platform} - PYTHON VERSION: {py_version}')
        args = [sys.executable, '-m', 'pip', 'download',
                '--only-binary=:all:',
                f'--python-version={py_version}',
                '-d', target_dir,
                '--index-url', index_url] + packages
        print(' '.join(args))
        print(subprocess.check_output(args).decode())
    print('Downloaded Packages to '+target_dir)
    print('\t- '+'\n\t- '.join([u for u in os.listdir(target_dir) if u.endswith('whl')] ))


if __name__ == "__main__":
    populate_wheels()
