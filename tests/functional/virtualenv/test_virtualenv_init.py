from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

TEST_VENV_NAME = '.venv'

if sys.platform.startswith('win'):
    pip_path = Path(TEST_VENV_NAME)/'scripts'/'pip'
else:
    pip_path = Path(TEST_VENV_NAME)/'bin'/'pip'


class VirtualEnvTestCase(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()

    def tearDown(self):
        try:
            self.td.cleanup()
        except PermissionError:
            pass

    def test_venv_pip(self):
        subprocess.check_call([sys.executable, '-m', 'virtualenv', str(Path(self.td.name)/TEST_VENV_NAME), '--seeder', 'azdo-pip'])
        installed_packages = subprocess.check_output([str(Path(self.td.name)/pip_path), 'freeze']).decode()
        self.assertIn('artifacts-keyring', installed_packages)
        self.assertIn('requests', installed_packages)
        self.assertIn('keyring', installed_packages)
