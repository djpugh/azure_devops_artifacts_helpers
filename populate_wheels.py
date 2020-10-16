import os
from pathlib import Path
import subprocess
import sys


wheels_dir = Path(__file__).parent.absolute()/'src'/'azure_devops_artifacts_helpers'/'wheels'

ARTIFACTS_KEYRING_VERSION = "0.2.10"
INDEX_URL = os.environ.get('PIP_INDEX_URL', "https://pypi.org/simple")

PYTHON_VERSIONS = ['3.5', '3.6', '3.7', '3.8', '3.9']


def populate(artifacts_keyring_version=ARTIFACTS_KEYRING_VERSION, index_url=INDEX_URL, python_versions=PYTHON_VERSIONS):
    for py_version in python_versions:
        subprocess.check_call([sys.executable, '-m', 'pip', 'download',
                            '--only-binary=:all:',
                            '--platform', 'any',
                            '--python-version', py_version,
                            '--implementation', 'py',
                            '-d', str(wheels_dir),
                            '--index-url', index_url,
                            f'artifacts-keyring=={artifacts_keyring_version}'])


if __name__ == "__main__":
    populate()
