import tempfile
import subprocess
import sys
import unittest



class VirtualEnvTestCase(unittest.TestCase):

    def test_venv_pip(self):
        with tempfile.TemporaryDirectory() as td:
            subprocess.check_call([sys.executable, '-m', 'virtualenv', f'{td}/.venv', '--seeder', 'azdo-pip'])
            installed_packages = subprocess.check_output([f'{td}/.venv/scripts/pip', 'freeze']).decode()
            self.assertIn('artifacts-keyring', installed_packages)
            self.assertIn('requests', installed_packages)
            self.assertIn('keyring', installed_packages)
