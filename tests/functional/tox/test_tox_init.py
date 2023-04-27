from pathlib import Path
import tempfile
import subprocess
import sys
import unittest


TOX_INI = 'tox.ini'


class ToxTestCase(unittest.TestCase):

    @property
    def tox_ini(self):
        return """
[tox]
envlist = {test}
requires =
    azure_devops_artifacts_helpers
[testenv:test]
skip_install = True
commands =
    pip install pydantic --no-cache-dir
    pip freeze
"""
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()

    def tearDown(self):
        try:
            self.td.cleanup()
        except (PermissionError, RecursionError):
            pass

    def test_tox(self):
        with open(str(Path(self.td.name)/TOX_INI), 'w') as f:
            f.write(self.tox_ini)
        tox_output = subprocess.check_output([sys.executable, '-m', 'tox', '-vv', '-c', str(Path(self.td.name)/TOX_INI), '--workdir', self.td.name]).decode()
        self.assertIn('artifacts-keyring', tox_output)
        self.assertIn('requests', tox_output)
        self.assertIn('keyring', tox_output)
        # Test local install
        self.assertIn('python -I -m pip install artifacts-keyring -f', tox_output)
        self.assertIn('Looking in links', tox_output)
        self.assertNotIn('Downloading artifacts-keyring', tox_output)
        print(tox_output)

    def test_tox_extra_args(self):
        with open(str(Path(self.td.name)/TOX_INI), 'w') as f:
            f.write(self.tox_ini)
        tox_output = subprocess.check_output([sys.executable, '-m', 'tox', '-vv', '-c', str(Path(self.td.name)/TOX_INI), '--workdir', self.td.name, '--sitepackages', '--alwayscopy']).decode()
        self.assertIn('artifacts-keyring', tox_output)
        self.assertIn('requests', tox_output)
        self.assertIn('keyring', tox_output)
        # Test local install
        self.assertIn('python -I -m pip install artifacts-keyring -f', tox_output)
        self.assertIn('Looking in links', tox_output)
        self.assertNotIn('Downloading artifacts-keyring', tox_output)
        print(tox_output)
