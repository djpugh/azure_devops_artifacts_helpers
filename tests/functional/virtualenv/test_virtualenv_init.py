from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

if sys.platform.startswith('win'):
    pip_path = Path('.venv')/'scripts'/'pip'
else:
    pip_path = Path('.venv')/'bin'/'pip'


class VirtualEnvTestCase(unittest.TestCase):

    def test_venv_pip(self):
        with tempfile.TemporaryDirectory() as td:
            subprocess.check_call([sys.executable, '-m', 'virtualenv', f'{td}/.venv', '--seeder', 'azdo-pip'])
            installed_packages = subprocess.check_output([str(Path(td)/pip_path), 'freeze']).decode()
            self.assertIn('artifacts-keyring', installed_packages)
            self.assertIn('requests', installed_packages)
            self.assertIn('keyring', installed_packages)
