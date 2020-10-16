#!/usr/bin/env python
"""
Setup script for azure_devops_artifacts_helpers
===============================================

Call from command line as::

    python setup.py --help

to see the options available.
"""
from setuptools import setup
from setuptools import find_packages

try:
    import versioneer
    __version__ = versioneer.get_version()
    cmdclass = versioneer.get_cmdclass()
except AttributeError:
    __version__ = '0.0.0'
    cmdclass = None

__author__ = 'David Pugh'
__email__ = 'djpugh@gmail.com'

description = 'Bootstrap using Private Azure Devops Artifacts Feeds as an index-url with virtualenv/tox'

with open('README.rst') as f:
    readme = f.read()
    f.close()

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

kwargs = dict(name='azure_devops_artifacts_helpers',
              version=__version__,
              author=__author__,
              author_email=__email__,
              classifiers=[],
              packages=find_packages('src'),
              package_dir={'': 'src'},
              requires=[],
              install_requires=[],
              provides=['azure_devops_artifacts_helpers'],
              url='https://github.com/djpugh/azure_devops_artifacts_helpers>',
              test_suite='tests',
              description=description,
              long_description=readme,
              package_data={'': ['*.rst',
                                 'requirements.txt',
                                 '*.ini',
                                 '*.cfg']}
              )

if cmdclass is not None:
    kwargs['cmdclass'] = cmdclass

setup(**kwargs)
