import os
from pathlib import Path
import subprocess
import sys

import click


WHEELS_DIR = Path(__file__).parent.absolute()/'src'/'azure_devops_artifacts_helpers'/'wheels'

DOWNLOAD_INDEX_URL = os.environ.get('PIP_INDEX_URL', "https://pypi.org/simple")

PYTHON_VERSIONS = ['3.5', '3.6', '3.7', '3.8', '3.9']


@click.command()
@click.option('--index-url', default=DOWNLOAD_INDEX_URL, help='Index URL to use')
@click.option('--py', 'python_versions', default=PYTHON_VERSIONS, multiple=True, help='Python versions to populate')
@click.option('--target-dir', default=str(WHEELS_DIR), help='Target directory to output to')
def populate_wheels(index_url=DOWNLOAD_INDEX_URL, python_versions=PYTHON_VERSIONS, target_dir=str(WHEELS_DIR)):
    for py_version in python_versions:
        print(f'PLATFORM: {sys.platform} - PYTHON VERSION: {py_version}')
        args = [sys.executable, '-m', 'pip', 'download',
                '--only-binary=:all:',
                f'--python-version={py_version}',
                '-d', target_dir,
                '--index-url', index_url,
                '-r', 'embed_requirements.txt']
        print(' '.join(args))
        print(subprocess.check_output(args).decode())
    print(f'Downloaded Packages to {target_dir}')
    print('\t- '+'\n\t- '.join([u for u in os.listdir(target_dir) if u.endswith('whl')] ))


if __name__ == "__main__":
    populate_wheels()
