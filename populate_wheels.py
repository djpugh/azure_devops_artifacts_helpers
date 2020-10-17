import json
import os
from pathlib import Path
import subprocess
import sys

import click


WHEELS_DIR = Path(__file__).parent.absolute()/'src'/'azure_devops_artifacts_helpers'/'wheels'

with open(str(Path(__file__).parent.absolute()/'supported_python_versions.json')) as f:
    DEFAULT_PYTHON_VERSIONS = json.load(f)

DOWNLOAD_INDEX_URL = os.environ.get('PIP_INDEX_URL', "https://pypi.org/simple")



@click.command()
@click.option('--index-url', default=DOWNLOAD_INDEX_URL, help='Index URL to use')
@click.option('--py', 'python_versions', default=DEFAULT_PYTHON_VERSIONS, multiple=True, help='Python versions to populate')
@click.option('--target-dir', default=str(WHEELS_DIR), help='Target directory to output to')
def populate_wheels(index_url=DOWNLOAD_INDEX_URL, python_versions=DEFAULT_PYTHON_VERSIONS, target_dir=str(WHEELS_DIR)):
    for py_version in python_versions:
        print('PLATFORM: {} - PYTHON VERSION: {}'.format(sys.platform, py_version))
        args = [sys.executable, '-m', 'pip', 'download',
                '--only-binary=:all:',
                '--python-version='+py_version,
                '-d', target_dir,
                '--index-url', index_url,
                '-r', 'embed_requirements.txt']
        print(' '.join(args))
        print(subprocess.check_output(args).decode())
    print('Downloaded Packages to '+target_dir)
    print('\t- '+'\n\t- '.join([u for u in os.listdir(target_dir) if u.endswith('whl')] ))


if __name__ == "__main__":
    populate_wheels()
