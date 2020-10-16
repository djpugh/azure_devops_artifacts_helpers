#!/usr/bin/env python
"""
Setup script for azure_devops_artifacts_helpers
===============================================

Call from command line as::

    python setup.py --help

to see the options available.
"""
import os
from pathlib import Path
import subprocess
import sys

from setuptools import setup
from setuptools.config import read_configuration
from pkg_resources import parse_version, parse_requirements

try:
    import versioneer
    __version__ = versioneer.get_version()
    cmdclass = versioneer.get_cmdclass()
except AttributeError:
    __version__ = '0.0.0'
    cmdclass = None


WHEELS_DIR = Path(__file__).parent.absolute()/'src'/'azure_devops_artifacts_helpers'/'wheels'

DOWNLOAD_INDEX_URL = os.environ.get('PIP_INDEX_URL', "https://pypi.org/simple")

PLATFORMS = ['win32']  # , 'linux_x86_64', 'any']
PYTHON_VERSIONS = ['3.5', '3.6', '3.7', '3.8', '3.9']

# We are going to take the approach that the requirements.txt specifies
# exact (pinned versions) to use but install_requires should only
# specify package names
# see https://caremad.io/posts/2013/07/setup-vs-requirement/
# install_requires should specify abstract requirements e.g.::
#
#   install_requires = ['requests']
#
# whereas the requirements.txt file should specify pinned versions to
# generate a repeatable environment

with open('requirements.txt') as f:
    install_requires = []
    for req in parse_requirements(f.read()):
        install_requires.append(str(req).replace('==', '>='))

if parse_version(__version__) < parse_version('0.2.0'):
    development_status = 'Development Status :: 2 - Pre-Alpha'
elif parse_version(__version__).is_prerelease :
    development_status = 'Development Status :: 4 - Beta'
elif parse_version(__version__) >= parse_version('0.2.0'):
    development_status = 'Development Status :: 5 - Production/Stable'
elif parse_version(__version__) >= parse_version('1.0.0'):
    development_status = 'Development Status :: 6 - Mature'
else:
    development_status = 'Development Status :: 1 - Planning'

config = read_configuration('setup.cfg')
# See https://pypi.org/classifiers/
classifiers = config['metadata']['classifiers']
classifiers.append(development_status)
for py_version in PYTHON_VERSIONS:
    classifiers.append(f'Programming Language :: Python :: {py_version}')

for platform in PLATFORMS:
    if platform == 'win32':
        classifiers.append("Operating System :: Microsoft :: Windows")
    if platform == 'linux_x86_64':
        classifiers.append("Operating System :: POSIX")

kwargs = {'install_requires': install_requires,
          'version':  __version__,
          'classifiers': classifiers}


if cmdclass is not None:
    kwargs['cmdclass'] = cmdclass



def populate_wheels(index_url=DOWNLOAD_INDEX_URL, python_versions=PYTHON_VERSIONS):
    for platform in PLATFORMS:
        print(f'PLATFORM: {platform}')
        for py_version in python_versions:
            print(f'PYTHON VERSION: {py_version}')
            print(subprocess.check_output([sys.executable, '-m', 'pip', 'download',
                                           '--only-binary=:all:',
                                           '--platform', platform,
                                           '--python-version', py_version,
                                           '--implementation', 'py',
                                           '-d', str(WHEELS_DIR),
                                           '--index-url', index_url,
                                           '-r', 'embed_requirements.txt']).decode())
    print('Downloaded Packages')
    print(os.listdir(str(WHEELS_DIR)))

populate_wheels(index_url=DOWNLOAD_INDEX_URL,
                python_versions=PYTHON_VERSIONS)

setup(**kwargs)